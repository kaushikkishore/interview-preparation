# Sample Tricky Go Questions and Answers

## Question 1: Slice Modification

**Q: What's the output of this code and why?**
```go
func main() {
    s := []int{1, 2, 3}
    modify(s)
    fmt.Println(s)
}

func modify(s []int) {
    s = append(s, 4)
    s[0] = 99
}
```

**A:** The output is `[1 2 3]`

This is because:
1. When a slice is passed to a function, it's passed by value but this value contains a pointer to the underlying array
2. The `append(s, 4)` operation in `modify()` creates a new backing array since the original slice has capacity 3
3. After `append()`, `s` inside `modify()` points to a new array, so the `s[0] = 99` operation modifies this new array
4. The original slice in `main()` still points to the original array, which remains unchanged

If we changed the code to:
```go
func modify(s []int) {
    s[0] = 99       // Modifies original backing array
    s = append(s, 4) // Now creates new backing array, but too late
}
```
Then the output would be `[99 2 3]` because we modified the original array before creating a new one.

## Question 2: Closure Variable Capture

**Q: Explain what happens in this code and fix the issue:**
```go
func main() {
    ch := make(chan int)
    for i := 0; i < 10; i++ {
        go func() {
            ch <- i
        }()
    }
    
    for j := 0; j < 10; j++ {
        fmt.Println(<-ch)
    }
}
```

**A:** The issue is that the closure is capturing the loop variable `i` by reference, not by value. 

When the goroutines execute, they all reference the same variable `i`, which will likely have the value 10 by the time most goroutines run. So instead of getting values 0-9, we'll likely get the value 10 multiple times (or possibly 9 or other values depending on when each goroutine executes).

The fix is to pass the value of `i` as a parameter to the anonymous function:

```go
func main() {
    ch := make(chan int)
    for i := 0; i < 10; i++ {
        go func(val int) {
            ch <- val
        }(i)  // Pass i as an argument to create a new value for each goroutine
    }
    
    for j := 0; j < 10; j++ {
        fmt.Println(<-ch)
    }
}
```

Alternatively in Go 1.22+, for loop variables are no longer shared between iterations, so the original code would work as expected. But the explicit parameter approach works in all Go versions.

## Question 3: Concurrent Map Access

**Q: What's wrong with this concurrent map access and how would you fix it?**
```go
func processData(data map[string]int, keys []string) {
    var wg sync.WaitGroup
    for _, k := range keys {
        wg.Add(1)
        go func(key string) {
            defer wg.Done()
            data[key]++
        }(k)
    }
    wg.Wait()
}
```

**A:** The code has a race condition because multiple goroutines are accessing the map concurrently without synchronization. In Go, maps are not safe for concurrent use.

This can result in:
- Non-deterministic behavior
- Potential memory corruption
- Runtime panic with "concurrent map read/write" error

To fix this, we need to add synchronization:

```go
func processData(data map[string]int, keys []string) {
    var mu sync.Mutex
    var wg sync.WaitGroup
    
    for _, k := range keys {
        wg.Add(1)
        go func(key string) {
            defer wg.Done()
            
            mu.Lock()
            data[key]++
            mu.Unlock()
        }(k)
    }
    wg.Wait()
}
```

Alternatively, we could use the thread-safe `sync.Map` for Go 1.9+:

```go
func processData(data *sync.Map, keys []string) {
    var wg sync.WaitGroup
    
    for _, k := range keys {
        wg.Add(1)
        go func(key string) {
            defer wg.Done()
            
            val, _ := data.LoadOrStore(key, 0)
            data.Store(key, val.(int) + 1)
        }(k)
    }
    wg.Wait()
}
```

## Question 4: Defer and Return Values

**Q: What will this function return and why?**
```go
func example() (result int) {
    defer func() {
        result *= 2
    }()
    return 5
}
```

**A:** The function will return 10.

This is because:
1. The `return 5` statement first assigns 5 to the named return variable `result`
2. Then the deferred function executes, which multiplies `result` by 2, changing it to 10
3. Finally, the function returns with the modified `result` value

This demonstrates that deferred functions can modify named return values because they execute after the return value is set but before the function actually returns to the caller.

## Question 5: Interface Values and nil

**Q: What will this code print and why?**
```go
type MyError struct {
    Msg string
}

func (e *MyError) Error() string {
    return e.Msg
}

func process() error {
    var err *MyError
    // Do something that may set err
    return err
}

func main() {
    err := process()
    if err == nil {
        fmt.Println("No error")
    } else {
        fmt.Println("Error:", err)
    }
}
```

**A:** This will print `Error: <nil>`.

Explanation:
1. The `process()` function returns a `nil` *MyError pointer
2. However, it's returned as an `error` interface value
3. An interface value is considered non-nil even if the concrete value it holds is nil
4. The interface has two components: a type descriptor and a value
5. Here the interface has type *MyError but nil value
6. This creates a non-nil interface containing a nil pointer

To fix this, you should explicitly return nil when the error is nil:

```go
func process() error {
    var err *MyError
    // Do something that may set err
    if err == nil {
        return nil // Return nil interface, not typed nil
    }
    return err
}
```

## Question 6: Channel Behavior

**Q: What will happen when this code executes? Will it print anything?**
```go
func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 10; i++ {
            ch <- i
        }
    }()
    
    for {
        select {
        case val := <-ch:
            fmt.Println(val)
        case <-time.After(time.Second):
            fmt.Println("Timeout")
            return
        }
    }
}
```

**A:** The code will print numbers 0 to 9 and then, after a 1-second pause, will print "Timeout" and exit.

Explanation:
1. The goroutine sends values 0-9 to the channel
2. The main function receives and prints each value as it arrives
3. The `time.After(time.Second)` creates a new timer for each iteration of the loop
4. After receiving all 10 values, the select statement will block
5. When no more values arrive for 1 second, the timeout case executes
6. "Timeout" is printed and the function returns

Note that this isn't the most efficient approach because a new timer is created on each iteration. A better approach would be:

```go
func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 10; i++ {
            ch <- i
        }
        close(ch)
    }()
    
    timeout := time.After(time.Second)
    for {
        select {
        case val, ok := <-ch:
            if !ok {
                // Channel closed, all done
                return
            }
            fmt.Println(val)
        case <-timeout:
            fmt.Println("Timeout")
            return
        }
    }
}
```

## Question 7: Initializing Structs

**Q: What is wrong with the following struct initialization?**
```go
type Config struct {
    Server string
    Port   int
    Timeout time.Duration
    MaxConnections int
}

func main() {
    conf := Config{
        "localhost",
        8080,
        5 * time.Second,
        MaxConnections: 10,
    }
    fmt.Println(conf)
}
```

**A:** The initialization mixes positional and named arguments, which is not allowed in Go.

You must either:
1. Use all positional arguments:
```go
conf := Config{
    "localhost",
    8080,
    5 * time.Second,
    10,
}
```

2. Or use all named arguments:
```go
conf := Config{
    Server: "localhost",
    Port: 8080,
    Timeout: 5 * time.Second,
    MaxConnections: 10,
}
```

Named arguments are preferred as they're clearer and more maintainable, especially when struct fields change.

## Question 8: Slice Capacity

**Q: What will this code print and why?**
```go
func main() {
    a := make([]int, 3, 5)
    a[0], a[1], a[2] = 1, 2, 3
    
    b := append(a, 4, 5)
    b[0] = 99
    
    c := append(a, 6, 7, 8)
    
    fmt.Println("a:", a)
    fmt.Println("b:", b)
    fmt.Println("c:", c)
}
```

**A:** The output will be:
```
a: [1 2 3]
b: [99 2 3 4 5]
c: [1 2 3 6 7 8]
```

Explanation:
1. `a` is a slice with length 3 and capacity 5
2. `b` is created by appending two elements to `a`
   - Since `a` has capacity 5 and length 3, the backing array has room for 2 more elements
   - `b` shares the same backing array as `a`
   - When `b[0]` is modified to 99, it also modifies the backing array shared with `a`
   - But `a`'s length is still 3, so printing `a` shows only the first 3 elements
3. `c` is created by appending three elements to `a`
   - This exceeds the capacity of `a`'s backing array
   - A new, larger backing array is allocated
   - Elements from `a` are copied to this new array
   - Because `c` has a different backing array, the change to `b[0]` isn't reflected in `c`

## Question 9: Method Sets

**Q: Why does this code not compile and how would you fix it?**
```go
type Counter int

func (c Counter) Increment() {
    c++
}

func main() {
    var c Counter
    fmt.Println("Initial:", c)
    
    c.Increment()
    fmt.Println("After increment:", c)
}
```

**A:** The code compiles but doesn't behave as expected. It will print:
```
Initial: 0
After increment: 0
```

The issue is that the `Increment()` method has a value receiver, not a pointer receiver. This means it operates on a copy of the Counter value, not the original.

To fix it, change the method to use a pointer receiver:

```go
func (c *Counter) Increment() {
    *c++
}
```

Then it will print:
```
Initial: 0
After increment: 1
```

This is a common mistake in Go. Methods with value receivers operate on copies, so they can't modify the original value. Use pointer receivers when you need to modify the receiver.

## Question 10: Goroutine Leaks

**Q: What's wrong with this code and how would you fix it?**
```go
func searchItems(query string, items []string) string {
    ch := make(chan string)
    
    for _, item := range items {
        go func(item string) {
            if strings.Contains(item, query) {
                ch <- item
            }
        }(item)
    }
    
    return <-ch
}
```

**A:** This code has a goroutine leak:
1. It launches a goroutine for each item to check if it contains the query
2. It only reads one result from the channel before returning
3. If multiple items match, all other goroutines will be blocked trying to send to the channel
4. If no items match, all goroutines will be blocked and the function will deadlock

There are multiple ways to fix this:

1. Use a buffered channel to prevent blocking:
```go
func searchItems(query string, items []string) (string, bool) {
    ch := make(chan string, len(items))
    
    for _, item := range items {
        go func(item string) {
            if strings.Contains(item, query) {
                ch <- item
            } else {
                ch <- ""
            }
        }(item)
    }
    
    for i := 0; i < len(items); i++ {
        if result := <-ch; result != "" {
            return result, true
        }
    }
    
    return "", false
}
```

2. Use context for cancellation:
```go
func searchItems(query string, items []string) (string, bool) {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel() // Ensure all goroutines are cancelled
    
    ch := make(chan string)
    
    for _, item := range items {
        go func(item string) {
            if strings.Contains(item, query) {
                select {
                case ch <- item:
                case <-ctx.Done():
                    // Cancelled, exit goroutine
                }
            }
        }(item)
    }
    
    select {
    case result := <-ch:
        return result, true
    case <-time.After(time.Second):
        return "", false
    }
}
```

3. Or the simplest solution - just use a direct approach without goroutines:
```go
func searchItems(query string, items []string) (string, bool) {
    for _, item := range items {
        if strings.Contains(item, query) {
            return item, true
        }
    }
    return "", false
}
```

For this simple case, the direct approach is likely faster and clearer. Only use goroutines when the benefit of concurrency outweighs the complexity.
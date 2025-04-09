### 1. **Data Structures and Algorithms**

#### Questions from "What to expect":

- **Reverse a linked list.**
- **Find the shortest path in a graph.**
- **Implement a stack or queue.**

##### **Reverse a Linked List**

**Answer**: Let’s implement a singly linked list reversal in Go.

```go
package main

import "fmt"

// Node represents a linked list node
type Node struct {
    Value int
    Next  *Node
}

// Reverse reverses a linked list iteratively
func Reverse(head *Node) *Node {
    var prev *Node
    current := head
    for current != nil {
        next := current.Next   // Store next node
        current.Next = prev    // Reverse the link
        prev = current         // Move prev forward
        current = next         // Move current forward
    }
    return prev // New head
}

func main() {
    // Example: 1 -> 2 -> 3 -> nil
    list := &Node{1, &Node{2, &Node{3, nil}}}
    reversed := Reverse(list)
    for reversed != nil {
        fmt.Print(reversed.Value, " ")
        reversed = reversed.Next
    }
    // Output: 3 2 1
}
```

**Explanation**: We use three pointers (`prev`, `current`, `next`) to reverse the links iteratively. Time complexity is O(n), space complexity is O(1). In an interview, mention that Go’s lack of tail recursion optimization makes iteration preferable over recursion.

---

##### **Find the Shortest Path in a Graph**

**Answer**: Let’s use Breadth-First Search (BFS) to find the shortest path in an unweighted graph, implemented with a map in Go.

```go
package main

import "fmt"

// BFS finds the shortest path between start and end in an unweighted graph
func BFS(graph map[string][]string, start, end string) []string {
    visited := make(map[string]bool)
    queue := [][]string{{start}} // Queue of paths
    visited[start] = true

    if start == end {
        return []string{start}
    }

    for len(queue) > 0 {
        path := queue[0]
        queue = queue[1:]
        node := path[len(path)-1]

        for _, neighbor := range graph[node] {
            if !visited[neighbor] {
                visited[neighbor] = true
                newPath := append([]string{}, path...) // Copy path
                newPath = append(newPath, neighbor)
                if neighbor == end {
                    return newPath
                }
                queue = append(queue, newPath)
            }
        }
    }
    return nil // No path found
}

func main() {
    graph := map[string][]string{
        "A": {"B", "C"},
        "B": {"A", "D"},
        "C": {"A", "D"},
        "D": {"B", "C"},
    }
    path := BFS(graph, "A", "D")
    fmt.Println(path) // Output: [A D]
}
```

**Explanation**: BFS guarantees the shortest path in an unweighted graph. We use a queue to explore nodes level by level and track the path. Time complexity is O(V + E), space complexity is O(V), where V is vertices and E is edges.

---

##### **Implement a Stack or Queue**

**Answer**: Let’s implement a stack using a slice in Go.

```go
package main

import "fmt"

type Stack struct {
    items []int
}

// Push adds an item to the top
func (s *Stack) Push(item int) {
    s.items = append(s.items, item)
}

// Pop removes and returns the top item
func (s *Stack) Pop() (int, bool) {
    if len(s.items) == 0 {
        return 0, false
    }
    index := len(s.items) - 1
    item := s.items[index]
    s.items = s.items[:index]
    return item, true
}

func main() {
    stack := Stack{}
    stack.Push(1)
    stack.Push(2)
    stack.Push(3)
    if item, ok := stack.Pop(); ok {
        fmt.Println(item) // Output: 3
    }
}
```

**Explanation**: A stack is LIFO (Last In, First Out). We use Go’s slice for dynamic sizing. Push is O(1) amortized, Pop is O(1). For a queue (FIFO), you’d use a similar approach but dequeue from the front (shift with `s.items[0], s.items = s.items[1:]`).

---

### 2. **Rate Limiter**

#### Questions from "What to expect":

- **Use a channel to control request flow.**
- **Handle concurrent requests with goroutines.**

##### **Use a Channel to Control Request Flow**

**Answer**: Here’s a simple rate limiter using a channel as a semaphore.

```go
package main

import (
    "fmt"
    "time"
)

func RateLimit(maxRequests int, duration time.Duration) chan struct{} {
    ch := make(chan struct{}, maxRequests)
    go func() {
        for {
            time.Sleep(duration / time.Duration(maxRequests))
            ch <- struct{}{} // Release a token
        }
    }()
    return ch
}

func main() {
    limiter := RateLimit(3, time.Second) // 3 requests per second
    for i := 0; i < 5; i++ {
        <-limiter // Wait for a token
        fmt.Println("Request", i+1, "processed at", time.Now())
    }
}
```

**Explanation**: The channel acts as a token bucket with a capacity of `maxRequests`. Tokens are added at a fixed rate. Clients block until a token is available. This limits the rate to 3 requests per second here.

---

##### **Handle Concurrent Requests with Goroutines**

**Answer**: Let’s extend the rate limiter for concurrent clients.

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

type RateLimiter struct {
    tokens chan struct{}
}

func NewRateLimiter(maxRequests int, duration time.Duration) *RateLimiter {
    rl := &RateLimiter{tokens: make(chan struct{}, maxRequests)}
    go func() {
        ticker := time.NewTicker(duration / time.Duration(maxRequests))
        defer ticker.Stop()
        for range ticker.C {
            rl.tokens <- struct{}{}
        }
    }()
    return rl
}

func (rl *RateLimiter) Wait() {
    <-rl.tokens
}

func main() {
    rl := NewRateLimiter(2, time.Second) // 2 requests per second
    var wg sync.WaitGroup
    for i := 0; i < 5; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            rl.Wait()
            fmt.Println("Request", id, "processed at", time.Now())
        }(i)
    }
    wg.Wait()
}
```

**Explanation**: We wrap the limiter in a struct and use goroutines to simulate concurrent requests. Each goroutine waits for a token, ensuring no more than 2 requests per second. `sync.WaitGroup` ensures the program waits for all requests.

---

### 3. **Generators**

#### Questions from "What to expect":

- **Write a generator function in Go using a goroutine and channel.**
- **Explain how to iterate over the generated values.**

##### **Write a Generator Function in Go Using a Goroutine and Channel**

**Answer**: Here’s a generator for an infinite sequence of even numbers.

```go
package main

import "fmt"

func EvenNumbers() chan int {
    ch := make(chan int)
    go func() {
        for i := 0; ; i += 2 {
            ch <- i
        }
    }()
    return ch
}

func main() {
    evens := EvenNumbers()
    for i := 0; i < 5; i++ {
        fmt.Println(<-evens) // Prints 0, 2, 4, 6, 8
    }
}
```

**Explanation**: The goroutine runs an infinite loop, sending even numbers to the channel. The main function reads from the channel as needed. This is lazy evaluation—values are generated on demand.

---

##### **Explain How to Iterate Over the Generated Values**

**Answer**: In Go, you iterate over a generator’s values by reading from the channel it returns. You can use a `for` loop with a condition to limit the iteration or a `range` loop if the channel is closed (which isn’t the case here since it’s infinite). For example:

```go
evens := EvenNumbers()
for i := 0; i < 5; i++ {
    value := <-evens
    fmt.Println(value)
}
```

Alternatively, if the generator closes the channel after a finite sequence:

```go
func FiniteNumbers() chan int {
    ch := make(chan int)
    go func() {
        for i := 0; i < 5; i++ {
            ch <- i
        }
        close(ch)
    }()
    return ch
}

nums := FiniteNumbers()
for num := range nums {
    fmt.Println(num) // Prints 0, 1, 2, 3, 4
}
```

**Explanation**: With an infinite generator, you control the loop manually. With a finite one, `range` works after closing the channel to signal completion.

---

### 4. **Group Membership or Username Generator**

#### Questions from "What to expect" (Group Membership):

- **Add/remove users from groups.**
- **Check if a user belongs to a group.**

#### Questions from "What to expect" (Username Generator):

- **Generate a username from input.**
- **Ensure no duplicates.**

##### **Add/Remove Users from Groups**

**Answer**: Here’s a simple group membership system.

```go
package main

import "fmt"

type GroupManager struct {
    groups map[string][]string // group -> users
}

func NewGroupManager() *GroupManager {
    return &GroupManager{groups: make(map[string][]string)}
}

func (gm *GroupManager) AddUser(group, user string) {
    gm.groups[group] = append(gm.groups[group], user)
}

func (gm *GroupManager) RemoveUser(group, user string) {
    users := gm.groups[group]
    for i, u := range users {
        if u == user {
            gm.groups[group] = append(users[:i], users[i+1:]...)
            return
        }
    }
}

func main() {
    gm := NewGroupManager()
    gm.AddUser("admins", "alice")
    gm.AddUser("admins", "bob")
    gm.RemoveUser("admins", "alice")
    fmt.Println(gm.groups["admins"]) // Output: [bob]
}
```

**Explanation**: We use a map of group names to user slices. Adding is O(1) amortized, removing is O(n) due to linear search and slice manipulation.

---

##### **Check if a User Belongs to a Group**

**Answer**: Add this method to the `GroupManager`.

```go
func (gm *GroupManager) IsMember(group, user string) bool {
    for _, u := range gm.groups[group] {
        if u == user {
            return true
        }
    }
    return false
}

func main() {
    gm := NewGroupManager()
    gm.AddUser("admins", "alice")
    fmt.Println(gm.IsMember("admins", "alice")) // Output: true
    fmt.Println(gm.IsMember("admins", "bob"))   // Output: false
}
```

**Explanation**: Linear search checks if the user exists in the group’s slice. Time complexity is O(n). For optimization, you could use a `map[string]struct{}` per group.

---

##### **Generate a Username from Input**

**Answer**: Here’s a basic username generator.

```go
package main

import (
    "fmt"
    "strings"
)

func GenerateUsername(firstName, lastName string) string {
    return strings.ToLower(firstName + "." + lastName)
}

func main() {
    username := GenerateUsername("John", "Doe")
    fmt.Println(username) // Output: john.doe
}
```

**Explanation**: Concatenates first and last names with a dot, converting to lowercase. Simple but meets basic requirements.

---

##### **Ensure No Duplicates**

**Answer**: Extend the generator with a uniqueness check.

```go
package main

import (
    "fmt"
    "strings"
)

type UsernameGenerator struct {
    used map[string]bool
}

func NewUsernameGenerator() *UsernameGenerator {
    return &UsernameGenerator{used: make(map[string]bool)}
}

func (ug *UsernameGenerator) Generate(firstName, lastName string) string {
    base := strings.ToLower(firstName + "." + lastName)
    if !ug.used[base] {
        ug.used[base] = true
        return base
    }
    for i := 1; ; i++ {
        candidate := fmt.Sprintf("%s%d", base, i)
        if !ug.used[candidate] {
            ug.used[candidate] = true
            return candidate
        }
    }
}

func main() {
    ug := NewUsernameGenerator()
    fmt.Println(ug.Generate("John", "Doe")) // Output: john.doe
    fmt.Println(ug.Generate("John", "Doe")) // Output: john.doe1
    fmt.Println(ug.Generate("John", "Doe")) // Output: john.doe2
}
```

**Explanation**: Uses a map to track used usernames. If a duplicate is found, appends a number until a unique name is generated. Time complexity is O(1) for the map lookup, though the loop could run longer in rare cases.

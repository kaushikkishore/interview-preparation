# Go-Specific Data Structures & Concurrency

## 1. Channels and Goroutines

### Q: Explain how you would implement a worker pool pattern in Go. How would you ensure all workers finish their tasks before the program exits?

**A:** A worker pool pattern in Go is implemented using goroutines and channels:

```go
func workerPool(numWorkers int, jobs <-chan Job, results chan<- Result) {
    var wg sync.WaitGroup
    
    // Launch workers
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                // Process the job
                result := processJob(job)
                results <- result
            }
        }(i)
    }
    
    // Wait for all workers to finish
    go func() {
        wg.Wait()
        close(results)  // Signal that no more results will come
    }()
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)
    
    // Start the worker pool
    workerPool(5, jobs, results)
    
    // Send jobs to the pool
    for i := 0; i < 10; i++ {
        jobs <- Job{ID: i}
    }
    close(jobs)  // Signal that no more jobs will come
    
    // Collect results
    for result := range results {
        fmt.Println(result)
    }
}
```

Key points:
- Use a `sync.WaitGroup` to track when all workers have completed
- Close the jobs channel to signal workers to exit
- Use a goroutine to wait for all workers and then close the results channel
- The main function waits for all results by ranging over the results channel

### Q: Write a function that performs concurrent binary search across multiple goroutines. How would you coordinate the results?

**A:** Here's a concurrent binary search implementation:

```go
func concurrentBinarySearch(arr []int, target int, concurrencyLevel int) (index int, found bool) {
    if len(arr) == 0 {
        return -1, false
    }
    
    // Divide array into segments
    segmentSize := len(arr) / concurrencyLevel
    if segmentSize == 0 {
        segmentSize = 1
        concurrencyLevel = len(arr)
    }
    
    type result struct {
        index int
        found bool
    }
    
    resultChan := make(chan result, concurrencyLevel)
    var wg sync.WaitGroup
    
    // Launch concurrent binary searches
    for i := 0; i < concurrencyLevel; i++ {
        wg.Add(1)
        go func(segmentIdx int) {
            defer wg.Done()
            
            // Calculate segment bounds
            start := segmentIdx * segmentSize
            end := start + segmentSize
            if segmentIdx == concurrencyLevel-1 {
                end = len(arr) // Last segment takes remaining elements
            }
            
            // Skip if segment is out of bounds
            if start >= len(arr) {
                return
            }
            
            // Check if target might be in this segment
            if arr[start] > target || arr[end-1] < target {
                return
            }
            
            // Perform binary search in this segment
            left, right := start, end-1
            for left <= right {
                mid := left + (right-left)/2
                if arr[mid] == target {
                    resultChan <- result{mid, true}
                    return
                } else if arr[mid] < target {
                    left = mid + 1
                } else {
                    right = mid - 1
                }
            }
        }(i)
    }
    
    // Close result channel when all searches complete
    go func() {
        wg.Wait()
        close(resultChan)
    }()
    
    // Check results
    for r := range resultChan {
        if r.found {
            return r.index, true
        }
    }
    
    return -1, false
}
```

Key points:
- Divide the array into segments and search each segment concurrently
- Use a channel to collect results from each goroutine
- Use a WaitGroup to wait for all searches to complete
- Return as soon as a match is found, or -1 if not found

### Q: How would you implement a thread-safe cache in Go without using mutexes?

**A:** Using sync/atomic and channels instead of mutexes:

```go
type Cache struct {
    data   atomic.Value // holds a map[string]interface{}
    writes chan writeOp
    reads  chan readOp
    quit   chan struct{}
}

type readOp struct {
    key      string
    response chan interface{}
}

type writeOp struct {
    key      string
    value    interface{}
    response chan bool
}

func NewCache() *Cache {
    c := &Cache{
        writes: make(chan writeOp),
        reads:  make(chan readOp),
        quit:   make(chan struct{}),
    }
    c.data.Store(make(map[string]interface{}))
    
    // Start background goroutine to handle operations
    go c.processOperations()
    return c
}

func (c *Cache) processOperations() {
    for {
        select {
        case read := <-c.reads:
            m := c.data.Load().(map[string]interface{})
            read.response <- m[read.key]
            
        case write := <-c.writes:
            // Copy on write pattern
            m := c.data.Load().(map[string]interface{})
            mCopy := make(map[string]interface{})
            for k, v := range m {
                mCopy[k] = v
            }
            mCopy[write.key] = write.value
            c.data.Store(mCopy)
            write.response <- true
            
        case <-c.quit:
            return
        }
    }
}

func (c *Cache) Get(key string) interface{} {
    response := make(chan interface{})
    c.reads <- readOp{key: key, response: response}
    return <-response
}

func (c *Cache) Set(key string, value interface{}) {
    response := make(chan bool)
    c.writes <- writeOp{key: key, value: value, response: response}
    <-response
}

func (c *Cache) Close() {
    close(c.quit)
}
```

Key points:
- Use atomic.Value for consistent snapshots of the cache
- Use channels for coordinating reads and writes
- Implement a Copy-on-Write pattern for thread safety
- Use a dedicated goroutine to serialize all operations

## 2. Slices vs. Arrays

### Q: What happens when you append to a slice that exceeds its capacity? Walk through the internal memory allocation process.

**A:** When appending to a slice that exceeds its capacity:

1. Go allocates a new, larger underlying array
2. The growth strategy is:
   - If the current capacity is less than 1024, capacity doubles
   - If capacity is at least 1024, capacity grows by 25%
3. Go copies all elements from the old array to the new array
4. The original slice header is updated to point to the new array with the new capacity
5. The new element is appended to the new array
6. The slice's length is incremented

Code example:
```go
func appendExample() {
    // Initial slice with capacity 4
    s := make([]int, 2, 4)
    fmt.Printf("Initial: len=%d cap=%d ptr=%p %v\n", len(s), cap(s), &s[0], s)
    
    // Append within capacity
    s = append(s, 3)
    fmt.Printf("Append 1: len=%d cap=%d ptr=%p %v\n", len(s), cap(s), &s[0], s)
    
    // Append within capacity again
    s = append(s, 4)
    fmt.Printf("Append 2: len=%d cap=%d ptr=%p %v\n", len(s), cap(s), &s[0], s)
    
    // Append beyond capacity (will allocate new array)
    s = append(s, 5)
    fmt.Printf("Append 3: len=%d cap=%d ptr=%p %v\n", len(s), cap(s), &s[0], s)
}
```

Output:
```
Initial: len=2 cap=4 ptr=0xc0000b2000 [0 0]
Append 1: len=3 cap=4 ptr=0xc0000b2000 [0 0 3]
Append 2: len=4 cap=4 ptr=0xc0000b2000 [0 0 3 4]
Append 3: len=5 cap=8 ptr=0xc0000b4000 [0 0 3 4 5]
```

Note how the pointer changed on the third append operation when capacity was exceeded.

### Q: Write a function that efficiently removes an element from the middle of a slice without using additional memory. What's the time complexity?

**A:** 
```go
func removeElement(s []int, index int) []int {
    if index < 0 || index >= len(s) {
        return s
    }
    
    // Shift elements after index one position left
    copy(s[index:], s[index+1:])
    
    // Return slice with last element truncated
    return s[:len(s)-1]
}
```

Time complexity:
- O(n-i) where n is the length of the slice and i is the index to remove
- In the worst case (removing the first element), this is O(n)
- The operation requires shifting all subsequent elements 

Space complexity: O(1) as we're modifying the slice in-place.

### Q: Explain the difference between passing a slice and an array to a function. How does this affect performance?

**A:** Key differences:

1. **Pass by value vs. reference**:
   - Arrays are passed by value (a complete copy is made)
   - Slices are passed by value of their header (pointer to underlying array, length, capacity)

2. **Memory usage**:
   - Passing an array copies all its elements (expensive for large arrays)
   - Passing a slice only copies the slice header (3 words: pointer, length, capacity)

3. **Mutation effects**:
   - Changes to an array inside a function don't affect the original array
   - Changes to a slice's elements inside a function affect the original slice's elements

4. **Performance implications**:
   - Arrays: higher memory usage, more copying overhead
   - Slices: minimal overhead, but can cause unintended side effects

```go
func modifyArray(arr [5]int) {
    arr[0] = 100 // Only modifies the local copy
}

func modifySlice(slc []int) {
    slc[0] = 100 // Modifies the original slice's underlying array
}

func main() {
    array := [5]int{1, 2, 3, 4, 5}
    slice := []int{1, 2, 3, 4, 5}
    
    modifyArray(array)
    modifySlice(slice)
    
    fmt.Println(array) // Output: [1 2 3 4 5] - unchanged
    fmt.Println(slice) // Output: [100 2 3 4 5] - modified
}
```

Performance-wise, using slices is almost always better due to reduced memory copying.

## 3. Maps and Concurrency

### Q: Why aren't Go maps safe for concurrent use? Implement a concurrent-safe map without using sync.Map.

**A:** Go maps aren't safe for concurrent use because they aren't designed with internal locking mechanisms. Concurrent reads are generally safe, but concurrent writes or a mix of reads and writes can lead to:
- Race conditions
- Map corruption
- Non-deterministic behavior
- Program crashes with "concurrent map read/write" panic

Implementing a concurrent-safe map:

```go
type ConcurrentMap struct {
    mu    sync.RWMutex
    items map[string]interface{}
}

func NewConcurrentMap() *ConcurrentMap {
    return &ConcurrentMap{
        items: make(map[string]interface{}),
    }
}

func (m *ConcurrentMap) Get(key string) (interface{}, bool) {
    m.mu.RLock()
    defer m.mu.RUnlock()
    
    val, exists := m.items[key]
    return val, exists
}

func (m *ConcurrentMap) Set(key string, value interface{}) {
    m.mu.Lock()
    defer m.mu.Unlock()
    
    m.items[key] = value
}

func (m *ConcurrentMap) Delete(key string) {
    m.mu.Lock()
    defer m.mu.Unlock()
    
    delete(m.items, key)
}

func (m *ConcurrentMap) Len() int {
    m.mu.RLock()
    defer m.mu.RUnlock()
    
    return len(m.items)
}
```

Key points:
- Use a read-write mutex to allow concurrent reads but exclusive writes
- Use deferred unlocks to ensure the mutex is always released
- RLock() for read operations, Lock() for write operations

### Q: How would you implement a custom hash table in Go that outperforms the built-in map for your specific use case?

**A:** A custom hash table could outperform the built-in map in specialized cases:

```go
type CustomHashTable struct {
    buckets    []*bucket
    numBuckets int
    size       int
}

type bucket struct {
    items []*item
}

type item struct {
    key   string
    value interface{}
}

func NewCustomHashTable(numBuckets int) *CustomHashTable {
    table := &CustomHashTable{
        buckets:    make([]*bucket, numBuckets),
        numBuckets: numBuckets,
    }
    
    for i := 0; i < numBuckets; i++ {
        table.buckets[i] = &bucket{items: make([]*item, 0, 8)}
    }
    
    return table
}

func (t *CustomHashTable) hash(key string) int {
    h := 0
    for i := 0; i < len(key); i++ {
        h = 31*h + int(key[i])
    }
    return h & (t.numBuckets - 1) // Assumes numBuckets is power of 2
}

func (t *CustomHashTable) Get(key string) (interface{}, bool) {
    bucketIndex := t.hash(key)
    bucket := t.buckets[bucketIndex]
    
    for _, item := range bucket.items {
        if item.key == key {
            return item.value, true
        }
    }
    
    return nil, false
}

func (t *CustomHashTable) Set(key string, value interface{}) {
    bucketIndex := t.hash(key)
    bucket := t.buckets[bucketIndex]
    
    // Check if key already exists
    for i, item := range bucket.items {
        if item.key == key {
            bucket.items[i].value = value
            return
        }
    }
    
    // Key doesn't exist, add new item
    bucket.items = append(bucket.items, &item{key: key, value: value})
    t.size++
    
    // Resize if load factor exceeds threshold
    if float64(t.size)/float64(t.numBuckets) > 0.75 {
        t.resize()
    }
}

func (t *CustomHashTable) resize() {
    // Double the number of buckets
    newTable := NewCustomHashTable(t.numBuckets * 2)
    
    // Rehash all items
    for _, bucket := range t.buckets {
        for _, item := range bucket.items {
            newTable.Set(item.key, item.value)
        }
    }
    
    // Update current table
    t.buckets = newTable.buckets
    t.numBuckets = newTable.numBuckets
}
```

Ways this could outperform the built-in map:
1. Use a specialized hash function optimized for your key distribution
2. Reduce memory overhead for your specific use case 
3. Use lock-free techniques for concurrent access
4. Implement custom conflict resolution strategies
5. Pre-allocate memory for expected load
6. Use SIMD instructions for hash computation
7. Implement domain-specific optimizations

### Q: Implement a LRU cache using Go's standard library. How would you make it thread-safe?

**A:** An LRU (Least Recently Used) cache with thread safety:

```go
type LRUCache struct {
    capacity int
    cache    map[string]*list.Element
    items    *list.List
    mu       sync.Mutex
}

type entry struct {
    key   string
    value interface{}
}

func NewLRUCache(capacity int) *LRUCache {
    return &LRUCache{
        capacity: capacity,
        cache:    make(map[string]*list.Element),
        items:    list.New(),
    }
}

func (c *LRUCache) Get(key string) (interface{}, bool) {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    element, exists := c.cache[key]
    if !exists {
        return nil, false
    }
    
    // Move to front (mark as most recently used)
    c.items.MoveToFront(element)
    return element.Value.(*entry).value, true
}

func (c *LRUCache) Put(key string, value interface{}) {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    // If key exists, update value and move to front
    if element, exists := c.cache[key]; exists {
        c.items.MoveToFront(element)
        element.Value.(*entry).value = value
        return
    }
    
    // If cache is full, remove the least recently used item
    if c.items.Len() >= c.capacity {
        oldest := c.items.Back()
        if oldest != nil {
            c.items.Remove(oldest)
            delete(c.cache, oldest.Value.(*entry).key)
        }
    }
    
    // Add new item to front
    element := c.items.PushFront(&entry{key: key, value: value})
    c.cache[key] = element
}

func (c *LRUCache) Remove(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    if element, exists := c.cache[key]; exists {
        c.items.Remove(element)
        delete(c.cache, key)
    }
}
```

Key points for thread safety:
1. Use a mutex to synchronize all operations
2. Lock/unlock the mutex for each operation
3. Use defer to ensure the mutex is always unlocked
4. Consider using a sync.RWMutex if reads greatly outnumber writes
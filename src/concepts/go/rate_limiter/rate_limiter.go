package main

import (
	"fmt"
	"time"
)

func RateLimiter(maxRequests int, duration time.Duration) chan struct{} {
	ch := make(chan struct{}, maxRequests)

	go func() {
		for {
			time.Sleep(duration / time.Duration(maxRequests))
			ch <- struct{}{}
		}
	}()
	return ch
}

func main() {
	limiter := RateLimiter(3, time.Minute)
	for i := 0; i < 5; i++ {
		<-limiter
		fmt.Println("Requests ", i+1, "processed at ", time.Now())

	}
}

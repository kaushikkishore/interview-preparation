"""
Finding the Median from a Data Stream
Let me explain how to efficiently find the median from a continuous data stream.
Problem Understanding
In this problem, we need to design a data structure that can:

Add new numbers to a dataset
Find the median of all numbers added so far at any time

The median is the middle value when data is sorted. 
If we have an odd number of elements, it's the middle element. If we have an even number, 
it's the average of the two middle elements.
"""

import heapq

class MedianFinder:
    def __init__(self):
        self.small_heap = []
        self.large_heap = []

    def add_num(self, num):
        # by default add to small heap 
        heapq.heappush(self.small_heap, -num)

        # make sure length of all elements in small heap is <= length of all elements in large heap 
        # move the largest element from small heap to large heap 
        if  self.small_heap and self.large_heap and -self.small_heap[0] > self.large_heap[0]:
            val = -heapq.heappop(self.small_heap)
            heapq.heappush(self.large_heap, val)

        # balance the heaps as their size should not be more than 1 
        if len(self.small_heap) > len(self.large_heap) +1:
            # small heap have more 
            val = -heapq.heappop(self.small_heap)
            heapq.heappush(self.large_heap, val)
        elif len(self.large_heap) > len(self.small_heap):
            # large heap have more elements 
            val = heapq.heappop(self.large_heap)
            heapq.heappush(self.small_heap, -val)

    def find_median(self):
        if len(self.small_heap) > len(self.large_heap):
            return -self.small_heap[0]
        else:
            return (-self.small_heap[0] + self.large_heap[0])/2

stream = MedianFinder()
stream.add_num(1)
stream.add_num(2)
print(stream.find_median())
stream.add_num(3)
print(stream.find_median())



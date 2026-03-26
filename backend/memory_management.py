# backend/memory_management.py

import random
from collections import deque, OrderedDict

class PagingSimulator:
    def __init__(self, num_frames, replacement_algo):
        self.num_frames = num_frames
        self.frames = [None] * num_frames  # list representing physical frames
        self.page_faults = 0
        self.total_hits = 0
        self.replacement_algo = replacement_algo
        self.page_history = []  # track page access sequence
        if replacement_algo == "FIFO":
            self.queue = deque()
        elif replacement_algo == "LRU":
            self.lru_order = OrderedDict()
        elif replacement_algo == "Random":
            pass  # Random replacement doesn't require extra structure
        elif replacement_algo == "Optimal":
            self.future_accesses = []  # Store future page accesses for optimal algorithm
            self.remaining_accesses = []  # Track remaining future accesses

    def access_page(self, page):
        self.page_history.append(page)
        if page in self.frames:
            # Page hit: for LRU, update usage
            if self.replacement_algo == "LRU":
                self.lru_order.move_to_end(page)
            self.total_hits += 1
            return False  # No page fault
        else:
            self.page_faults += 1
            self.load_page(page)
            return True   # Page fault occurred

    def load_page(self, page):
        if None in self.frames:
            index = self.frames.index(None)
            self.frames[index] = page
            if self.replacement_algo == "FIFO":
                self.queue.append(index)
            elif self.replacement_algo == "LRU":
                self.lru_order[page] = index
        else:
            if self.replacement_algo == "FIFO":
                index = self.queue.popleft()
                self.frames[index] = page
                self.queue.append(index)
            elif self.replacement_algo == "LRU":
                oldest_page, index = self.lru_order.popitem(last=False)
                self.frames[index] = page
                self.lru_order[page] = index
            elif self.replacement_algo == "Random":
                index = random.randrange(self.num_frames)
                self.frames[index] = page
            elif self.replacement_algo == "Optimal":
                index = self.find_optimal_replacement()
                self.frames[index] = page

    def find_optimal_replacement(self):
        # For each page in frames, find its next use in remaining accesses
        next_use = {}
        for i, page in enumerate(self.frames):
            try:
                # Find the next occurrence of this page in remaining accesses
                next_use[i] = self.remaining_accesses.index(page)
            except ValueError:
                # If the page won't be used again, it's the best candidate
                return i
        
        # If we found next uses for all pages, replace the one with the furthest next use
        if next_use:
            return max(next_use.items(), key=lambda x: x[1])[0]
        
        # If no next uses found (shouldn't happen), replace the first frame
        return 0

    def process_pages(self, pages):
        # For Optimal algorithm, we need to know future accesses
        if self.replacement_algo == "Optimal":
            self.future_accesses = pages.copy()
            self.remaining_accesses = pages.copy()
        
        results = []
        for page in pages:
            if self.replacement_algo == "Optimal":
                # Remove the current page from remaining accesses
                if self.remaining_accesses:
                    self.remaining_accesses.pop(0)
            
            fault = self.access_page(page)
            results.append({
                'page': page,
                'frames': self.frames.copy(),
                'fault': fault,
                'total_faults': self.page_faults,
                'total_hits': self.total_hits
            })
        return results

    def reset(self):
        self.frames = [None] * self.num_frames
        self.page_faults = 0
        self.total_hits = 0
        self.page_history = []
        if self.replacement_algo == "FIFO":
            self.queue.clear()
        elif self.replacement_algo == "LRU":
            self.lru_order.clear()
        elif self.replacement_algo == "Optimal":
            self.future_accesses = []
            self.remaining_accesses = []

class SegmentationSimulator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.segments = []  # List of tuples: (start, size, label)
        self.free_memory = total_memory

    def allocate_segment(self, size, label):
        if size > self.free_memory:
            return False
        start = 0
        if self.segments:
            # Find gap using first-fit strategy
            self.segments.sort(key=lambda x: x[0])
            for seg in self.segments:
                if seg[0] - start >= size:
                    break
                start = seg[0] + seg[1]
            if self.total_memory - start < size:
                return False
        self.segments.append((start, size, label))
        self.free_memory -= size
        return True

    def free_segment(self, label):
        for seg in self.segments:
            if seg[2] == label:
                self.segments.remove(seg)
                self.free_memory += seg[1]
                return True
        return False

    def reset(self):
        self.segments = []
        self.free_memory = self.total_memory

import itertools
import math


class DEQ:
    def __init__(self):
        self.pq = []  # List of entries arranged in a heap
        self.entry_finder = {}  # Mapping of task to entries
        self.counter = itertools.count()  # unique sequence count
        self.REMOVED = '<removed-task>'  # Placeholder for removed task

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        self.heappush(entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_min_task(self, peek_call=False):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = self.heappop_min()
            if task is not self.REMOVED:
                if peek_call:
                    return [priority, count, task]
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def pop_max_task(self, peek_call=False):
        'Remove and return the highest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = self.heappop_max()
            if task is not self.REMOVED:
                if peek_call:
                    return [priority, count, task]
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

    def peek_min_task(self):
        'Take a peek at the lowest priority task. Raise KeyError if empty.'
        if self.pq:
            min_entry = self.pop_min_task(True)
            self.heappush(min_entry)
            return min_entry[2]
        raise KeyError('peek from an empty priority queue')

    def peek_max_task(self):
        'Take a peek at the highest priority task. Raise KeyError if empty.'
        if self.pq:
            max_entry = self.pop_max_task(True)
            self.heappush(max_entry)
            return max_entry[2]
        raise KeyError('peek from an empty priority queue')

    def heappush(self, value):
        'Pushes a given value into the heap'
        element_count = len(self.pq)+1
        level = math.floor(math.log2(element_count))  # Find level
        self.pq.append(value)
        if level % 2 == 0:
            self.heappush_minlevel(element_count-1)
        else:
            self.heappush_maxlevel(element_count-1)

    def heappush_minlevel(self, index):
        'Heapifies a min-leveled element'
        parent = math.ceil(index/2)-1  # Parent index
        if parent >= 0:  # If parent exists
            if self.pq[parent] < self.pq[index]:
                self.pq[parent], self.pq[index] = self.pq[index], self.pq[parent]
                self.maxify_up(parent)
            else:
                self.minify_up(index)

    def heappush_maxlevel(self, index):
        'Heapifies a max-leveled element'
        parent = math.ceil(index/2)-1
        if parent >= 0:
            if self.pq[parent] > self.pq[index]:
                self.pq[parent], self.pq[index] = self.pq[index], self.pq[parent]
                self.minify_up(parent)
            else:
                self.maxify_up(index)

    def minify_up(self, index):
        'sift up for an element in the min level'
        parent = math.ceil(index/2)-1
        grand_parent = math.ceil(parent/2)-1  # Next min level is 2 levels up
        while grand_parent > 0:
            if self.pq[grand_parent] > self.pq[index]:
                self.pq[grand_parent], self.pq[index] = self.pq[index], self.pq[grand_parent]
                parent = math.ceil(grand_parent/2)-1
                grand_parent = math.ceil(parent/2)-1
            else:
                break

    def maxify_up(self, index):
        'sift up for an element in the max level'
        parent = math.ceil(index/2)-1
        grand_parent = math.ceil(parent/2)-1  # Next max level is 2 levels up
        while grand_parent > 0:
            if self.pq[grand_parent] < self.pq[index]:
                self.pq[grand_parent], self.pq[index] = self.pq[index], self.pq[grand_parent]
                parent = math.ceil(grand_parent/2)-1
                grand_parent = math.ceil(parent/2)-1
            else:
                break

    def heappop_min(self):
        'Pop the minimum priority node from the heap'
        self.pq[0], self.pq[len(self.pq)-1] = self.pq[len(self.pq)-1], self.pq[0]
        return_value = self.pq.pop()
        if len(self.pq):
            self.minify_down(0)
        return return_value

    def minify_down(self, index):
        'sift down an element in the min level'
        left_index = 2*index+1
        right_index = 2*index+2
        if not len(self.pq) > 2*(left_index)+1:  # Last min level
            left_child = self.pq[left_index] if left_index < len(self.pq) else [math.inf]
            right_child = self.pq[right_index] if right_index < len(self.pq) else [math.inf]
            elements = (self.pq[index], left_child, right_child)
            min_index = elements.index(min(elements))
            if min_index != 0:
                self.pq[index], self.pq[min_index-1+left_index] = self.pq[min_index-1+left_index], self.pq[index]
        else:  # Next min level is 2 levels down
            gc = [2*left_index+1, 2*left_index+2, 2*right_index+1, 2*right_index+2]
            left_left_child = self.pq[gc[0]] if gc[0] < len(self.pq) else [math.inf]
            left_right_child = self.pq[gc[1]] if gc[1] < len(self.pq) else [math.inf]
            right_left_child = self.pq[gc[2]] if gc[2] < len(self.pq) else [math.inf]
            right_right_child = self.pq[gc[3]] if gc[3] < len(self.pq) else [math.inf]
            elements = (self.pq[index], left_left_child, left_right_child,
                        right_left_child, right_right_child)
            min_index = elements.index(min(elements))
            if min_index != 0:
                self.pq[index], self.pq[gc[min_index-1]] = self.pq[gc[min_index-1]], self.pq[index]
                self.minify_down(gc[min_index-1])

    def heappop_max(self):
        'Pop the maximum priority node from the heap'
        if len(self.pq) == 1:
            return self.pq.pop()
        right = self.pq[2] if 2 < len(self.pq) else [-math.inf]
        elements = ([-math.inf], self.pq[1], right)
        max_index = elements.index(max(elements))
        self.pq[max_index], self.pq[len(self.pq)-1] = self.pq[len(self.pq)-1], self.pq[max_index]
        return_value = self.pq.pop()
        if len(self.pq) > 1 and max_index < len(self.pq):
            self.maxify_down(max_index)
        return return_value

    def maxify_down(self, index):
        'sift down an element in the max level'
        left_index = 2*index+1
        right_index = 2*index+2
        if not len(self.pq) > 2*(left_index)+1:  # Last max level
            left_child = self.pq[left_index] if left_index < len(self.pq) else [-math.inf]
            right_child = self.pq[right_index] if right_index < len(self.pq) else [-math.inf]
            elements = (self.pq[index], left_child, right_child)
            max_index = elements.index(max(elements))
            if max_index != 0:
                self.pq[index], self.pq[max_index-1+left_index] = self.pq[max_index-1+left_index], self.pq[index]
        else:  # Next max level is 2 levels down
            gc = [2*left_index+1, 2*left_index+2, 2*right_index+1, 2*right_index+2]
            left_left_child = self.pq[gc[0]] if gc[0] < len(self.pq) else [math.inf]
            left_right_child = self.pq[gc[1]] if gc[1] < len(self.pq) else [math.inf]
            right_left_child = self.pq[gc[2]] if gc[2] < len(self.pq) else [math.inf]
            right_right_child = self.pq[gc[3]] if gc[3] < len(self.pq) else [math.inf]
            elements = (self.pq[index], left_left_child, left_right_child,
                        right_left_child, right_right_child)
            max_index = elements.index(max(elements))
            if max_index != 0:
                self.pq[index], self.pq[gc[max_index-1]] = self.pq[gc[max_index-1]], self.pq[index]
                self.maxify_down(gc[max_index-1])
                
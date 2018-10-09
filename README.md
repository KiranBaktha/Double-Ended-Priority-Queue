# Double-Ended-Priority-Queue
A min-max heap implementation for a double ended priority queue with sort stability.
Refer to the medium post [link](https://medium.com/@kiranbaktha2002/min-max-heaps-for-double-ended-priority-queue-b8a6b93997fb) for more details on the implementation and running time.

# Usage
<pre>
from depq import DEPQ
queue = DEPQ()
</pre>

## Adding a task with priority
<b>Syntax:</b> queue.add_task(task, priority=0)

<pre>queue.add_task('one', 1)  # Adds a task with priority 1</pre>
<pre>queue.add_task('zero')  # Adds a task with default priority of 0</pre>

<b>Note: </b> Adding an already exisiting task back to the queue updates the priority. <br>
<pre>queue.add_task('one', 7)  # Updates the previous priority of 1 with 7</pre>

## Pop the min priority task
<pre> queue.pop_min_task() </pre>

## Pop the max priority task
<pre> queue.pop_max_task() </pre>

## Peek the min priority task
<pre> queue.peek_min_task() </pre>

## Peek the max priority task
<pre> queue.peek_max_task() </pre>

## Remove a particular task
<pre> queue.remove_task(task) </pre>

## Check if queue is empty

<pre> queue.empty() </pre>

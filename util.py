class Queue:
    "A container with a first-in-first-out queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def lengthLimit(self):
        """ Deque the earliest enqueued item still in the queue. This operation removes
        the item from the queue if there are 200 other entries in teh queue"""
        if len(self.list) >= 200:
            return self.list.pop()

    def itemNotInQueue(self,item):
        if item not in self.list:
            return True 
        return False

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0
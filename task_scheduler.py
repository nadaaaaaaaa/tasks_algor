import random
import time


class Task:
    def __init__(self, name, priority, arrival):
        self.name = name
        self.priority = priority
        self.arrival = arrival

    def __repr__(self):
        return f"{self.name}(p={self.priority}, t={self.arrival})"


def higher(a, b):
    """True if task a is more urgent than task b (ties: earlier arrival wins)."""
    if a.priority != b.priority:
        return a.priority > b.priority
    return a.arrival < b.arrival


class MaxHeap:
    def __init__(self):
        self.items = []

    def insert(self, task):                      
        self.items.append(task)
        i = len(self.items) - 1
        while i > 0:
            parent = (i - 1) // 2
            if higher(self.items[i], self.items[parent]):
                self.items[i], self.items[parent] = self.items[parent], self.items[i]
                i = parent
            else:
                break

    def extract_max(self):                    
        if not self.items:
            return None
        top = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            i = 0
            while True:
                left, right, best = 2 * i + 1, 2 * i + 2, i
                if left < len(self.items) and higher(self.items[left], self.items[best]):
                    best = left
                if right < len(self.items) and higher(self.items[right], self.items[best]):
                    best = right
                if best == i:
                    break
                self.items[i], self.items[best] = self.items[best], self.items[i]
                i = best
        return top

    def is_empty(self):
        return len(self.items) == 0


class SortedListScheduler:
    def __init__(self):
        self.items = []

    def insert(self, task):                 
        self.items.append(task)
        self.items.sort(key=lambda t: (-t.priority, t.arrival))

    def extract_max(self):
        return self.items.pop(0) if self.items else None

    def is_empty(self):
        return len(self.items) == 0


def run_all(scheduler, tasks):
    """Insert every task, then extract everything. Returns the run order."""
    for t in tasks:
        scheduler.insert(t)
    order = []
    while not scheduler.is_empty():
        order.append(scheduler.extract_max())
    return order


def main():
    
    print("=== Example: A(3), B(9), C(5), D(7) ===")
    example = [Task("A", 3, 1), Task("B", 9, 2), Task("C", 5, 3), Task("D", 7, 4)]
    order = run_all(MaxHeap(), example)
    print("Run order:", " -> ".join(t.name for t in order))   # B, D, C, A

    print("\n=== 20 random tasks ===")
    tasks = [Task(f"T{i + 1}", random.randint(1, 100), i + 1) for i in range(20)]
    print("Tasks:", tasks)
    print("\nRun order:")
    for n, t in enumerate(run_all(MaxHeap(), tasks), start=1):
        print(f"  {n:2}. {t}")

    print("\n=== Heap vs sorted list (insert n tasks, then run all) ===")
    for n in [1000, 3000, 5000]:
        big = [Task(f"T{i}", random.randint(1, 10**6), i) for i in range(n)]

        start = time.perf_counter()
        run_all(MaxHeap(), big)
        heap_time = time.perf_counter() - start

        start = time.perf_counter()
        run_all(SortedListScheduler(), big)
        list_time = time.perf_counter() - start

        print(f"n={n:<5} heap: {heap_time:.4f}s   sorted list: {list_time:.4f}s")


if __name__ == "__main__":
    main()

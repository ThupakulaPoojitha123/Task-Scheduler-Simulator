# -*- coding: utf-8 -*-
"""Member 1: Scheduler Server - Priority queue based task scheduling"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import save_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import save_data

import heapq

class Task:
    def __init__(self, task_id, priority, cpu, memory):
        self.task_id = task_id
        self.priority = priority
        self.cpu = cpu
        self.memory = memory
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def to_dict(self):
        return {
            'task_id': self.task_id,
            'priority': self.priority,
            'cpu': self.cpu,
            'memory': self.memory
        }

class Scheduler:
    def __init__(self):
        self.task_queue = []
        self.scheduled_tasks = []
        self.pending_tasks = []
    
    def add_task(self, task):
        heapq.heappush(self.task_queue, task)
    
    def schedule(self, available_cpu, available_memory):
        scheduled = []
        remaining = []
        
        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            if task.cpu <= available_cpu and task.memory <= available_memory:
                available_cpu -= task.cpu
                available_memory -= task.memory
                scheduled.append(task)
                self.scheduled_tasks.append(task)
            else:
                remaining.append(task)
        
        # Put back unscheduled tasks
        for task in remaining:
            heapq.heappush(self.task_queue, task)
            self.pending_tasks.append(task)
        
        return scheduled
    
    def save_state(self):
        state = {
            'scheduled': [t.to_dict() for t in self.scheduled_tasks],
            'pending': [t.to_dict() for t in self.pending_tasks]
        }
        save_data('scheduler.json', state)

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 1: SCHEDULER SERVER")
    print("=" * 50)
    
    scheduler = Scheduler()
    
    # Add sample tasks
    print("\nAdding tasks to queue...")
    n = int(input("Number of tasks to add: "))
    
    for i in range(n):
        print(f"\nTask {i+1}:")
        priority = int(input("  Priority (lower = higher priority): "))
        cpu = int(input("  CPU cores: "))
        memory = int(input("  Memory (MB): "))
        scheduler.add_task(Task(f"T{i+1}", priority, cpu, memory))
        print(f"  Task T{i+1} added")
    
    print(f"\n{n} tasks in queue")
    
    # Schedule tasks
    print("\n" + "=" * 50)
    print("SCHEDULING TASKS")
    cpu = int(input("Available CPU cores: "))
    mem = int(input("Available Memory (MB): "))
    
    scheduled = scheduler.schedule(cpu, mem)
    
    print(f"\nScheduled {len(scheduled)} tasks:")
    for task in scheduled:
        print(f"  {task.task_id}: Priority={task.priority}, CPU={task.cpu}, Memory={task.memory}")
    
    if scheduler.task_queue:
        print(f"\n{len(scheduler.task_queue)} tasks pending (insufficient resources)")
    
    scheduler.save_state()
    print(f"\nScheduler state saved")
    print("Member 2 can now allocate resources")
    print("Member 3 can monitor metrics")
    
    input("\nPress Enter to exit...")

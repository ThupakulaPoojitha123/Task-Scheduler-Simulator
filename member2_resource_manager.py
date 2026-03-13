# -*- coding: utf-8 -*-
"""Member 2: Resource Manager - Bin packing allocation"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import load_data, save_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import load_data, save_data

class Node:
    def __init__(self, node_id, cpu, memory):
        self.node_id = node_id
        self.total_cpu = cpu
        self.total_memory = memory
        self.available_cpu = cpu
        self.available_memory = memory
        self.tasks = []
    
    def can_fit(self, cpu, memory):
        return self.available_cpu >= cpu and self.available_memory >= memory
    
    def allocate(self, task_id, cpu, memory):
        self.available_cpu -= cpu
        self.available_memory -= memory
        self.tasks.append(task_id)
    
    def to_dict(self):
        return {
            'node_id': self.node_id,
            'total_cpu': self.total_cpu,
            'total_memory': self.total_memory,
            'available_cpu': self.available_cpu,
            'available_memory': self.available_memory,
            'tasks': self.tasks
        }

class ResourceManager:
    def __init__(self):
        self.nodes = []
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def allocate_tasks(self, tasks):
        allocations = []
        failed = []
        
        for task in tasks:
            allocated = False
            for node in self.nodes:
                if node.can_fit(task['cpu'], task['memory']):
                    node.allocate(task['task_id'], task['cpu'], task['memory'])
                    allocations.append({
                        'task_id': task['task_id'],
                        'node_id': node.node_id
                    })
                    allocated = True
                    break
            
            if not allocated:
                failed.append(task['task_id'])
        
        return allocations, failed
    
    def save_state(self):
        state = {
            'nodes': [n.to_dict() for n in self.nodes]
        }
        save_data('resource_manager.json', state)

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 2: RESOURCE MANAGER")
    print("=" * 50)
    
    rm = ResourceManager()
    
    # Create nodes
    print("\nSetting up compute nodes...")
    n = int(input("Number of nodes: "))
    for i in range(n):
        cpu = int(input(f"Node {i+1} CPU cores: "))
        mem = int(input(f"Node {i+1} Memory (MB): "))
        rm.add_node(Node(f"N{i+1}", cpu, mem))
        print(f"  Node N{i+1} created")
    
    # Load scheduled tasks from Member 1
    scheduler_data = load_data('scheduler.json')
    
    if scheduler_data and 'scheduled' in scheduler_data:
        tasks = scheduler_data['scheduled']
        print(f"\nLoaded {len(tasks)} scheduled tasks from Member 1")
        
        print("\n" + "=" * 50)
        print("ALLOCATING TASKS TO NODES")
        
        allocations, failed = rm.allocate_tasks(tasks)
        
        print(f"\nSuccessfully allocated {len(allocations)} tasks:")
        for alloc in allocations:
            print(f"  {alloc['task_id']} -> {alloc['node_id']}")
        
        if failed:
            print(f"\nFailed to allocate {len(failed)} tasks: {failed}")
        
        # Display node status
        print(f"\nNODE STATUS:")
        for node in rm.nodes:
            cpu_used = node.total_cpu - node.available_cpu
            mem_used = node.total_memory - node.available_memory
            print(f"\n  {node.node_id}:")
            print(f"    CPU: {cpu_used}/{node.total_cpu} cores")
            print(f"    Memory: {mem_used}/{node.total_memory} MB")
            print(f"    Tasks: {node.tasks}")
        
        rm.save_state()
        print(f"\nResource allocation saved")
        print("Member 3 can now monitor metrics")
    else:
        print("\nERROR: No scheduled tasks found!")
        print("Please run Member 1 (Scheduler) first.")
    
    input("\nPress Enter to exit...")

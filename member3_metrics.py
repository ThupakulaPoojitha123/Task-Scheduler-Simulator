# -*- coding: utf-8 -*-
"""Member 3: Metrics Client - Monitoring dashboard"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from shared_utils import load_data, save_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared_utils import load_data, save_data

from collections import defaultdict
import time

class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.load_metrics()
    
    def record(self, metric_name, value):
        self.metrics[metric_name].append({
            'value': value,
            'timestamp': time.time()
        })
        self.save_metrics()
    
    def get_avg(self, metric_name):
        if metric_name not in self.metrics:
            return 0
        values = [m['value'] for m in self.metrics[metric_name]]
        return sum(values) / len(values)
    
    def get_max(self, metric_name):
        if metric_name not in self.metrics:
            return 0
        return max(m['value'] for m in self.metrics[metric_name])
    
    def get_min(self, metric_name):
        if metric_name not in self.metrics:
            return 0
        return min(m['value'] for m in self.metrics[metric_name])
    
    def display_dashboard(self):
        print("\n" + "=" * 50)
        print("   METRICS DASHBOARD")
        print("=" * 50)
        
        # Load system data
        scheduler_data = load_data('scheduler.json')
        resource_data = load_data('resource_manager.json')
        
        if scheduler_data:
            print(f"\nSCHEDULER METRICS:")
            print(f"   Scheduled Tasks: {len(scheduler_data.get('scheduled', []))}")
            print(f"   Pending Tasks: {len(scheduler_data.get('pending', []))}")
        
        if resource_data:
            nodes = resource_data.get('nodes', [])
            print(f"\nRESOURCE METRICS:")
            print(f"   Total Nodes: {len(nodes)}")
            
            total_cpu = sum(n['total_cpu'] for n in nodes)
            used_cpu = sum(n['total_cpu'] - n['available_cpu'] for n in nodes)
            total_mem = sum(n['total_memory'] for n in nodes)
            used_mem = sum(n['total_memory'] - n['available_memory'] for n in nodes)
            
            print(f"   CPU Usage: {used_cpu}/{total_cpu} cores ({used_cpu/total_cpu*100:.1f}%)")
            print(f"   Memory Usage: {used_mem}/{total_mem} MB ({used_mem/total_mem*100:.1f}%)")
        
        if self.metrics:
            print(f"\nCUSTOM METRICS:")
            for metric, data in self.metrics.items():
                print(f"\n   {metric}:")
                print(f"     Count: {len(data)}")
                print(f"     Avg: {self.get_avg(metric):.2f}")
                print(f"     Min: {self.get_min(metric):.2f}")
                print(f"     Max: {self.get_max(metric):.2f}")
    
    def save_metrics(self):
        save_data('metrics.json', dict(self.metrics))
    
    def load_metrics(self):
        data = load_data('metrics.json')
        if data:
            self.metrics = defaultdict(list, data)

if __name__ == "__main__":
    print("=" * 50)
    print("   MEMBER 3: METRICS CLIENT")
    print("=" * 50)
    
    collector = MetricsCollector()
    print("\nMetrics collector started")
    
    while True:
        print("\n" + "=" * 50)
        print("COMMANDS: RECORD | DASHBOARD | CLEAR | QUIT")
        cmd = input("Enter command: ").strip().upper()
        
        if cmd == "RECORD":
            metric = input("Metric name (e.g., cpu_usage, latency): ")
            value = float(input("Value: "))
            collector.record(metric, value)
            print(f"Recorded {metric} = {value}")
            
        elif cmd == "DASHBOARD":
            collector.display_dashboard()
            
        elif cmd == "CLEAR":
            collector.metrics.clear()
            collector.save_metrics()
            print("Metrics cleared")
            
        elif cmd == "QUIT":
            break
    
    print("\nMetrics client closed.")

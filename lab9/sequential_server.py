import time
from typing import List, Tuple, Dict
from user_request import UserRequest
from cpu_manager import cpu_manager, CPU_MANAGER_ENABLE


def sequential_simulation(requests: List[UserRequest]) -> Tuple[float, float, Dict]:
    if CPU_MANAGER_ENABLE:
        cpu_manager.reset()
    total_cpu = 0.0
    start_time = time.time()

    for request in requests:
        result = request.process_request()
        total_cpu += result.cpu_load
        print(f"User {result.user_id}: action {result.action_type}, "
              f"time: {result.processing_time:.3f}s, CPU: {result.cpu_load*100:.1f}%")

    total_time = time.time() - start_time
    avg_cpu = total_cpu / len(requests)

    print(f"\nSequential - Total time: {total_time:.3f}s, "
          f"Avg CPU: {avg_cpu*100:.1f}%")

    return total_time, avg_cpu, cpu_manager.get_stats()

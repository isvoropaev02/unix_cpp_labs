from typing import List, Tuple
from user_request import UserRequest, RequestResult
import time


def sequential_simulation(requests: List[UserRequest]) -> Tuple[float, float]:

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

    return total_time, avg_cpu

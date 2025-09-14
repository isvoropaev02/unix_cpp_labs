from typing import List, Tuple
from user_request import UserRequest, RequestResult
import time
import multiprocessing as mp


def process_worker(request: UserRequest) -> RequestResult:
    result = request.process_request()
    print(f"User {result.user_id}: action {result.action_type}, "
          f"time: {result.processing_time:.3f}s, CPU: {result.cpu_load*100:.1f}%")
    return result

def multiprocess_simulation(requests: List[UserRequest], num_proc: int = 4) -> Tuple[float, float]:
    start_time = time.time()
    
    with mp.Pool(processes=num_proc) as pool:
        results = pool.map(process_worker, requests)
    
    total_time = time.time() - start_time
    total_cpu = sum(result.cpu_load for result in results)
    avg_cpu = total_cpu / len(results)
    
    print(f"\nMultiprocess - Total time: {total_time:.3f}s, "
          f"Avg CPU: {avg_cpu*100:.1f}%")
    
    return total_time, avg_cpu
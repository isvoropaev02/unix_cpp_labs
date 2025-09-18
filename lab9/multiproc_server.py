import time
import multiprocessing as mp
from typing import List, Tuple, Dict
from user_request import UserRequest, RequestResult
from cpu_manager import cpu_manager, CPU_MANAGER_ENABLE, NUM_WORKERS


def process_worker(request: UserRequest) -> RequestResult:
    result = request.process_request()
    print(
        f"User {result.user_id}: action {result.action_type}, "
        f"time: {result.processing_time:.3f}s, CPU: {result.cpu_load*100:.1f}%"
    )
    return result


def multiprocess_simulation(
    requests: List[UserRequest], num_proc: int = NUM_WORKERS
) -> Tuple[float, Dict]:
    if CPU_MANAGER_ENABLE:
        cpu_manager.reset()
    start_time = time.time()

    with mp.Pool(processes=num_proc) as pool:
        _ = pool.map(process_worker, requests)

    total_time = time.time() - start_time
    print(f"\nMultiprocess - Total time: {total_time:.3f}s")
    return total_time, cpu_manager.get_stats()

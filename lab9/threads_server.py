import threading
import time
from typing import List, Tuple, Dict
from user_request import UserRequest, RequestResult
from queue import Queue
from cpu_manager import cpu_manager, CPU_MANAGER_ENABLE


def thread_worker(queue: Queue[UserRequest], results: List[RequestResult]):
    while not queue.empty():
        try:
            request = queue.get_nowait()
            result = request.process_request()
            results.append(result)
            queue.task_done()
            print(f"User {result.user_id}: action {result.action_type}, "
                  f"time: {result.processing_time:.3f}s, CPU: {result.cpu_load*100:.1f}%")
        except:
            break


def threaded_simulation(requests: List[UserRequest], num_threads: int = 4) -> Tuple[float, float, Dict]:
    if CPU_MANAGER_ENABLE:
        cpu_manager.reset()
    queue = Queue()

    for request in requests:
        queue.put(request)

    results = []
    threads = []
    start_time = time.time()

    for _ in range(num_threads):
        thread = threading.Thread(target=thread_worker, args=(queue, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    total_cpu = sum(result.cpu_load for result in results)
    avg_cpu = total_cpu / len(results)

    print(f"\nThreaded - Total time: {total_time:.3f}s, "
          f"Avg CPU: {avg_cpu*100:.1f}%")

    return total_time, avg_cpu, cpu_manager.get_stats()

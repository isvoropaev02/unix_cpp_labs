
import time
import asyncio
from typing import List, Tuple, Dict
from user_request import UserRequest
from cpu_manager import cpu_manager, CPU_MANAGER_ENABLE

async def asyncio_simulation(requests: List[UserRequest]) -> Tuple[float, float, Dict]:
    if CPU_MANAGER_ENABLE:
        cpu_manager.reset()
    tasks = [request.process_request_async() for request in requests]
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    total_cpu = sum(result.cpu_load for result in results)
    avg_cpu = total_cpu / len(results)
    
    for result in results:
        print(f"User {result.user_id}: action {result.action_type}, "
              f"time: {result.processing_time:.3f}s, CPU: {result.cpu_load*100:.1f}%")
    
    print(f"\nAsyncio - Total time: {total_time:.3f}s, "
          f"Avg CPU: {avg_cpu*100:.1f}%")
    
    return total_time, avg_cpu, cpu_manager.get_stats()
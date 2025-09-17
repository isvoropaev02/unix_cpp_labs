import time
import asyncio
from dataclasses import dataclass
from typing import List
from random import shuffle
from cpu_manager import cpu_manager
from sim_params import *


@dataclass
class RequestResult:
    user_id: int
    action_type: int
    cpu_load: float
    processing_time: float


class UserRequest:
    def __init__(self, user_id: int, action_type: int, ):
        self.user_id = user_id
        self.action_type = action_type
        self.required_cpu = self._get_cpu_load()
        self.processing_time = self._get_processing_time()
    
    def _get_cpu_load(self) -> float:
        loads = {1: C1, 2: C2, 3: C3}
        return loads.get(self.action_type, 0)
    
    def _get_processing_time(self) -> float:
        times = {1: T1, 2: T2, 3: T3}
        return times.get(self.action_type, 0)

    def process_request(self) -> RequestResult:
        start_time = time.time()
        if CPU_MANAGER_ENABLE:
            cpu_manager.wait_for_resource(self.required_cpu)
        time.sleep(self.processing_time)
        processing_time = time.time() - start_time
        if CPU_MANAGER_ENABLE:
            cpu_manager.release(self.required_cpu)
        return RequestResult(self.user_id, self.action_type, self.required_cpu, processing_time)
    
    async def process_request_async(self) -> RequestResult:
        start_time = time.time()
        
        # Имитация асинхронной обработки
        if self.action_type == 1:
            await asyncio.sleep(0.5)
            cpu_load = 0.25
        elif self.action_type == 2:
            await asyncio.sleep(0.3)
            cpu_load = 0.15
        elif self.action_type == 3:
            await asyncio.sleep(0.1)
            cpu_load = 0.01
        else:
            cpu_load = 0.0
        
        processing_time = time.time() - start_time
        return RequestResult(self.user_id, self.action_type, cpu_load, processing_time)


def create_requests(U1: int, U2: int, U3: int) -> List[UserRequest]:
    requests = []
    user_id = 0

    for _ in range(U1):
        requests.append(UserRequest(user_id, 1))
        user_id += 1

    for _ in range(U2):
        requests.append(UserRequest(user_id, 2))
        user_id += 1

    for _ in range(U3):
        requests.append(UserRequest(user_id, 3))
        user_id += 1
    shuffle(requests)
    return requests

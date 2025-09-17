import time
from dataclasses import dataclass
from typing import List
from random import shuffle
import asyncio

T1 = 0.5  # Registration
T2 = 0.3  # Get main page
T3 = 0.1  # Get active users


@dataclass
class RequestResult:
    user_id: int
    action_type: int
    cpu_load: float
    processing_time: float


class UserRequest:
    def __init__(self, user_id: int, action_type: int):
        self.user_id = user_id
        self.action_type = action_type

    def process_request(self) -> RequestResult:
        start_time = time.time()

        # Имитация обработки запроса
        if self.action_type == 1:
            time.sleep(T1)
            cpu_load = 0.25
        elif self.action_type == 2:
            time.sleep(T2)
            cpu_load = 0.15
        elif self.action_type == 3:
            time.sleep(T3)
            cpu_load = 0.01
        else:
            cpu_load = 0.0

        processing_time = time.time() - start_time
        return RequestResult(self.user_id, self.action_type, cpu_load, processing_time)
    
    async def process_async(self) -> RequestResult:
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

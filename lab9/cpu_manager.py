import time
import threading
from dataclasses import dataclass
from typing import List, Dict
from sim_params import *

@dataclass
class CpuManager:
    current_load: float
    max_load: float
    load_history: List[float]
    timestamps: List[float]
    lock: threading.Lock
    max_capacity: float = MAX_CAPACITY
    
    def __init__(self) -> None:
        self.current_load = 0.0
        self.max_load = 0.0
        self.load_history = []
        self.timestamps = []
        self.lock = threading.Lock()
        self.start_time = time.time()
        self._record()
    
    def acquire(self, required_cpu: float) -> bool:
        """Добавить нагрузку"""
        with self.lock:
            if self.current_load + required_cpu <= self.max_capacity:
                self.current_load += required_cpu
                self.max_load = max(self.max_load, self.current_load)
                self._record()
                return True
            return False
    
    def release(self, load: float) -> None:
        """Убрать нагрузку"""
        with self.lock:
            self.current_load -= load
            if self.current_load < 0:
                self.current_load = 0
            self._record()

    def wait_for_resource(self, required_cpu: float) -> None:
        """Ждать пока не освободится достаточно ресурсов"""
        while True:
            with self.lock:
                if self.acquire(required_cpu):
                    return
            # Ждем немного перед повторной проверкой
            time.sleep(T_WAIT)
    
    def _record(self) -> None:
        """Записать текущее состояние"""
        current_time = time.time() - self.start_time
        self.load_history.append(self.current_load)
        self.timestamps.append(current_time)

    def reset(self) -> None:
        self.__init__()
    
    def get_stats(self) -> Dict:
        """Получить статистику"""
        with self.lock:
            avg_load = sum(self.load_history) / len(self.load_history) if self.load_history else 0
            return {
                'max': self.max_load,
                'avg': avg_load,
                'history': self.load_history.copy(),
                'timestamps': self.timestamps.copy()}

cpu_manager = CpuManager()
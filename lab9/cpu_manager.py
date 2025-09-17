import time
import threading
from dataclasses import dataclass
from typing import List

@dataclass
class CpuManager:
    current_load: float
    max_load: float
    load_history: List[float]
    timestamps: List[float]
    lock: threading.Lock
    max_capacity: float = 1.0
    
    def __init__(self):
        self.current_load = 0.0
        self.max_load = 0.0
        self.load_history = []
        self.timestamps = []
        self.lock = threading.Lock()
        self.start_time = time.time()
    
    def acquire(self, required_cpu: float):
        """Добавить нагрузку"""
        with self.lock:
            if self.current_load + required_cpu <= self.max_capacity:
                self.current_load += required_cpu
                self.max_load = max(self.max_load, self.current_load)
                self._record()
                return True
            self._record()
            return False
    
    def release(self, load: float):
        """Убрать нагрузку"""
        with self.lock:
            self.current_load -= load
            if self.current_load < 0:
                self.current_load = 0
            self._record()

    def wait_for_resource(self, required_cpu: float):
        """Ждать пока не освободится достаточно ресурсов"""
        while True:
            with self.lock:
                if self.current_usage + required_cpu <= self.max_capacity:
                    self.current_usage += required_cpu
                    return
            # Ждем немного перед повторной проверкой
            time.sleep(0.01)
    
    def _record(self):
        """Записать текущее состояние"""
        current_time = time.time() - self.start_time
        self.load_history.append(self.current_load)
        self.timestamps.append(current_time)
    
    def get_stats(self):
        """Получить статистику"""
        with self.lock:
            avg_load = sum(self.load_history) / len(self.load_history) if self.load_history else 0
            return {
                'max': self.max_load,
                'avg': avg_load,
                'history': self.load_history.copy(),
                'timestamps': self.timestamps.copy()
            }

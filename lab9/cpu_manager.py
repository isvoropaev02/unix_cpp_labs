import time
import threading
import matplotlib.pyplot as plt
import numpy as np
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

    def _get_avg_load(self) -> float:
        if len(self.timestamps) == 1:
            return 0.0
        integral = 0
        for i in range(0, len(self.load_history) - 1):
            integral += self.load_history[i] * (
                self.timestamps[i + 1] - self.timestamps[i]
            )
        return integral / self.timestamps[-1]

    def get_stats(self) -> Dict:
        """Получить статистику"""
        with self.lock:
            avg_load = self._get_avg_load()
            return {
                "max": self.max_load,
                "avg": avg_load,
                "history": self.load_history.copy(),
                "timestamps": self.timestamps.copy(),
            }


cpu_manager = CpuManager()


def visualize_cpu_usage(
    seq_cpu_report: Dict,
    mp_cpu_report: Dict,
    thread_cpu_report: Dict,
    asyncio_cpu_report: Dict,
) -> None:
    fig1 = plt.figure(figsize=(13, 8))

    plt.subplot(4, 1, 1)
    plt.step(
        seq_cpu_report["timestamps"],
        np.array(seq_cpu_report["history"]) * 100,
        label="Sequential",
        color="C0",
        where="post",
    )
    plt.legend()
    plt.ylabel(
        f"CPU usage [%]\nMax value: {seq_cpu_report["max"]:.2f}\nAvg value: {seq_cpu_report["avg"]:.2f}",
        rotation=0,
    )
    plt.grid()
    plt.gca().yaxis.set_label_coords(-0.10, 0.5)

    plt.subplot(4, 1, 2)
    plt.step(
        mp_cpu_report["timestamps"],
        np.array(mp_cpu_report["history"]) * 100,
        label="Multiprocess",
        color="C1",
        where="post",
    )
    plt.legend()
    plt.ylabel(
        f"CPU usage [%]\nMax value: {mp_cpu_report["max"]:.2f}\nAvg value: {mp_cpu_report["avg"]:.2f}",
        rotation=0,
    )
    plt.grid()
    plt.gca().yaxis.set_label_coords(-0.10, 0.5)

    plt.subplot(4, 1, 3)
    plt.step(
        thread_cpu_report["timestamps"],
        np.array(thread_cpu_report["history"]) * 100,
        label="Threaded",
        color="C2",
        where="post",
    )
    plt.legend()
    plt.ylabel(
        f"CPU usage [%]\nMax value: {thread_cpu_report["max"]:.2f}\nAvg value: {thread_cpu_report["avg"]:.2f}",
        rotation=0,
    )
    plt.grid()
    plt.gca().yaxis.set_label_coords(-0.10, 0.5)

    plt.subplot(4, 1, 4)
    plt.step(
        asyncio_cpu_report["timestamps"],
        np.array(asyncio_cpu_report["history"]) * 100,
        label="Async",
        color="C3",
        where="post",
    )
    plt.ylabel(
        f"CPU usage [%]\nMax value: {asyncio_cpu_report["max"]:.2f}\nAvg value: {asyncio_cpu_report["avg"]:.2f}",
        rotation=0,
    )
    plt.grid()
    plt.gca().yaxis.set_label_coords(-0.10, 0.5)
    plt.xlabel("Time [s]")
    plt.legend()
    plt.suptitle("CPU usage history")
    fig1.savefig("lab9/cpu_report.png", transparent=False)

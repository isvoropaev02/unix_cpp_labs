from sequential_server import sequential_simulation
from threads_server import threaded_simulation
from multiproc_server import multiprocess_simulation
from async_server import asyncio_simulation
from cpu_manager import visualize_cpu_usage
from sim_params import SEED, CPU_MANAGER_ENABLE
from user_request import *
from random import shuffle, seed


def main():
    seed(SEED)
    requests = create_requests(U1=U1, U2=U2, U3=U3)
    print("=== Sequential Simulation ===")
    seq_time, seq_cpu = sequential_simulation(requests=requests)

    print("\n=== Multiprocess Simulation ===")
    mp_time, mp_cpu = multiprocess_simulation(requests=requests)

    print("\n=== Threaded Simulation ===")
    thread_time, thread_cpu = threaded_simulation(requests=requests)

    print("\n=== Asyncio Simulation ===")
    asyncio_time, asyncio_cpu = asyncio.run(asyncio_simulation(requests=requests))

    # Сравнение результатов
    print("\n" + "=" * 50)
    print("COMPARISON RESULTS:")
    print("=" * 50)
    print(f"{'Method':<12} {'Time (s)':<10} {'Avg CPU (%)':<12}")
    print("-" * 50)
    print(f"{'Sequential':<12} {seq_time:<10.3f} {seq_cpu["avg"]*100:<12.1f}")
    print(f"{'Multiprocess':<12} {mp_time:<10.3f} {mp_cpu["avg"]*100:<12.1f}")
    print(f"{'Threaded':<12} {thread_time:<10.3f} {thread_cpu["avg"]*100:<12.1f}")
    print(f"{'Asyncio':<12} {asyncio_time:<10.3f} {asyncio_cpu["avg"]*100:<12.1f}")

    if CPU_MANAGER_ENABLE:
        visualize_cpu_usage(
            seq_cpu_report=seq_cpu,
            mp_cpu_report=mp_cpu,
            thread_cpu_report=thread_cpu,
            asyncio_cpu_report=asyncio_cpu,
        )


if __name__ == "__main__":
    main()

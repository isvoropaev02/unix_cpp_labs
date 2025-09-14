from sequential_server import sequential_simulation
from threads_server import threaded_simulation
from user_request import *
from random import shuffle

U1 = 3
U2 = 5
U3 = 10


def main():
    requests = create_requests(U1=U1, U2=U2, U3=U3)
    print("=== Sequential Simulation ===")
    seq_time, seq_cpu = sequential_simulation(requests=requests)

    # print("\n=== Multiprocess Simulation ===")
    # mp_time, mp_cpu = multiprocess_simulation(U1, U2, U3)

    print("\n=== Threaded Simulation ===")
    thread_time, thread_cpu = threaded_simulation(requests=requests)

    # print("\n=== Asyncio Simulation ===")
    # asyncio_time, asyncio_cpu = asyncio.run(asyncio_simulation(U1, U2, U3))

    # Сравнение результатов
    print("\n" + "="*50)
    print("COMPARISON RESULTS:")
    print("="*50)
    print(f"{'Method':<12} {'Time (s)':<10} {'Avg CPU (%)':<12}")
    print("-" * 50)
    print(f"{'Sequential':<12} {seq_time:<10.3f} {seq_cpu*100:<12.1f}")
    # print(f"{'Multiprocess':<12} {mp_time:<10.3f} {mp_cpu*100:<12.1f}")
    print(f"{'Threaded':<12} {thread_time:<10.3f} {thread_cpu*100:<12.1f}")
    # print(f"{'Asyncio':<12} {asyncio_time:<10.3f} {asyncio_cpu*100:<12.1f}")


if __name__ == "__main__":
    main()

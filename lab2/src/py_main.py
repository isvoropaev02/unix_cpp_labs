from  timeit import timeit
from random import random

def measure_time(x, num_loops):
    time = timeit(stmt='x ** 2 - x ** 2 + x * 4 - x * 5 + x + x',
                  globals={'x': x}, number=num_loops)
    return time

def main():
    time_list = list()
    ans = "y"
    while ans == "y":
        try:
            num_loops = int(input("Input number of loops: "))
        except ValueError:
            print("Input should be a number")
            break
        x = random()
        time = measure_time(x, num_loops)
        time_list.append(time)
        print(f"{time*1e6} us spent on {num_loops} loops")
        ans = str(input("Do you wish to continue? [y/n]: "))
    print(time_list)
    return 0

if __name__ == "__main__":
    main()
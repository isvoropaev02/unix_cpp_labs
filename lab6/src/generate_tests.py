from random import uniform, seed, randint

seed(0)
FILE_PATH = "lab6/src/input.txt"

def gen_tests_task1(n_samples=10000):
    return [str(round(uniform(-1, 1), 3)) for _ in range(n_samples)]

def gen_tests_task2(n_samples=128):
    arr = [str(i) for i in range(n_samples)]
    for i in range(len(arr)):  
        p = uniform(0,1)
        if p>0.98:
            swap_id = randint(1, n_samples) % n_samples
            arr[i], arr[swap_id] = arr[swap_id], arr[i] # swap
    return arr

if __name__ == "__main__":
    arr = gen_tests_task1(10000)

    with open(FILE_PATH, "w") as file:
        file.write(str(len(arr))+"\n")
        file.write("\n".join(arr))
    print(" ".join(arr[:5]))
    

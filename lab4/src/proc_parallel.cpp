#include <iostream>
#include <random>
#include <vector>
#include <ctime>
#include <unistd.h>
#include <sys/wait.h>

inline double formula1(const double x) { return x * x - x * x + x * 4 - x * 5 + x + x; }

inline double formula2(const double x) { return x + x; }

double measure_time(double x, size_t num_loops)
{
    std::vector<double> val1(num_loops);
    std::vector<double> val2(num_loops);
    [[maybe_unused]] double val3;

    clock_t time_start = clock();

    int fd1[2], fd2[2];
    int result1{pipe(fd1)}, result2{pipe(fd2)};
    if (result1 == -1 || result2 == -1)
    {
        std::cout << "[ERROR] Pipes are not created\n";
        exit(1);
    }

    pid_t pid1 = fork();
    if (pid1 < 0)
    {
        std::cout << "[ERROR] fork error for proc. 1\n";
        exit(2);
    }
    else if (pid1 == 0) // child proc.
    {
        for (size_t i = 0; i < num_loops; i++)
        {
            close(fd2[0]); // no reading&writting for proc. 2
            close(fd2[1]);
            close(fd1[0]); // no reading for current pipe
            close(fd1[1]);
            val1[i] = formula1(x);
        }
        exit(0);
    }
    

    pid_t pid2 = fork();
    if (pid2 < 0)
    {
        std::cout << "[ERROR] fork error for proc. 1\n";
        exit(2);
    }
    else if (pid2 == 0) // child proc.
    {
        for (size_t i = 0; i < num_loops; i++)
        {
            close(fd2[0]); // no reading&writting for proc. 2
            close(fd2[1]);
            close(fd1[0]); // no reading for current pipe
            close(fd1[1]);
            val2[i] = formula2(x);
        }
        exit(0);
    }


    clock_t time_end = clock();
    return (double(time_end - time_start) / CLOCKS_PER_SEC);
}

int main()
{
    // random gen config
    std::random_device rd;  // Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dis(0.0, 1.0);

    double x = dis(gen);
    size_t num_loops1{10000}, num_loops2{100000};
    double time1 = measure_time(x, num_loops1);
    std::cout << time1*1e6 << " us spent on " << num_loops1 << " loops" << "\n";
    double time2 = measure_time(x, num_loops2);
    std::cout << time2*1e6 << " us spent on " << num_loops2 << " loops" << "\n";
    return 0;
}
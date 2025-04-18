#include <iostream>
#include <random>
#include <vector>
#include <ctime>
#include <unistd.h>
#include <sys/wait.h>

#define READ_END	0
#define WRITE_END	1

inline double formula1(const double x) { return x * x - x * x + x * 4 - x * 5 + x + x; }

inline double formula2(const double x) { return x + x; }

int main()
{
    // random gen config
    std::random_device rd;  // Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dis(0.0, 1.0);
    double x = dis(gen);
    size_t num_loops{10000};

    clock_t time_start = clock();

    int fd1[2], fd2[2];
    int result1{pipe(fd1)}, result2{pipe(fd2)};
    if (result1 == -1 || result2 == -1) {
        std::cout << "[ERROR] Failed to create pipes.\n";
        exit(1);
    }
    pid_t pid1 = fork();
    if (pid1 == -1) {
        std::cout << "[ERROR] Failed in creating proc. with fork().\n";
        // return 1;
        exit(1);
    } else if (pid1 == 0) {
        // First child process
        
        close(fd1[0]); // Close read end of pipe 1
        close(fd2[0]); // Close read end of pipe 2
        close(fd2[1]); // Close write end of pipe 2
        float calc_1[num_loops];
        for (int i = 0; i < num_loops; i++) {
            calc_1[i] = formula1(x);
            // std::cout << "p1\n";
        }
        write(fd1[1], calc_1, sizeof(calc_1)); // Write result to pipe 1
        close(fd1[1]); // Close write end of pipe 1
        // return 0;
        exit(0);
    }
    pid_t pid2 = fork();
    if (pid2 == -1) {
        std::cout << "[ERROR] Failed in creating proc. with fork().\n";
        // return 1;
        exit(1);
    } else if (pid2 == 0) {
        // Second child process
        close(fd2[0]); // Close read end of pipe 2
        close(fd1[0]); // Close read end of pipe 1
        close(fd2[1]); // Close write end of pipe 2
        float calc_2[num_loops];
        for (int i = 0; i < num_loops; i++) {
            calc_2[i] = formula2(x);
            // std::cout << "p2\n";
        }
        write(fd2[1], calc_2, sizeof(calc_2)); // Write result to pipe 2
        close(fd2[1]); // Close write end of pipe 2
        // return 0;
        exit(0);
    }

    // Wait for child processes to exit
    int status;
    waitpid(pid1, &status, 0);
    waitpid(pid2, &status, 0);
    // Parent process
    close(fd1[0]); // Close read end of pipe 1
    close(fd1[1]); // Close write end of pipe 1
    close(fd2[1]); // Close write end of pipe 2
    float  calc_3;
    float calc_2[num_loops];
    read(fd2[0], calc_2, sizeof(calc_2)); // Read result from pipe 2
    float calc_1[num_loops];
    read(fd1[0], calc_1, sizeof(calc_1)); // Read result from pipe 1
    for (int i = 0; i < num_loops; i++) {
        calc_3 = calc_1[i] + calc_2[i] - calc_1[i];
    }

    clock_t time_end = clock();
    double time = (double(time_end - time_start) / CLOCKS_PER_SEC);
    std::cout << time*1e6 << " us spent on " << num_loops << " loops" << "\n";
    return 0;
}
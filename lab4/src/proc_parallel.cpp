#include <iostream>
#include <random>
#include <vector>
#include <ctime>
#include <unistd.h>
#include <sys/wait.h>

#define READ_END    0
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
    size_t num_loops{100000};

    clock_t time_start = clock();

    int fd1[2];
    int result1{pipe(fd1)};
    if (result1 == -1) {
        std::cout << "[ERROR] Failed to create pipe-channel.\n";
        return 1;
    }
    pid_t pid1 = fork();
    if (pid1 == -1) {
        std::cout << "[ERROR] Failed in creating proc. with fork().\n";
        return 1;
    }
    else if (pid1 == 0)
    {   // child process
        close(fd1[READ_END]); // Close read end of pipe 1
        std::vector<double> val1(num_loops);
        for (int i = 0; i < num_loops; i++) {
            val1[i] = formula1(x);
            // std::cout << "Child Process (PID: " << getpid() << ") val1: " << val1[i] <<"\n";
        }
        write(fd1[WRITE_END], val1.data(), val1.size()*sizeof(double)); // Write result to pipe 1
        close(fd1[WRITE_END]); // Close write end of pipe 1
        exit(0);
    }
    else
    {   // parrent process
        close(fd1[WRITE_END]);
        double val3;
        std::vector<double> val1(num_loops);
        std::vector<double> val2(num_loops);
        for (int i = 0; i < num_loops; i++) {
            val2[i] = formula2(x);
            // std::cout << "Child Process (PID: " << getpid() << ") val2:" << val2[i] <<"\n";
        }
        
        read(fd1[READ_END], val1.data(), val1.size()*sizeof(double)); // Read result from pipe
        close(fd1[READ_END]);
        for (int i = 0; i < num_loops; i++) {
            val3 = val1[i] + val2[i] - val1[i];
            // std::cout << "Child Process (PID: " << getpid() << ") val3: " << val3 <<"\n";
        }
        // Wait for child processes to exit
        waitpid(pid1, nullptr, 0);
    }
    clock_t time_end = clock();
    double time = (double(time_end - time_start) / CLOCKS_PER_SEC);
    std::cout << time*1e6 << " us spent on " << num_loops << " loops" << "\n";
    return 0;
}
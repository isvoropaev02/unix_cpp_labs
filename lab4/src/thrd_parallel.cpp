#include <iostream>
#include <random>
#include <vector>
#include <ctime>
#include <thread>
#include <mutex>

inline double formula1(const double x) { return x * x - x * x + x * 4 - x * 5 + x + x; }

inline double formula2(const double x) { return x + x; }

double measure_time(double x, size_t num_loops)
{
    // set-up
    std::mutex mtx;
    std::vector<double> val1(num_loops);
    std::vector<double> val2(num_loops);
    [[maybe_unused]] double val3;

    clock_t time_start = clock();

    std::thread thrd1([&](){
        for (size_t i = 0; i < num_loops; i++){
            mtx.lock();
            val1[i] = formula1(x);
            mtx.unlock();
        }
    });

    std::thread thrd2([&](){
        for (size_t i = 0; i < num_loops; i++){
            mtx.lock();
            val2[i] = formula2(x);
            mtx.unlock();
        }
    });
    thrd1.join();
    thrd2.join();

    for (size_t i = 0; i < num_loops; i++) val3 = val1[i] + val2[i] - val1[i];

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

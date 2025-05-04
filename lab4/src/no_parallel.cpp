#include <iostream>
#include <random>
#include <ctime>

inline double formula1(const double x) { return x * x - x * x + x * 4 - x * 5 + x + x; }

inline double formula2(const double x) { return x + x; }

double measure_time(double x, size_t num_loops)
{
    clock_t time_start = clock();
    for (size_t j_loop = 0; j_loop < num_loops; j_loop++)
    {
        double val1 = formula1(x);
        double val2 = formula2(x);
        [[maybe_unused]] double val3 = val1 + val2 - val1;
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

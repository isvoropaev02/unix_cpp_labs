#include <iostream>
#include <cmath>
#include <string>
#include <vector>
#include <random>
#include <ctime>

double measure_time(double x, size_t num_loops)
{
    double val;
    clock_t time_start = clock();
    for (size_t j_loop = 0; j_loop < num_loops; j_loop++)
    {
        val = pow(x, 2) - pow(x, 2) + pow(x, 4) - pow(x, 5) + x + x;
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

    // same as in python
    double x;
    size_t num_loops;
    double time;
    std::vector<double> time_vec;
    std::string ans{"y"};

    while (ans == "y")
    {
        std::cout << "Input number of loops: ";
        if (!(std::cin >> num_loops))
        {
            std::cout << "Input should be a number" << "\n";
            break;
        }
        x = dis(gen);
        time = measure_time(x, num_loops);
        time_vec.push_back(time);
        std::cout << time*1e6 << " us spent on " << num_loops << " loops" << "\n";
        std::cout << "Do you wish to continue? [y/n]: ";
        std::cin >> ans;
    }
    // printing vector
    std::cout << "[";
    for (size_t j_time = 0; j_time < time_vec.size(); j_time++) std::cout << time_vec[j_time] << ", ";
    std::cout << "]\n";
    return 0;
}

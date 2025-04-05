#include <iostream>
#include <cmath>
#include <string>
#include <vector>
#include <random>

int main()
{
    // random gen config
    std::random_device rd;  // Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dis(0.0, 1.0);

    // same as in python
    double x;
    unsigned int num_loops;
    std::vector<double> time_vec;
    std::string ans{"y"};
    while (ans == "y")
    {
        
    }
    
    return 0;
}

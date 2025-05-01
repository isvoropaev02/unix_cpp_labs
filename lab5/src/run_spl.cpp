#include <string>
#include <stdexcept>
#include <ctime>
#include <iostream>

static char OUTPUT{'c'};
static std::string FILE_PATH{""};

int main(int argc, char const *argv[])
{
    switch (argc)
    {
    case 1:
        break;
    case 2:
        FILE_PATH = std::string(argv[1]);
        OUTPUT = 'f';
        break;
    default:
        throw std::invalid_argument("Only 1 optional CLI argument is supported (<OUTPUT_FILE_PATH>)\n");
        break;
    }
    clock_t time_start = clock();
    // main code
    clock_t time_end = clock();
    std::cout << "Execution time: " << double(time_end - time_start) / CLOCKS_PER_SEC << "\n";
    return 0;
}

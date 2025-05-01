#include <string>
#include <stdexcept>

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
    return 0;
}

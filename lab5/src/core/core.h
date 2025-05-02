#include "command.h"

#include <string>
#include <stdexcept>
#include <vector>

class Core
{
private:
    std::vector<std::vector<int>> tasks_;
public:
    Core(std::vector<std::vector<std::vector<std::string>>>);
    ~Core();
};

Core::Core(std::vector<std::vector<std::vector<std::string>>>)
{

}

Variable a;
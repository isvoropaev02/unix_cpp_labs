#include <vector>
#include <string>

class parser
{
private:
    std::vector<std::string> tokenize_line();
public:
    parser() = default;
    ~parser() = default;
    std::vector<std::vector<std::string>> process();
};

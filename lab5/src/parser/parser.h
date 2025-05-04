#include <vector>
#include <string>

class Parser
{
private:
    std::vector<std::vector<std::string>> tokenize_line(const std::string& line);
    size_t line_num_{0};
public:
    Parser() = default;
    ~Parser() = default;
    std::vector<std::vector<std::vector<std::string>>> process();
};

#include "core.h"
#include "command.h"

#include <vector>
#include <string>
#include <stdexcept>

Core::Core(const std::vector<std::vector<std::vector<std::string>>>& comands)
{
    for (size_t i = 0; i < comands.size(); i++)
    {
        std::vector<int> line_expr;
        std::vector<std::vector<std::string>> comand_line = comands[i];
        for (size_t j = 0; j < comand_line.size(); j++)
        {
            auto expr = derive_comand(comand_line[j]);
            line_expr.push_back(expr);
        }
        tasks_.push_back(line_expr);
    }
    
}
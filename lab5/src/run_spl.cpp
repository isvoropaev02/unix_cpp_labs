#include "io_handler/parser.h"

#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <bits/stdc++.h>

void redirect_cout_to_file(const std::string& filename)
{
    static std::ofstream out(filename, std::ios::app);
    std::cout.rdbuf(out.rdbuf());
}

int main(int argc, char const *argv[])
{
    switch (argc)
    {
    case 1:
        break;
    case 2:
        redirect_cout_to_file(std::string(argv[1]));
        break;
    default:
        throw std::invalid_argument("Only 1 optional CLI argument is supported (<OUTPUT_FILE_PATH>)\n");
        break;
    }
    std::cout << "here\n";
    Parser parser;
    auto commands = parser.process();
    for (size_t i = 0; i < commands.size(); i++)
    {
        std::cout << "line " << i << "\n";
        auto commands_line = commands[i];
        for (size_t j = 0; j < commands_line.size(); j++)
        {
            std::cout << "command " << j << "\n";
            auto comand_j = commands_line[j];
            for (size_t k = 0; k < comand_j.size(); k++)
            {
                std::cout << comand_j[k] << " ";
            }
            std::cout << "\n";
        }
        std::cout << "\n";
    }
    return 0;
}

#include "parser/parser.h"
#include "core/core.h"

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
        return 1;
    }
    Parser parser;
    const auto commands = parser.process();
    Core core(commands);
    core.process();
    return 0;
}

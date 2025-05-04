#include "parser/parser.h"
#include "core/core.h"
#include "parser/io_handler.h"

#include <string>
#include <vector>
#include <stdexcept>
#include <iostream>
#include <fstream>

int main(int argc, char const *argv[])
{
    parse_args(argc, argv);
    Parser parser;
    const auto commands = parser.process();
    Core core(commands);
    core.process();
    return 0;
}

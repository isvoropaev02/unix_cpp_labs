#include "parser.h"
#include <stdexcept>
#include <bits/stdc++.h>

std::vector<std::vector<std::string>> Parser::tokenize_line(const std::string& line)
{
    if (line[0] != '!') throw std::invalid_argument("Syntax error in line " + std::to_string(line_num_) + "\n");
    // split commands
    std::vector<std::string> commands;
    size_t start = 0;
    size_t end = line.find('!');
    
    while (end != std::string::npos) {
        if (end != start) {
            commands.push_back(line.substr(start, end - start));
        }
        start = end + 1;
        end = line.find('!', start);
    }
    if (start < line.length()) commands.push_back(line.substr(start));

    // tokenize commands
    std::vector<std::vector<std::string>> tok_line;
    for (size_t i = 0; i < commands.size(); i++)
    {
        std::vector<std::string> tokens;
        std::istringstream iss(commands[i]);
        std::string token;
        while (std::getline(iss, token, ' '))
        {
            if (!token.empty()) tokens.push_back(token);
        }
        tok_line.push_back(tokens);
    }
    return tok_line;
}

std::vector<std::vector<std::vector<std::string>>> Parser::process()
{
    std::vector<std::vector<std::vector<std::string>>> all_commands;
    for (size_t i = 0; i < 1000; i++)
    {
        line_num_++;
        std::string line;
        std::getline(std::cin, line);
        if (line.size() == 1 && line[0] == '!') break;
        all_commands.push_back(tokenize_line(line));
    }
    return all_commands;
}
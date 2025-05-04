#pragma once
#include <string>

void redirect_cout_to_file(const std::string& filename);
void redirect_cin_from_file(const std::string& filename);
void parse_args(int argc, const char* argv[]);
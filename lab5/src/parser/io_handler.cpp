#include "io_handler.h"

#include <stdexcept>
#include <iostream>
#include <fstream>
#include <memory>

std::unique_ptr<std::ifstream> input_file;
std::streambuf* orig_cin_buf = nullptr;

void redirect_cout_to_file(const std::string& filename)
{
    static std::ofstream out(filename, std::ios::app);
    std::cout.rdbuf(out.rdbuf());
}

void redirect_cin_from_file(const std::string& filename)
{
    // Закрываем предыдущий файл (если был)
    input_file.reset();
    input_file = std::make_unique<std::ifstream>(filename);
    if (!input_file->is_open()) throw std::runtime_error("Failed to open file: " + filename);
    // Сохраняем оригинальный буфер (только при первом вызове)
    if (!orig_cin_buf) orig_cin_buf = std::cin.rdbuf();
    // Перенаправляем cin
    std::cin.rdbuf(input_file->rdbuf());
}

void parse_args(int argc, const char* argv[])
{
    for (int i = 1; i < argc; ++i)
    {
        std::string arg = argv[i];
        if (arg == "-i" || arg == "--input")
        {
            if (i + 1 < argc) redirect_cin_from_file(argv[++i]);
            else std::cerr << "Error: Missing argument for " << arg << std::endl;
        }
        else if (arg == "-o" || arg == "--output")
        {
            if (i + 1 < argc) redirect_cout_to_file(argv[++i]);
            else std::cerr << "Error: Missing argument for " << arg << std::endl;
        }
        else std::cerr << "Error: Unknown option " << arg << std::endl;
    }
}
#pragma once
#include <string>

struct Variable
{
    int val_int_{0};
    float val_flt_{0.0};
    std::string type_{"flt"};
    Variable(const std::string& val="0", const std::string& type="flt");
    Variable(Variable& other);
    ~Variable() = default;
};

#include <vector>
#include <string>
#include "core.h"
#include<iostream>


class IExpression
{
public:
    virtual void check_syntaxis() = 0;
    virtual void run() = 0;
};

class CreateVariable : public IExpression
{
private:
    void check_syntaxis() override;
    std::vector<std::string> tok_line_;
public:
    CreateVariable(const std::vector<std::string>& tok_line);
    ~CreateVariable() = default;
    void run() override;
};

CreateVariable::CreateVariable(const std::vector<std::string>& tok_line) : tok_line_(tok_line) {}

void CreateVariable::check_syntaxis()
{
    if (tok_line_.size() != 4) throw std::invalid_argument("Error in creating variable\n");
    std::string type{tok_line_[0]}, val{tok_line_[3]}, name {tok_line_[1]};
    if (!(type == "flt" || type == "int")) throw std::runtime_error("Variables must be int or flt, no such type: " + type + " \n");
    try {
        auto _ = std::stof(val);
     }
     catch(...) {
        throw std::invalid_argument("Error in creating variable: " + val + "\n");
     }
}

void CreateVariable::run()
{
    check_syntaxis();
    Variable new_var(tok_line_[3], tok_line_[0]);
    VARIABLES.insert({tok_line_[1], new_var});
}


class Print : public IExpression
{
private:
    void print_to_file();
    void print_to_console();
    void check_syntaxis() override;
    std::vector<std::string> tok_line_;
public:
    Print(const std::vector<std::string>& tok_line);
    ~Print() = default;
    void run() override;
};

Print::Print(const std::vector<std::string>& tok_line) : tok_line_(tok_line) {}

void Print::check_syntaxis()
{
    if (tok_line_.size() != 2) throw std::invalid_argument("Error in printing: Incorrect number of arguments\n");
    if (auto search = VARIABLES.find(tok_line_[1]); search == VARIABLES.end())
    {
        throw std::invalid_argument("Error in printing: No such variable" + tok_line_[1] + "\n");
    }
}

void Print::run()
{
    check_syntaxis();
    Variable tmp = VARIABLES[tok_line_[1]];
    auto val = (tmp.type_ == "flt") ? tmp.val_flt_ : tmp.val_int_;
    std::cout << tok_line_[1] << " : " << val << tmp.type_ << "\n";
}
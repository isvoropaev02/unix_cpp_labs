#include "comand.h"

#include <stdexcept>
#include <iostream>
#include <mutex>

std::mutex cout_mtx;


Variable::Variable(const std::string& val, const std::string& type) : type_(type), val_flt_(std::stof(val)), val_int_((int)std::stof(val)) {}
Variable::Variable(Variable& other) : val_int_(other.val_int_), val_flt_(other.val_flt_), type_(other.type_) {}

IComand::IComand(const std::vector<std::string>& tok_line) : tok_line_(tok_line) {}

CreateVariable::CreateVariable(const std::vector<std::string>& tok_line) : IComand(tok_line) {}

void CreateVariable::check_syntaxis()
{
    if (tok_line_.size() != 4) throw std::invalid_argument("Error in creating variable\n");
    std::string type{tok_line_[0]}, val{tok_line_[3]}, name {tok_line_[1]}, eq{tok_line_[2]};
    if (eq != "=") throw std::runtime_error("Error in creating variable: = expected, " + eq + " received instead\n");
    if (!(type == "flt" || type == "int")) throw std::runtime_error("Variables must be int or flt, no such type: " + type + " \n");
    try {
        auto _ = std::stof(val);
     }
     catch(...) {
        throw std::invalid_argument("Error in creating variable: " + val + "\n");
     }
}

void CreateVariable::run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id)
{
    check_syntaxis();
    Variable new_var(tok_line_[3], tok_line_[0]);
    variables.insert_or_assign(tok_line_[1], new_var);
}

Print::Print(const std::vector<std::string>& tok_line) : IComand(tok_line) {}

void Print::check_syntaxis()
{
    if (tok_line_.size() != 2) throw std::invalid_argument("Error in printing: Incorrect number of arguments\n");
}

void Print::run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id)
{
    check_syntaxis();
    if (auto search = variables.find(tok_line_[1]); search == variables.end())
    {
        throw std::invalid_argument("Error in printing: No such variable" + tok_line_[1] + "\n");
    }
    Variable tmp = variables[tok_line_[1]];
    if (tmp.type_ == "flt")
    {
        cout_mtx.lock();
        std::cout << ("[THREAD " + std::to_string(thread_id) + "] " + tok_line_[1] + " : " + std::to_string(tmp.val_flt_) + " (" + tmp.type_ +")\n");
        cout_mtx.unlock();
    }
    else
    {
        cout_mtx.lock();
        std::cout << ("[THREAD " + std::to_string(thread_id) + "] " + tok_line_[1] + " : " + std::to_string(tmp.val_int_) + " (" + tmp.type_ +")\n");
        cout_mtx.unlock();
    }
}

Expression::Expression(const std::vector<std::string>& tok_line) : IComand(tok_line) {}

void Expression::check_syntaxis()
{
    if (tok_line_.size() != 6) throw std::invalid_argument("Error in expression\n");
    std::string eq{tok_line_[2]}, op{tok_line_[4]};
    if (eq != "=") throw std::runtime_error("Error in expression: = expected, " + eq + " received instead\n");
    if (!(op == "+" || op == "-" || op == "*" || op == "/")) throw std::runtime_error("Error in expression: binary operation expected, " + op + " received instead\n");
}

Variable Expression::calculate(const std::string& bop, Variable& var1, Variable& var2)
{
    Variable out;
    if (var1.type_ == "int" && var2.type_ == "int") out.type_ = "int";
    switch (char(bop[0]))
    {
        case '+':
            if (out.type_ == "flt")
            {
                out.val_flt_ = var1.val_flt_ + var2.val_flt_;
                out.val_int_ = int(out.val_flt_);
            }
            else
            {
                out.val_int_ = var1.val_int_ + var2.val_int_;
                out.val_flt_ = float(out.val_int_);
            }
            break;
        case '-':
            if (out.type_ == "flt")
            {
                out.val_flt_ = var1.val_flt_ - var2.val_flt_;
                out.val_int_ = int(out.val_flt_);
            }
            else
            {
                out.val_int_ = var1.val_int_ - var2.val_int_;
                out.val_flt_ = float(out.val_int_);
            }
            break;
        case '*':
            if (out.type_ == "flt")
            {
                out.val_flt_ = var1.val_flt_ * var2.val_flt_;
                out.val_int_ = int(out.val_flt_);
            }
            else
            {
                out.val_int_ = var1.val_int_ * var2.val_int_;
                out.val_flt_ = float(out.val_int_);
            }
            break;
        case '/':
            if (out.type_ == "flt")
            {
                if(var2.val_flt_ == 0.0) throw std::runtime_error("Division by 0\n");
                else out.val_flt_ = var1.val_flt_ / var2.val_flt_;
                out.val_int_ = int(out.val_flt_);
            }
            else
            {
                if(var2.val_int_ == 0) throw std::runtime_error("Division by 0\n");
                else out.val_int_ = var1.val_int_ / var2.val_int_;
                out.val_flt_ = float(out.val_int_);
            }
            break;
        default:
            throw std::runtime_error("No such binary operation: " + bop + "\n");
            break;
    }
    return out;
}

void Expression::run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id)
{
    check_syntaxis();
    std::string var1_name{tok_line_[3]}, var2_name{tok_line_[5]};
    auto search1 = variables.find(var1_name);
    auto search2 = variables.find(var2_name);
    if (search1 == variables.end() || search2 == variables.end())
    {
        throw std::invalid_argument("Error in expression: No such variables " + var1_name + " and " + var2_name + "\n");
    }
    Variable new_var = calculate(tok_line_[4], variables[var1_name], variables[var2_name]);
    variables.insert_or_assign(tok_line_[1], new_var);
}
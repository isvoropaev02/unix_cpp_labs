#include "comand.h"

#include <stdexcept>
#include <iostream>
#include <mutex>

std::mutex cout_mtx;


Variable::Variable(const std::string& val, const std::string& type) : type_(type), val_flt_(std::stof(val)), val_int_((int)val_flt_) {}
Variable::Variable(Variable& other) : val_int_(other.val_int_), val_flt_(other.val_flt_), type_(other.type_) {}

Variable calculate_expr(const std::string& bop, Variable& var1, Variable& var2)
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

IExpression::IExpression(const std::vector<std::string>& tok_line) : tok_line_(tok_line) {}

CreateVariable::CreateVariable(const std::vector<std::string>& tok_line) : IExpression(tok_line) {}

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

void CreateVariable::run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id)
{
    check_syntaxis();
    Variable new_var(tok_line_[3], tok_line_[0]);
    variables.insert_or_assign(tok_line_[1], new_var);
}

Print::Print(const std::vector<std::string>& tok_line) : IExpression(tok_line) {}

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
    auto val = (tmp.type_ == "flt") ? tmp.val_flt_ : tmp.val_int_;
    cout_mtx.lock();
    std::cout << ("[THREAD " + std::to_string(thread_id) + "] " + tok_line_[1] + " : " + std::to_string(val) + " (" + tmp.type_ +")\n");
    cout_mtx.unlock();
}

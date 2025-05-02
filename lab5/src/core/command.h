#include <vector>
#include <iostream>
#include <unordered_map>
#include <string>
#include <stdexcept>

struct Variable
{
    int val_int_{0};
    float val_flt_{0.0};
    std::string type_{"flt"};
    Variable(const std::string& val="0", const std::string& type="flt");
    Variable(Variable& other);
    ~Variable() = default;
};

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
}

static std::unordered_map<std::string, Variable> VARIABLES;


class IExpression
{
protected:
    std::vector<std::string> tok_line_;
    virtual void check_syntaxis() = 0;
public:
    virtual void run() = 0;
    IExpression(const std::vector<std::string>& tok_line);
    virtual ~IExpression() = default;
};

IExpression::IExpression(const std::vector<std::string>& tok_line) : tok_line_(tok_line) {}

class CreateVariable : public IExpression
{
private:
    void check_syntaxis() override;
    // std::vector<std::string> tok_line_;
public:
    CreateVariable(const std::vector<std::string>& tok_line);
    ~CreateVariable() = default;
    void run() override;
};

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

void CreateVariable::run()
{
    check_syntaxis();
    Variable new_var(tok_line_[3], tok_line_[0]);
    VARIABLES.insert({tok_line_[1], new_var});
}


class Print : public IExpression
{
private:
    void check_syntaxis() override;
public:
    Print(const std::vector<std::string>& tok_line);
    ~Print() = default;
    void run() override;
};

Print::Print(const std::vector<std::string>& tok_line) : IExpression(tok_line) {}

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
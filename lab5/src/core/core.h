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


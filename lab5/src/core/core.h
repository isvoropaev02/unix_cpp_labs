#include <unordered_map>
#include <string>
#include <stdexcept>

class Variable
{
private:
    int val_int_{0};
    float val_flt_{0.0};
    std::string type_;
public:
    Variable(const std::string& val="0", const std::string& type="flt");
    Variable(Variable& other);
    std::string get_type();
    int get_int();
    float get_flt();
    void set_type(const std::string& tmp);
    void set_int(int tmp);
    void set_flt(float tmp);
    ~Variable() = default;
};

Variable::Variable(const std::string& val, const std::string& type) : type_(type)
{
    val_flt_ = std::stof(val);
    val_int_ = int(val_flt_);
}

std::string Variable::get_type() { return type_; }
int Variable::get_int() { return val_int_; }
float Variable::get_flt() { return val_flt_; }
void Variable::set_type(const std::string& tmp) { type_ = tmp; }
void Variable::set_int(int tmp) { val_int_ = tmp; }
void Variable::set_flt(float tmp) { val_flt_ = tmp; }

Variable::Variable(Variable& other)
{
    type_ = other.get_type();
    val_int_ = other.get_int();
    val_flt_ = other.get_flt();
}



Variable calculate_expr(const std::string& bop, Variable& var1, Variable& var2)
{
    Variable out;
    switch (char(bop[0]))
    {
        case '+':
            if 
            break;
        case '-':
            break;
        case '*':
            break;
        case '/':
            break;
        default:
            throw std::runtime_error("No such binary operation: " + bop + "\n");
            break;
    }
}

static std::unordered_map<std::string, Variable> VARIABLES;


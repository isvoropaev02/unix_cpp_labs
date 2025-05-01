#include <vector>
#include <string>

class IExpression
{
public:
    virtual void run() = 0;
};

template <typename T>
class Calculate : private IExpression
{
private:
    void run();
    T res_value_;
    std::string new_var_;
public:
    Calculate();
    ~Calculate() = default;
};

Calculate::Calculate()
{
}

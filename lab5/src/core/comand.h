#include <vector>
#include <unordered_map>
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

class IExpression
{
protected:
    std::vector<std::string> tok_line_;
    virtual void check_syntaxis() = 0;
public:
    virtual void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) = 0;
    IExpression(const std::vector<std::string>& tok_line);
    virtual ~IExpression() = default;
};

class CreateVariable : public IExpression
{
private:
    void check_syntaxis() override;
    // std::vector<std::string> tok_line_;
public:
    CreateVariable(const std::vector<std::string>& tok_line);
    ~CreateVariable() = default;
    void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) override;
};

class Print : public IExpression
{
private:
    void check_syntaxis() override;
public:
    Print(const std::vector<std::string>& tok_line);
    ~Print() = default;
    void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) override;
};

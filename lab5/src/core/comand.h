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

class IComand
{
protected:
    std::vector<std::string> tok_line_;
    virtual void check_syntaxis() = 0;
public:
    virtual void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) = 0;
    IComand(const std::vector<std::string>& tok_line);
    virtual ~IComand() = default;
};

class CreateVariable : public IComand
{
private:
    void check_syntaxis() override;
    // std::vector<std::string> tok_line_;
public:
    CreateVariable(const std::vector<std::string>& tok_line);
    ~CreateVariable() = default;
    void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) override;
};

class Print : public IComand
{
private:
    void check_syntaxis() override;
public:
    Print(const std::vector<std::string>& tok_line);
    ~Print() = default;
    void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) override;
};

class Expression : public IComand
{
private:
    void check_syntaxis() override;
    Variable calculate(const std::string& bop, Variable& var1, Variable& var2);
public:
    Expression(const std::vector<std::string>& tok_line);
    ~Expression() = default;
    void run(std::unordered_map<std::string, Variable>& variables, const size_t thread_id) override;
};

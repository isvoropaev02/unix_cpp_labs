#include "command.h"

#include <string>
#include <stdexcept>
#include <vector>


class Core
{
private:
    std::vector<std::vector<IExpression>> tasks_;

    template <class Expr>
    Expr derive_comand(const std::vector<std::string>& comand);
public:
    Core(const std::vector<std::vector<std::vector<std::string>>>& comands);
    ~Core() = default;
    void process();
};

template <class Expr>
Expr Core::derive_comand(const std::vector<std::string>& comand)
{
    if (comand[0] == "int" || comand[0] == "flt")
    {
        using Expr = CreateVariable;
        return Expr(comand);
    }
    else if (comand[0] == "print")
    {
        using Expr = Print;
        return Expr(comand);
    }
    else
    {
        using Expr = Print; // ну лишь бы какой-то
        throw std::invalid_argument("No such comand: " + comand[0] + "\n");
        return Expr(comand);
    }
    
}

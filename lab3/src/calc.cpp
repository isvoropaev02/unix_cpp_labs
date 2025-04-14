#include <iostream>
#include <cstdlib>
#include <cassert>

int main(int argc, char const **argv)
{
    assert(argc == 4);
    double x1{std::atof(argv[1])}, x2{std::atof(argv[3])};
    char op{*argv[2]};

    switch (op)
    {
        case '+':
        {
            std:: cout << x1 << " + " << x2 << " = " << x1 + x2 << "\n";
            break;
        }
        case '-':
        {
            std:: cout << x1 << " - " << x2 << " = " << x1 - x2 << "\n";
            break;
        }
        case '^':
        {
            int p = int(x2);
            double ans{1};
            double coeff = p >= 0 ? x1 : ((double)1 / x1);
            int abs_p = p >= 0 ? p : -p;
            for (int i = 0; i < abs_p; i++) ans *= coeff;
            std:: cout << x1 << " ^ " << p << " = " << ans << "\n";
            break;
        }
        default:
        {
            std::cout << "[ERROR] Only +, - and ^ operations can be used.";
            break;
        }
    }
    return 0;
}

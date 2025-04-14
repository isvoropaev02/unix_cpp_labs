#include <iostream>
#include <list>
#include <string>

void execute_step(int n, int pin_from, int pin_to, std::list<std::string>& moves_log)
{
    std::string descr;
    if (n == 1)
    {
        descr.append("Move disk 1 from pin ");
        descr.append(std::to_string(pin_from));
        descr.append(" to pin ");
        descr.append(std::to_string(pin_to));
        moves_log.push_back(descr);
        return;
    }
    int pin_tmp = 6 - pin_from - pin_to;
    execute_step(n-1, pin_from, pin_tmp, moves_log);
    descr.append("Move disk ");
    descr.append(std::to_string(n));
    descr.append(" from pin ");
    descr.append(std::to_string(pin_from));
    descr.append(" to pin ");
    descr.append(std::to_string(pin_to));
    moves_log.push_back(descr);
    execute_step(n-1, pin_tmp, pin_to, moves_log);
}

void print_solution(std::list<std::string>& moves_log) { for (const auto& s: moves_log) std::cout << s << "\n"; }

int main()
{
    std::list<std::string> moves_log;
    int n{4}, pin_from{1}, pin_to{3};
    execute_step(n, pin_from, pin_to, moves_log);
    std::cout << "Number of steps: " << moves_log.size() << "\n";
    print_solution(moves_log);
    return 0;
}

#include "variable.h"

Variable::Variable(const std::string& val, const std::string& type) : type_(type), val_flt_(std::stof(val)), val_int_((int)std::stof(val)) {}
Variable::Variable(Variable& other) : val_int_(other.val_int_), val_flt_(other.val_flt_), type_(other.type_) {}

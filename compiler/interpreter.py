import sys
from compiler.lexer import lexer
from compiler.parser import parser


class value:
    def __init__(self, type, val=None):
        self.type = type
        self.val = val

    def is_empty(self):
        return self.val == None


class array_value:
    def __init__(self, type, vals=[]):
        self.type = type
        self.values = vals
        self.size = len(vals)

    def append(self, value):
        if value.type != self.type:
            raise Exception(
                f"error: incompatible types: {value.type} cannot be converted to {self.type}"
            )
        self.values.append(value)
        self.size += 1

    def is_empty(self):
        return self.size == 0


class variable:
    def __init__(self, name, type, val=None):
        self.name = name
        self.type = type
        if isinstance(val, value):
            if val.type == self.type:
                self.value = val
                return
            if val.type == "char" and self.type == "int":
                self.value = value(self.type, ord(val.val))
                return
            if val.type == "int" and self.type == "char":
                self.value = value(self.type, chr(val.val))
                return
        raise Exception("error: Incompatible types")

    def assign(self, value):
        if value.type == self.type:
            self.value.val = value.val
            return
        if value.type == "char" and self.type == "int":
            self.value.val = ord(value.val)
            return
        if value.type == "int" and self.type == "char":
            self.value.val = chr(value.val)
            return
        raise Exception("error: Incompatible types")

    def get_value(self):
        if self.value.is_empty():
            raise Exception(
                f"error: variable {self.name} might not have been initialized"
            )
        return self.value


class array:
    def __init__(self, name, type, arr_val):
        self.name = name
        self.type = type
        if isinstance(arr_val, value):
            raise Exception(
                f"error: incompatible types: {arr_val.type} cannot be converted to {self.type}[]"
            )
        if isinstance(arr_val, array_value) and arr_val.type != type:
            raise Exception(
                f"error: incompatible types: {arr_val.type} cannot be converted to {self.type}"
            )
        self.array_value = arr_val

    def assign(self, value, index):
        if value.type != self.type:
            raise Exception("error: incompatible types")
        if self.array_value.is_empty():
            raise Exception(
                f"error: variable {self.name} might not have been initialized"
            )
        if index >= self.array_value.size:
            raise Exception(
                f"java.lang.ArrayIndexOutOfBoundsException: Index {index} out of bounds for length {self.array_value.size}"
            )
        self.array_value.values[index] = value

    def instantiate(self, size):
        self.array_value.size = size
        self.array_value.values = [value(self.type, val=None) for i in range(size)]

    def get_value(self, index):
        if self.array_value.is_empty():
            raise Exception(
                f"error: variable {self.name} might not have been initialized"
            )
        if index >= self.array_value.size:
            raise Exception(
                f"java.lang.ArrayIndexOutOfBoundsException: Index {index} out of bounds for length {self.array_value.size}"
            )
        return self.array_value.values[index]


class interpreter:
    def __init__(self):
        self.variables = dict()

    def int(self, v):
        return value("int", v)

    def double(self, v):
        return value("double", v)

    def String(self, v):
        return value("String", v)

    def char(self, v):
        return value("char", v)

    def boolean(self, v):
        return value("boolean", v)

    def identifier(self, var_name):
        if not self.var_exists(var_name):
            raise Exception("error: cannot find symbol")
        if isinstance(self.variables[var_name], array):
            raise Exception("error: value required but array found")
        return self.variables[var_name].get_value()

    def array_identifier(self, var_name, index):
        if not self.var_exists(var_name):
            raise Exception("error: cannot find symbol")
        if not isinstance(self.variables[var_name], array):
            raise Exception(
                f"error: array required but {self.variables[var_name].type} found"
            )
        return self.variables[var_name].get_value(index)

    def declare(self, var_type, var_name):
        if self.var_exists(var_name):
            raise Exception(f"error: variable {var_name} is already defined")
        self.variables[var_name] = variable(var_name, var_type)

    def array_declare(self, var_type, var_name):
        if self.var_exists(var_name):
            raise Exception(f"error: variable {var_name} is already defined")
        self.variables[var_name] = array(
            var_name, var_type, arr_val=array_value(var_type, vals=[])
        )

    def assign(self, var_name, rhs):
        if not self.var_exists(var_name):
            raise Exception("error: cannot find symbol")
        value = self.eval(*rhs)
        if isinstance(self.variables[var_name], array):
            raise Exception(
                f"error: incompatible types: {value.type} cannot be converted to {self.variables[var_name].type}[]"
            )
        self.variables[var_name].assign(value)

    def array_assign(self, var_name, index, rhs):
        if not self.var_exists(var_name):
            raise Exception("error: cannot find symbol")
        if not isinstance(self.variables[var_name], array):
            raise Exception(
                f"error: array required but {self.variables[var_name].type} found"
            )
        value = self.eval(*rhs)
        self.variables[var_name].assign(value, index)

    def initialize(self, var_type, var_name, rhs):
        if self.var_exists(var_name):
            raise Exception(f"error: variable {var_name} is already defined")
        value = self.eval(*rhs)
        self.variables[var_name] = variable(var_name, var_type, value)

    def array_initialize(self, var_type, var_name, vals):
        if self.var_exists(var_name):
            raise Exception(f"error: variable {var_name} is already defined")
        arrval = array_value(var_type, [])
        for v in vals:
            value = self.eval(*v)
            arrval.append(value)
        self.variables[var_name] = array(var_name, var_type, arr_val=arrval)

    def array_instantiate(self, var_name, var_type, size):
        if not self.var_exists(var_name):
            raise Exception("error: cannot find symbol")
        if not isinstance(self.variables[var_name], array):
            raise Exception(
                f"error: array required but {self.variables[var_name].type} found"
            )
        if self.variables[var_name].type != var_type:
            raise Exception(
                f"error: incompatible types: {var_type}[] cannot be converted to {self.variables[var_name].type}[]"
            )
        self.variables[var_name].instantiate(size)

    def array_declare_instantiate(self, var_type, var_name, size):
        self.array_declare(var_type, var_name)
        self.array_instantiate(var_name, var_type, size)

    def println(self, rhs):
        val = self.eval(*rhs)
        if val:
            print(val.val)

    def print(self, rhs):
        val = self.eval(*rhs)
        if val:
            sys.stdout.write(str(val.val))
            sys.stdout.flush()

    def arithematic_operation(self, op, lhs, rhs):
        l = self.eval(*lhs)
        r = self.eval(*rhs)
        if "boolean" in [l.type, r.type]:
            raise Exception(f"error: bad operand type for binary operator '{op}'")
        if "String" in [l.type, r.type]:
            if op == "+":
                return value("String", str(l.val) + str(r.val))
            raise Exception(f"error: bad operand type for binary operator '{op}'")
        lv, rv = l.val, r.val
        if l.type == "char":
            lv = ord(l.val)
        if r.type == "char":
            rv = ord(r.val)
        if op == "+":
            ov = lv + rv
        elif op == "-":
            ov = lv - rv
        elif op == "*":
            ov = lv * rv
        elif op == "/":
            ov = lv / rv
        elif op == "%":
            ov = lv % rv
        try:
            if "double" in [l.type, r.type]:
                return value("double", ov)
            return value("int", int(ov))
        except ZeroDivisionError:
            raise Exception("java.lang.ArithmeticException: / by zero")

    def uminus(self, rhs):
        v = self.eval(*rhs)
        if v.type in ["boolean", "String"]:
            raise Exception(f"error: bad operand type {v.type} for unary operator '-'")
        if v.type == "char":
            return value("int", -ord(v.val))
        return value(v.type, -v.val)

    def increment(self, var_name, post_increment):
        v = self.identifier(var_name)
        if v.type in ["boolean", "String"]:
            raise Exception(f"error: bad operand type {v.type} for unary operator '++'")
        tmp_val = self.eval(
            "arithematic_operation", "+", ("identifier", var_name), ("int", 1)
        )
        self.eval("assign", var_name, (tmp_val.type, tmp_val.val))
        if post_increment:
            tmp_val.val -= 1
            return tmp_val
        return tmp_val

    def decrement(self, var_name, post_decrement):
        v = self.identifier(var_name)
        if v.type in ["boolean", "String"]:
            raise Exception(f"error: bad operand type {v.type} for unary operator '--'")
        tmp_val = self.eval(
            "arithematic_operation", "-", ("identifier", var_name), ("int", 1)
        )
        self.eval("assign", var_name, (tmp_val.type, tmp_val.val))
        if post_decrement:
            tmp_val.val += 1
            return tmp_val
        return tmp_val

    def eval(self, method, *args):
        return self.__getattribute__(method)(*args)

    def var_exists(self, var_name):
        if var_name in [v for v in self.variables]:
            return True
        return False


def interpret():
    i = interpreter()
    while True:
        try:
            exp = input("> ")
        except EOFError:
            break

        if not exp:
            continue

        if exp == "exit":
            break

        try:
            parse_out = parser.parse(exp, lexer=lexer)
            if parse_out:
                i.eval(parse_out[0], *parse_out[1:])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    interpret()
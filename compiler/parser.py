from compiler.lexer import tokens
import ply.yacc as yacc

start = "exp"

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MOD"),
    ("right", "INCREMENT", "DECREMENT", "UMINUS"),
    ("nonassoc", "POST_INCREMENT", "POST_DECREMENT"),
    ("left", "LPAREN", "RPAREN"),
)


def p_exp_declaration(p):
    "exp : var_type IDENTIFIER SEMICOLON"
    p[0] = ("declare", p[1], p[2])


def p_exp_initialization(p):
    "exp : var_type IDENTIFIER EQUAL RHS SEMICOLON"
    p[0] = ("initialize", p[1], p[2], p[4])


def p_exp_assignment(p):
    "exp : IDENTIFIER EQUAL RHS SEMICOLON"
    p[0] = ("assign", p[1], p[3])


def p_array_declaration(p):
    """exp : var_type LBRACK RBRACK IDENTIFIER SEMICOLON
    | var_type IDENTIFIER LBRACK RBRACK SEMICOLON"""
    if p[2] == "[":
        p[0] = ("array_declare", p[1], p[4])
    else:
        p[0] = ("array_declare", p[1], p[2])


def p_array_instantiation(p):
    "exp : IDENTIFIER EQUAL NEW var_type LBRACK INT_NUMBER RBRACK SEMICOLON"
    p[0] = ("array_instantiate", p[1], p[4], p[6])


def p_array_declaration_instantiation(p):
    """exp : var_type LBRACK RBRACK IDENTIFIER EQUAL NEW var_type LBRACK INT_NUMBER RBRACK SEMICOLON
    | var_type IDENTIFIER LBRACK RBRACK EQUAL NEW var_type LBRACK INT_NUMBER RBRACK SEMICOLON"""
    if p[1] != p[7]:
        raise Exception(
            f"error: incompatible types: {p[7]}[] cannot be converted to {p[1]}[]"
        )
    if p[2] == "[":
        p[0] = ("array_declare_instantiate", p[1], p[4], p[9])
    else:
        p[0] = ("array_declare_instantiate", p[1], p[2], p[9])


def p_array_initialization(p):
    """exp : var_type IDENTIFIER LBRACK RBRACK EQUAL LBRACE optargs RBRACE SEMICOLON
    | var_type LBRACK RBRACK IDENTIFIER EQUAL LBRACE optargs RBRACE SEMICOLON"""
    if p[2] == "[":
        p[0] = ("array_initialize", p[1], p[4], p[7])
    else:
        p[0] = ("array_initialize", p[1], p[2], p[7])


def p_array_assignment(p):
    "exp : IDENTIFIER LBRACK INT_NUMBER RBRACK EQUAL RHS SEMICOLON"
    p[0] = ("array_assign", p[1], p[3], p[6])


def p_exp_unary_operation(p):
    """exp : INCREMENT IDENTIFIER SEMICOLON
    | IDENTIFIER INCREMENT SEMICOLON %prec POST_INCREMENT
    | DECREMENT IDENTIFIER SEMICOLON
    | IDENTIFIER DECREMENT SEMICOLON %prec POST_DECREMENT"""
    if p.slice[1].type == "IDENTIFIER":
        p[0] = (p.slice[2].type.lower(), p[1], True)
    else:
        p[0] = (p.slice[1].type.lower(), p[2], False)


def p_print(p):
    """exp : PRINT LPAREN RHS RPAREN SEMICOLON"""
    p[0] = ("print", p[3])


def p_println(p):
    """exp : PRINTLN LPAREN RHS RPAREN SEMICOLON"""
    p[0] = ("println", p[3])


def p_optargs(p):
    "optargs : args"
    p[0] = p[1]  # the work happens in "args"


def p_optargsempty(p):
    "optargs : "
    p[0] = []  # no arguments -> return the empy list


def p_args(p):
    "args : RHS COMMA args"
    p[0] = [p[1]] + p[3]


def p_args_last(p):  # one argument
    "args : RHS"
    p[0] = [p[1]]


def p_var_type(p):
    """var_type : INT
    | DOUBLE
    | BOOL
    | STRING_TYPE
    | CHAR_TYPE"""
    p[0] = p[1]


def p_paren(p):
    "RHS : LPAREN RHS RPAREN"
    p[0] = p[2]


def p_binary_operation(p):
    """RHS : RHS PLUS RHS
    | RHS MINUS RHS
    | RHS TIMES RHS
    | RHS DIVIDE RHS
    | RHS MOD RHS"""
    p[0] = ("arithematic_operation", p[2], p[1], p[3])


def p_unary_operation(p):
    """RHS : INCREMENT IDENTIFIER
    | IDENTIFIER INCREMENT %prec POST_INCREMENT
    | DECREMENT IDENTIFIER
    | IDENTIFIER DECREMENT %prec POST_DECREMENT
    | MINUS RHS %prec UMINUS"""
    tokens
    if p[1] == "-":
        p[0] = ("uminus", p[2])
        return
    if p.slice[1].type == "IDENTIFIER":
        p[0] = (p.slice[2].type.lower(), p[1], True)
    else:
        p[0] = (p.slice[1].type.lower(), p[2], False)


def p_identifier(p):
    """RHS : IDENTIFIER
    | IDENTIFIER LBRACK INT_NUMBER RBRACK"""
    try:
        if p[2]:
            p[0] = ("array_identifier", p[1], p[3])
    except IndexError:
        p[0] = ("identifier", p[1])


def p_string(p):
    "RHS : STRING"
    p[0] = ("String", p[1])


def p_char(p):
    "RHS : CHAR"
    p[0] = ("char", p[1])


def p_number(p):
    """RHS : INT_NUMBER
    | DOUBLE_NUMBER"""
    if type(p[1]) is int:
        p[0] = ("int", p[1])
    else:
        p[0] = ("double", p[1])


def p_boolVal(p):
    """RHS : TRUE
    | FALSE"""
    p[0] = ("boolean", p[1])


def p_error(p):
    raise SyntaxError("Syntax error!")


# Build the parser
parser = yacc.yacc()

# For running the parser on its own
if __name__ == "__main__":
    while True:
        try:
            s = input("parser > ")
        except EOFError:
            break

        if not s:
            continue

        if s == "exit":
            break

        try:
            result = parser.parse(s)
        except SyntaxError as e:
            print(e)
            continue

        print(result)
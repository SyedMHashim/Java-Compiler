import ply.lex as lex

tokens = [
    "INT",  # int
    "DOUBLE",  # double
    "BOOL",  # bool
    "STRING_TYPE",  # string
    "CHAR_TYPE",  # char
    "IDENTIFIER",  # var/function name
    "EQUAL",  # =
    "INT_NUMBER",  # 1234
    "DOUBLE_NUMBER",  # 5.678
    "STRING",  # "this is a string"
    "CHAR",  # 'a'
    "TRUE",  # true
    "FALSE",  # false
    "LBRACE",  # {
    "RBRACE",  # }
    "SEMICOLON",  # ;
    "MINUS",  # -
    "PLUS",  # +
    "TIMES",  # *
    "DIVIDE",  # /
    "MOD",  # %
    "INCREMENT",  # ++
    "DECREMENT",  # --
    "LPAREN",  # (
    "RPAREN",  # )
    "LBRACK",  # [
    "RBRACK",  # ]
    "COMMA",  # ,
    "NEW",  # new
    "PRINT",
    "PRINTLN",
]

t_ignore = " \t\v\r"


def t_NEW(t):
    r"new"
    return t


def t_INT(t):
    r"int"
    return t


def t_DOUBLE(t):
    r"double"
    return t


def t_BOOL(t):
    r"boolean"
    return t


def t_STRING_TYPE(t):
    r"String"
    return t


def t_CHAR_TYPE(t):
    r"char"
    return t


def t_TRUE(t):
    r"true"
    return t


def t_FALSE(t):
    r"false"
    return t


def t_PRINTLN(t):
    r"System.out.println"
    return t


def t_PRINT(t):
    r"System.out.print"
    return t


def t_IDENTIFIER(t):
    r"[A-Za-z][A-Za-z0-9_]*"
    return t


def t_EQUAL(t):
    r"="
    return t


def t_DOUBLE_NUMBER(t):
    r"[0-9]+(?:\.[0-9]*)"
    t.value = float(t.value)
    return t


def t_INT_NUMBER(t):
    r"[0-9]+"
    t.value = int(t.value)
    return t


def t_CHAR(t):
    r"(?:\'[^(?:\')](?:\'))"
    t.value = t.value[1:-1]
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_SEMICOLON(t):
    r";"
    return t


def t_INCREMENT(t):
    r"\+\+"
    return t


def t_DECREMENT(t):
    r"--"
    return t


def t_MINUS(t):
    r"-"
    return t


def t_PLUS(t):
    r"\+"
    return t


def t_TIMES(t):
    r"\*"
    return t


def t_DIVIDE(t):
    r"/"
    return t


def t_MOD(t):
    r"%"
    return t


def t_LPAREN(t):
    r"\("
    return t


def t_RPAREN(t):
    r"\)"
    return t


def t_RBRACE(t):
    r"\}"
    return t


def t_LBRACE(t):
    r"\{"
    return t


def t_RBRACK(t):
    r"\]"
    return t


def t_LBRACK(t):
    r"\["
    return t


# t_GE =  r'>='
# t_GT =   r'>'
# t_LE =  r'<='
# t_LT = r'<'


def t_COMMA(t):
    r"\,"
    return t


def t_newline(t):
    r"\n"
    t.lexer.lineno += 1


def t_error(t):
    pass


# Build the lexer
lexer = lex.lex()

# For running the lexer on its own
if __name__ == "__main__":
    while True:
        try:
            s = input("lexer > ")
        except EOFError:
            break

        if not s:
            continue

        if s == "exit":
            break

        lexer.input(s)
        for token in lexer:
            print(token)
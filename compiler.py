import sys
import ply.lex as lex
import ply.yacc as yacc


# ###########################################################################
# ############################---LEXER FOR JAVA---##########################


start = 'exp'

precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right','INCREMENT', 'DECREMENT','UMINUS'),
        ('nonassoc', 'POST_INCREMENT','POST_DECREMENT'),
        ('left', 'LPAREN', 'RPAREN'),
)

tokens = (
    'INT',          # int
    'DOUBLE',       # double
    'BOOL',         # bool
    'STRING_TYPE',  # string
    'CHAR_TYPE',    # char
    'IDENTIFIER',   # var/function name
    'EQUAL',        # =
    'INT_NUMBER',   # 1234
    'DOUBLE_NUMBER',# 5.678
    'STRING',       # "this is a string"
    'CHAR',         # 'a'
    'TRUE',         # true
    'FALSE',        # false
    # 'IF',           # if
    # 'ELSE',         # else
    # 'FOR',          # for
    'LBRACE',       # {
    'RBRACE',       # }
    'SEMICOLON',    # ;
    'MINUS',        # -
    'PLUS',         # +
    'TIMES',        # *
    'DIVIDE',       # /
    'MOD',          # %
    'INCREMENT',    # ++
    'DECREMENT',    # --
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACK',       # [
    'RBRACK',       # ]
    # 'GT',           # >
    # 'GE',           # >=
    # 'LT',           # <
    # 'LE',           # <=
    'COMMA',        # ,
    'NEW',          # new
    'PRINT',
    'PRINTLN',
)

t_ignore = ' \t\v\r'

def t_NEW(t):
    r'new'
    return t

def t_INT(t):
    r'int'
    return t

def t_DOUBLE(t):
    r'double'
    return t

def t_BOOL(t):
    r'boolean'
    return t

def t_STRING_TYPE(t):
    r'String'
    return t

def t_CHAR_TYPE(t):
    r'char'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

# def t_IF(t):
#     r'if'
#     return t

# def t_ELSE(t):
#     r'else'
#     return t

# def t_FOR(t):
#     r'for'
#     return t

def t_PRINTLN(t):
    r'System.out.println'
    return t

def t_PRINT(t):
    r'System.out.print'
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    return t

def t_EQUAL(t):
    r'='
    return t

def t_DOUBLE_NUMBER(t):
    r'[0-9]+(?:\.[0-9]*)'
    t.value = float(t.value)
    return t

def t_INT_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r'(?:\'[^(?:\')](?:\'))'
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_INCREMENT(t):
    r'\+\+'
    return t

def t_DECREMENT(t):
    r'--'
    return t

def t_MINUS(t):
    r'-'
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return  t

def t_MOD(t):
    r'%'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_RBRACE(t):
    r'\}'
    return t

def t_LBRACE(t):
    r'\{'
    return t

def t_RBRACK(t):
    r'\]'
    return t

def t_LBRACK(t):
    r'\['
    return t

# t_GE =  r'>='
# t_GT =   r'>'
# t_LE =  r'<='
# t_LT = r'<'

def t_COMMA(t):
    r'\,'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    pass

# ###########################################################################
# ############################---PARSER FOR JAVA---##########################

def p_exp_declaration(p):
    'exp : varType IDENTIFIER SEMICOLON'
    p[0] = ("declare", p[1], p[2])

def p_exp_initialization(p):
    'exp : varType IDENTIFIER EQUAL RHS SEMICOLON'
    p[0] = ('initialize', p[1], p[2], p[4])

def p_exp_assignment(p):
    'exp : IDENTIFIER EQUAL RHS SEMICOLON'
    p[0] = ('assign', p[1],p[3])

def p_array_declaration(p):
    '''exp : varType LBRACK RBRACK IDENTIFIER SEMICOLON
           | varType IDENTIFIER LBRACK RBRACK SEMICOLON'''
    if p[2] == '[':
        p[0] = ("arrayDeclare", p[1],p[4])
    else:
        p[0] = ("arrayDeclare", p[1],p[2])

def p_array_instantiation(p):
    'exp : IDENTIFIER EQUAL NEW varType LBRACK INT_NUMBER RBRACK SEMICOLON'
    p[0] = ('instantiation',p[1],p[4],p[6])

def p_array_declaration_instantiation(p):
    '''exp : varType LBRACK RBRACK IDENTIFIER EQUAL NEW varType LBRACK INT_NUMBER RBRACK SEMICOLON
           | varType IDENTIFIER LBRACK RBRACK EQUAL NEW varType LBRACK INT_NUMBER RBRACK SEMICOLON'''
    if p[2] == '[':
        p[0] = ('arrayDeclaration_instantiation', p[1], p[4], p[7], p[9])
    else:
        p[0] = ('arrayDeclaration_instantiation', p[1], p[2], p[7], p[9])

def p_array_initialization(p):
    '''exp : varType IDENTIFIER LBRACK RBRACK EQUAL LBRACE optargs RBRACE SEMICOLON
           | varType LBRACK RBRACK IDENTIFIER EQUAL LBRACE optargs RBRACE SEMICOLON'''
    if p[2] == '[':
        p[0] = ("arrayInitialize", p[1], p[4], p[7])
    else:
        p[0] = ("arrayInitialize", p[1], p[2], p[7])

def p_array_assignment(p):
    'exp : IDENTIFIER LBRACK INT_NUMBER RBRACK EQUAL RHS SEMICOLON'
    p[0] = ("arrayAssignment",p[1],p[3],p[6])

def p_exp_unOp(p):
    '''exp : INCREMENT IDENTIFIER SEMICOLON
           | IDENTIFIER INCREMENT SEMICOLON %prec POST_INCREMENT
           | DECREMENT IDENTIFIER SEMICOLON
           | IDENTIFIER DECREMENT SEMICOLON %prec POST_DECREMENT'''
    if p[1]=='++' or p[1]=='--':
        p[0] = ('unop', p[1], ('identifier',p[2]))
    else:
        p[0] = ('unop', ('identifier',p[1]),  p[2])

def p_print(p):
    '''exp : PRINT LPAREN RHS RPAREN SEMICOLON
           | PRINTLN LPAREN RHS RPAREN SEMICOLON'''
    p[0] = (p[1], p[3])

def p_optargs(p):
    'optargs : args'
    p[0] = p[1] # the work happens in "args"

def p_optargsempty(p):
    'optargs : '
    p[0] = [] # no arguments -> return the empy list

def p_args(p):
    'args : RHS COMMA args'
    p[0] = [p[1]] + p[3]

def p_args_last(p): # one argument
    'args : RHS'
    p[0] = [p[1]]

def p_var_type(p):
    '''varType : INT
              | DOUBLE
              | BOOL
              | STRING_TYPE
              | CHAR_TYPE'''
    p[0] = p[1]

def p_paren(p):
    'RHS : LPAREN RHS RPAREN'
    p[0] = p[2]

def p_binary_operation(p):
    '''RHS : RHS PLUS RHS
           | RHS MINUS RHS
           | RHS TIMES RHS
           | RHS DIVIDE RHS
           | RHS MOD RHS'''
    p[0] = ('binop',p[1],p[2],p[3])

def p_unary_operations(p):
    '''RHS : INCREMENT IDENTIFIER
           | IDENTIFIER INCREMENT %prec POST_INCREMENT
           | DECREMENT IDENTIFIER
           | IDENTIFIER DECREMENT %prec POST_DECREMENT
           | MINUS RHS %prec UMINUS'''
    if p[1] == '-':
        p[0] = ('unop', p[1], p[2])
    elif p[1]=='++' or p[1]=='--':
        p[0] = ('unop', p[1], ('identifier',p[2]))
    else:
        p[0] = ('unop', ('identifier',p[1]),  p[2])

def p_identifier(p):
    '''RHS : IDENTIFIER
           | IDENTIFIER LBRACK INT_NUMBER RBRACK'''
    try:
        if p[2]:
            p[0] = ('arrayIdentifier', p[1], p[3])
    except IndexError:
        p[0] = ('identifier', p[1])

def p_string(p):
    'RHS : STRING'
    p[0] = ('String', p[1])

def p_char(p):
    'RHS : CHAR'
    p[0] = ('char', p[1])

def p_number(p):
    '''RHS : INT_NUMBER
           | DOUBLE_NUMBER'''
    if type(p[1]) is int:
        p[0] = ('int',p[1])
    else:
        p[0] = ('double',p[1])

def p_boolVal(p):
    '''RHS : TRUE
           | FALSE'''
    p[0] = ('boolean',p[1])

def p_error(p):
    print str(lineno) + ':Syntax error!'


##################################################################
###################--INTERPRETER FOR JAVA--#######################

uninitialized = []
initialized = []

def eval_exp(tree):
    nodetype = tree[0]
    if nodetype == 'int' or nodetype == 'double' or nodetype == 'String' or nodetype == 'char' or nodetype == 'boolean':
        return tree
    elif nodetype == 'identifier':
        for _,y,_ in uninitialized:
            if y == tree[1]:
                print str(lineno)+':'+'error: variable '+tree[1]+' might not have been initialized'
                return False
        for _,y,z in initialized:
            if y == tree[1]:
                if type(z) is list:
                    return ('list',z)
                else:
                    return z
        print str(lineno)+':'+'error: cannot find symbol'
        return False
    elif nodetype == 'declare':
        for _,y,_ in uninitialized:
            if y == tree[2]:
                print str(lineno)+':'+'error: variable '+tree[2]+' is already defined'
                return False
        for _,y,_ in initialized:
            if y == tree[2]:
                print str(lineno)+':'+'error: variable '+ tree[2]+ ' is already defined'
                return False
        uninitialized.append((tree[1], tree[2],None))
        return True
    elif nodetype == 'assign':
        for x,y,z in uninitialized:
            if y == tree[1]:
                rhs = eval_exp(tree[2])

                if rhs:
                    if x == rhs[0]:
                        uninitialized.remove((x, y, None))
                        initialized.append((x, y, rhs))
                    elif x == 'double' and rhs[0] == 'int':
                        uninitialized.remove((x, y, None))
                        initialized.append((x, y, ('double', float(rhs[1]))))
                    elif x == 'char' and rhs[0] == 'int':
                        uninitialized.remove((x, y, None))
                        initialized.append((x, y, ('char', chr(rhs[1]))))
                    elif (x == 'double' or x == 'int') and rhs[0] == 'char':
                        v = ord(rhs[1])
                        if x == 'double':
                            uninitialized.remove((x, y, None))
                            initialized.append((x, y, ('double', float(v))))
                        else:
                            uninitialized.remove((x, y, None))
                            initialized.append((x, y, ('int', v)))
                    else:
                        print str(lineno) + ':' + 'error: Incompatible types'
                        return False
                else:
                    return False
                return True
        for x,y,z in initialized:
            if y == tree[1]:
                rhs = eval_exp(tree[2])
                if rhs:
                    if x == rhs[0]:
                        initialized.remove((x, y, z))
                        initialized.append((x, y, rhs))
                    elif x == 'double' and rhs[0] == 'int':
                        initialized.remove((x, y, z))
                        initialized.append((x, y, ('double', float(rhs[1]))))
                    elif x == 'char' and rhs[0] == 'int':
                        initialized.remove((x, y, z))
                        initialized.append((x, y, ('char', chr(rhs[1]))))
                    elif (x == 'double' or x == 'int') and rhs[0] == 'char':
                        v = ord(rhs[1])
                        if x == 'double':
                            initialized.remove((x, y, z))
                            initialized.append((x, y, ('double', float(v))))
                        else:
                            initialized.remove((x, y, z))
                            initialized.append((x, y, ('int', v)))
                    else:
                        print str(lineno) + ':' + 'error: Incompatible types'
                        return False
                else:
                    return False
                return True
        print str(lineno)+':'+'error: cannot find symbol'
        return False
    elif nodetype == 'initialize':
        return eval_exp(('declare',tree[1],tree[2])) and eval_exp(('assign', tree[2],tree[3]))
    elif nodetype == 'arrayIdentifier':
        for x,y,z in uninitialized:
            if y == tree[1]:
                if type(z) is list:
                    print str(lineno)+':'+'error: variable '+y+' might not have been initialized'
                else:
                    print str(lineno)+':'+'error: array required but '+ x+' found'
                return False
        for x,y,z in initialized:
            if y == tree[1]:
                if type(z) is list:
                    try:
                        return z[tree[2]]
                    except IndexError:
                        print str(lineno)+':'+'IndexError: index out of bound'
                        return False
                else:
                    print str(lineno) + ':' + 'error: array required but ' + x + ' found'
                    return False
        print str(lineno)+':'+'error: cannot find symbol'
        return False
    elif nodetype == 'arrayDeclare':
        for _,y,_ in uninitialized:
            if y == tree[2]:
                print str(lineno)+':'+'error: variable '+tree[2]+' is already defined'
                return False
        for _,y,_ in initialized:
            if y == tree[2]:
                print str(lineno)+':'+'error: variable '+ tree[2]+ ' is already defined'
                return False
        uninitialized.append((tree[1], tree[2], []))
        return True
    elif nodetype == 'instantiation':
        for x,y,z in uninitialized:
            if y == tree[1]:
                if type(z) is not list or x!=tree[2]:
                    print str(lineno) + ':' + 'error: Incompatible types'
                    return False
                t = tree[2]
                l = tree[3]
                uninitialized.remove((x,y,z))
                for i in range(l):
                    if t == 'int':
                        z.append((t,0))
                    elif t == 'double':
                        z.append((t,0.0))
                    elif t == 'String':
                        z.append((t,'null'))
                    elif t == 'boolean':
                        z.append((t,'false'))
                    else:
                        z.append((t,'.'))
                initialized.append((x,y,z))
                return True
        for x,y,z in initialized:
            if y == tree[1]:
                if type(z) is not list or x != tree[2]:
                    print str(lineno) + ':' + 'error: Incompatible types'
                    return False
                t = tree[2]
                l = tree[3]
                initialized.remove((x, y, z))
                z = []
                for i in range(l):
                    if t == 'int':
                        z.append((t, 0))
                    elif t == 'double':
                        z.append((t, 0.0))
                    elif t == 'String':
                        z.append((t, 'null'))
                    elif t == 'boolean':
                        z.append((t, 'false'))
                    else:
                        z.append((t, '.'))
                initialized.append((x, y, z))
                return True
        print str(lineno)+':'+'error: cannot find symbol'
        return False
    elif nodetype == 'arrayDeclaration_instantiation':
        return eval_exp(('arrayDeclare',tree[1],tree[2])) and eval_exp(('instantiation',tree[2],tree[3],tree[4]))
    elif nodetype == "arrayInitialize":
        boolean = True
        boolean = boolean and eval_exp(('arrayDeclaration_instantiation',tree[1],tree[2],tree[1],len(tree[3])))
        if boolean:
            for i in range(len(tree[3])):
                boolean = boolean and eval_exp(('arrayAssignment',tree[2],i,tree[3][i]))
                if not boolean:
                    return boolean
        return boolean
    elif nodetype == 'arrayAssignment':
        for x,y,z in uninitialized:
            if y == tree[1]:
                if type(z) is not list:
                    print str(lineno) + ':' + 'error: array required but ' + x + ' found'
                    return False
                rhs = eval_exp(tree[3])
                t = rhs[0]
                v = rhs[1]
                if x == t:
                    uninitialized.remove((x, y, z))
                    z[tree[2]]=rhs
                    initialized.append((x, y, z))
                elif x == 'double' and t == 'int':
                    uninitialized.remove((x, y,z))
                    z[tree[2]]=('double',float(v))
                    initialized.append((x, y, z))
                elif x == 'char' and t == 'int':
                    uninitialized.remove((x, y, z))
                    z[tree[2]]=('char', chr(v))
                    initialized.append((x, y, z))
                elif (x == 'double' or x == 'int') and t == 'char':
                    v = ord(v)
                    if x == 'double':
                        uninitialized.remove((x, y,z))
                        z[tree[2]] = ('double', float(v))
                        initialized.append((x, y, z))
                    else:
                        uninitialized.remove((x, y,z))
                        z[tree[2]]=('int', v)
                        initialized.append((x, y, z))
                else:
                    print str(lineno)+':'+'error: Incompatible types'
                    return False
                return True
        for x,y,z in initialized:
            if y == tree[1]:
                if type(z) is not list:
                    print str(lineno) + ':' + 'error: array required but ' + x + ' found'
                    return False
                rhs = eval_exp(tree[3])
                t = rhs[0]
                v = rhs[1]
                if x == t:
                    initialized.remove((x, y, z))
                    z[tree[2]] = rhs
                    initialized.append((x, y, z))
                elif x == 'double' and t == 'int':
                    initialized.remove((x, y, z))
                    z[tree[2]] = ('double', float(v))
                    initialized.append((x, y, z))
                elif x == 'char' and t == 'int':
                    initialized.remove((x, y, z))
                    z[tree[2]] = ('char', chr(v))
                    initialized.append((x, y, z))
                elif (x == 'double' or x == 'int') and t == 'char':
                    v = ord(v)
                    if x == 'double':
                        initialized.remove((x, y, z))
                        z[tree[2]] = ('double', float(v))
                        initialized.append((x, y, z))
                    else:
                        initialized.remove((x, y, z))
                        z[tree[2]] = ('int', v)
                        initialized.append((x, y, z))
                else:
                    print str(lineno) + ':' + 'error: Incompatible types'
                    return False
                return True
        print str(lineno)+':'+'error: cannot find symbol'
        return False
    elif nodetype == 'unop':
        if tree[1] == '-':
            val = eval_exp(tree[2])
            if val:
                if val[0]=='double' or val[0] == 'int':
                    return (val[0],-val[1])
                elif val[0]=='char':
                    return ('int' ,-ord(val[1]))
                else:
                    print str(lineno)+':'+'error: bad operand type'
                    return False
        elif tree[1] == '--':
            val = eval_exp(tree[2])
            if val:
                if val[0]=='double' or val[0] == 'int':
                    temp = (val[0],val[1] - 1)
                    eval_exp(('assign',tree[2][1],temp))
                    return temp
                elif val[0] =='char':
                    temp = ord(val[1]) - 1
                    char = ('char',chr(temp))
                    eval_exp(('assign',tree[2][1],char))
                    return char
                else:
                    print str(lineno)+':'+'error: bad operand type'
                    return False
        elif tree[1] == '++':
            val = eval_exp(tree[2])
            if val:
                if val[0]=='double' or val[0] == 'int':
                    temp = (val[0],val[1] + 1)
                    eval_exp(('assign',tree[2][1],temp))
                    return temp
                elif val[0] =='char':
                    temp = ord(val[1]) + 1
                    char = ('char',chr(temp))
                    eval_exp(('assign',tree[2][1],char))
                    return char
                else:
                    print str(lineno)+':'+'error: bad operand type'
                    return False
        elif tree[2] == '--':
            val = eval_exp(tree[1])
            if val:
                if val[0]=='double' or val[0] == 'int':
                    temp = (val[0],val[1] - 1)
                    eval_exp(('assign',tree[1][1],temp))
                    return val
                elif val[0] =='char':
                    temp = ord(val[1]) - 1
                    char = ('char',chr(temp))
                    eval_exp(('assign',tree[1][1],char))
                    return val
                else:
                    print str(lineno)+':'+'error: bad operand type'
                    return False
        elif tree[2] == '++':
            val = eval_exp(tree[1])
            if val:
                if val[0]=='double' or val[0] == 'int':
                    temp = (val[0],val[1] + 1)
                    eval_exp(('assign',tree[1][1],temp))
                    return val
                elif val[0] =='char':
                    temp = ord(val[1]) + 1
                    char = ('char',chr(temp))
                    eval_exp(('assign',tree[1][1],char))
                    return val
                else:
                    print str(lineno)+':'+'error: bad operand type'
                    return False
    elif nodetype == 'binop':
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        left_val = eval_exp(left_child)
        right_val = eval_exp(right_child)
        if left_val and right_val:
            if operator == '+':
                if left_val[0]=='char' and right_val[0]=='char':
                    return ('int', ord(left_val[1]) + ord(right_val[1]))
                elif type(left_val[1]) is str and type(right_val[1]) is str:
                    return ('String',left_val[1] + right_val[1])
                elif left_val[0]=='String' or right_val[0]=='String' or left_val[0]=='boolean' or right_val[0]=='boolean':
                    print str(lineno)+':'+'error: bad operand type'
                    return False
                else:
                    if left_val[0]=='char':
                        left_val = ('int',ord(left_val[1]))
                    if right_val[0]=='char':
                        right_val = ('int',ord(right_val[1]))

                    if left_val[0]=='double' or right_val[0]=='double':
                        return ('double',left_val[1] + right_val[1])
                    else:
                        return ('int', left_val[1]+right_val[1])
            elif operator == '-':
                if left_val[0]=='String' or right_val[0]=='String' or left_val[0]=='boolean' or right_val[0]=='boolean':
                    print str(lineno)+':'+'error: bad operand type'
                    return False
                else:
                    if left_val[0]=='char':
                        left_val = ('int',ord(left_val[1]))
                    if right_val[0]=='char':
                        right_val = ('int',ord(right_val[1]))

                    if left_val[0]=='double' or right_val[0]=='double':
                        return ('double',left_val[1] - right_val[1])
                    else:
                        return ('int', left_val[1]-right_val[1])
            elif operator == '*':
                if left_val[0]=='String' or right_val[0]=='String' or left_val[0]=='boolean' or right_val[0]=='boolean':
                    print str(lineno)+':'+'error: bad operand type'
                    return False
                else:
                    if left_val[0]=='char':
                        left_val = ('int',ord(left_val[1]))
                    if right_val[0]=='char':
                        right_val = ('int',ord(right_val[1]))

                    if left_val[0]=='double' or right_val[0]=='double':
                        return ('double',left_val[1] * right_val[1])
                    else:
                        return ('int', left_val[1]*right_val[1])
            elif operator == '/':
                if left_val[0]=='String' or right_val[0]=='String' or left_val[0]=='boolean' or right_val[0]=='boolean':
                    print str(lineno)+':'+'error: bad operand type'
                    return False
                else:
                    if left_val[0]=='char':
                        left_val = ('int',ord(left_val[1]))
                    if right_val[0]=='char':
                        right_val = ('int',ord(right_val[1]))

                    try:
                        if left_val[0]=='double' or right_val[0]=='double':
                            return ('double',left_val[1] / right_val[1])
                        else:
                            return ('int', left_val[1]/right_val[1])
                    except ZeroDivisionError:
                        print str(lineno)+':'+'error: Zero Division Error'
                        return False
            elif operator == '%':
                if left_val[0]=='String' or right_val[0]=='String' or left_val[0]=='boolean' or right_val[0]=='boolean':
                    print str(lineno)+':'+'error: bad operand type'
                    return False
                else:
                    if left_val[0]=='char':
                        left_val = ('int',ord(left_val[1]))
                    if right_val[0]=='char':
                        right_val = ('int',ord(right_val[1]))

                    if left_val[0]=='double' or right_val[0]=='double':
                        return ('double',left_val[1] % right_val[1])
                    else:
                        return ('int', left_val[1]%right_val[1])
    elif nodetype == 'System.out.print':
        if not error:
            val = eval_exp(tree[1])
            if val:
                sys.stdout.write(str(val[1]))
                sys.stdout.flush()
                return True
            else:
                return False
    elif nodetype == 'System.out.println':
        if not error:
            val = eval_exp(tree[1])
            if val:
                print val[1]
                return True
            else:
                return False


#################################################################################
##################################--TESTING--####################################


f = open(sys.argv[1],'r')
text = f.read()
f.close()
text = text.split('\n')
error = False
lineno = 1
for expression in text:
    jslexer = lex.lex()
    jsparser = yacc.yacc()
    jsast = jsparser.parse(expression,lexer=jslexer)

    if jsast:
        error = not eval_exp(jsast)
        if error:
            break
    else:
        break
    lineno+=1


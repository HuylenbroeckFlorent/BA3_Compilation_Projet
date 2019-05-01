import ply.lex as lex

tokens = ('NUMBER','ADD_OP', 'MUL_OP')

t_ADD_OP = r'\+|-'
t_MUL_OP = r'\*|/'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_ignore = ' |\t'

def t_error(t):
    print("Illegal char '%s'" %t.value[0])
    t.lexer.skip(1)
    
if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
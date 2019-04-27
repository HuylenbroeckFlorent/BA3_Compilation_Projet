import ply.lex as lex
import queue

states = (
         ('BLOCK', 'inclusive'),
         ('STRING', 'inclusive'),
         )

tokens = (
        #Partie DATA
        'BLOCKstart', 'BLOCKend', 
        'AFFECT', 'VARIABLE', 'SEMICOLON', 'COMA', 'LPAREN', 'RPAREN', 'APOSTROPHE', 'STR',
        #Partie TEMPLATE
        'ADD_OP', 'MUL_OP', 'newline'
         )

t_ADD_OP = r'\+|-'
t_MUL_OP = r'\*|/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMA = r','
t_ignore = ' \t' 

def t_BLOCKstart(t):
    r'{{'
    t.lexer.begin('BLOCK')
    return t

def t_BLOCK_BLOCKend(t):
    r'}}'
    t.lexer.begin('INITIAL')
    return t

def t_BLOCK_AFFECT(t):
    r':='
    return t

def t_BLOCK_VARIABLE(t):
    r'[a-zA-Z0-9_]+\w*'  #Ou juste r'\w+' ?
    return t             #Penser à également virer les nom de variables réservés (comme "for")

def t_BLOCK_SEMICOLON(t):
    r';'
    return t

def t_BLOCK_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_BLOCK_APOSTROPHE(t):
    r'\''
    t.lexer.begin('STRING')
    return t

def t_STRING_APOSTROPHE(t):
    r'\''
    t.lexer.begin('BLOCK')
    
def t_STRING_STR(t):
    r"[^']+"  #tout jusqu'à '
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno =+ len(t.value)   

def t_error(t):
    print("Illegal char '%s'" %t.value[0])
    t.lexer.skip(1)

if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))


"""
def isWellParent(lexer):
    nopen=0
    for token in lexer:
        print("line %d : %s (%s) " %(token.lineno,token.type,token.value))
        #print(nopen)
        if (token.type == 'LPAREN'):
            nopen=nopen+1
        elif (token.type == 'RPAREN'):
            if(nopen>0):
                nopen=nopen-1
            else:
                return False
    return (nopen == 0)
""" 
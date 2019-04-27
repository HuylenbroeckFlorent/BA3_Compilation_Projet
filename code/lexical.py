import ply.lex as lex
import queue

npar = 0

states = (
         ('BLOCK', 'inclusive'),
         ('STRING', 'inclusive'),
         )

tokens = (
        'TXT'
        #Partie DATA
        'BLOCKstart', 'BLOCKend', 
        'AFFECT', 'VARIABLE', 'SEMICOLON', 'COMA', 'LPAREN', 'RPAREN', 'APOSTROPHE', 'STR',
        #Partie TEMPLATE
        'ADD_OP', 'MUL_OP' 
        #, 'newline'
         )

t_ADD_OP = r'\+|-'
t_MUL_OP = r'\*|/'
t_COMA = r','
t_BLOCK_ignore = ' \t'

def t_BLOCK_LPAREN(t):
    r'\('
    global npar
    npar+=1
    return t

def t_BLOCK_RPAREN(t):
    r'\)'
    global npar
    npar-=1
    return t

def t_BLOCKstart(t):
    r'{{'
    t.lexer.begin('BLOCK')
    return t

def t_BLOCK_BLOCKend(t):
    r'}}'
    t.lexer.begin('INITIAL')
    global npar
    if(npar!=0):
        print(' /!\WARNING:',npar,"parenthesis not closed!")
    npar=0
    return t

def t_BLOCK_AFFECT(t):
    r':='
    return t

def t_BLOCK_VARIABLE(t):
    r'[a-zA-Z0-9_]+\w*'  #Ou juste r'\w+' ?
    return t             #Penser à également virer les nom de variables réservées (comme "for")

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
    r"[^']+"  #tout jusqu'à ', need peut être un gestionnaire d'erreur au cas où pas de '
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno =+ len(t.value)   

def t_TXT(t):
    r'[^({{)]+'
    return t

def t_STRING_error(t):
    print("Illegal char '%s'" %t.value[0])
    t.lexer.skip(1)  

def t_BLOCK_error(t):
    print("Illegal char '%s'" %t.value[0])
    t.lexer.skip(1)
    
def t_error(t):
    print("Illegal char '%s'" %t.value[0])
    t.lexer.skip(1)

if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))

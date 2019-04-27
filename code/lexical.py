import ply.lex as lex
import queue

states = (
         ('BLOCK', 'inclusive'),
         ('STRING', 'inclusive'),
         )

tokens = (
        'BLOCKstart', 'BLOCKend', 
        'ADD_OP', 'MUL_OP', 'AFFECT',
        'VAR', 'SEMICOLON'
         )

t_ADD_OP = r'\+|-'
t_MUL_OP = r'\*|/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

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

def t_BLOCK_VAR(t):
    r'[a-zA-Z0-9_]+\w*'  #Ou juste r'\w+' ?
    return t             #Penser à également virer les nom de variables réservés (comme "for")

def t_BLOKC_SEMICOLON(t):
    r';'

def t_BLOCK_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

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
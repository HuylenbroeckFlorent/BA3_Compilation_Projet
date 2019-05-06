import ply.lex as lex

npar = 0


usednames={}  #Les variables
             
states = (
         ('BLOCK', 'inclusive'),
         ('STRING', 'inclusive'),
         )

tokens = (
        'TXT',
        'BLOCKstart', 'BLOCKend', 
        'BOOL', 'ANDOR', 'PRINT', 'FOR', 'IN', 'ENDFOR', 'DO', 'IF', 'ENDIF',
        'AFFECT', 'VARIABLE', 'SEMICOLON', 'COMA', 'LPAREN', 'RPAREN', 'APOSTROPHE', 'STR',
        'INT_OP', 'COMPARE', 'POINT','INT'
         )

t_BLOCK_INT_OP = r'\+|-|\*|/'
t_BLOCK_COMA = r','
t_BLOCK_POINT = r'\.'
t_BLOCK_ignore = ' \t'

def t_BLOCK_IF(t):
    r'if'
    return t

def t_BLOCK_ENDIF(t):
    r'endif'
    return t

def t_BLOCK_COMPARE(t):
    r'<=|>=|<|>|!=|='
    return t

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

def t_BLOCK_INT(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_BLOCKstart(t):
    r'{{'
    t.lexer.begin('BLOCK')
    return t

def t_BLOCK_BOOL(t):
    r'true|false'
    t.value=(t.value == "true")
    return t

def t_BLOCK_ANDOR(t):
    r'and|or'
    return t

def t_BLOCK_PRINT(t):
    r'print'
    return t

def t_BLOCK_FOR(t):
    r'for'
    return t

def t_BLOCK_ENDFOR(t):
    r'endfor'
    return t

def t_BLOCK_IN(t):
    r'in'
    return t

def t_BLOCK_DO(t):
    r'do'
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
    if(t.value in usednames):
        return t
    else:
        usednames[t.value]= None
        return t           

def t_BLOCK_SEMICOLON(t):
    r';'
    return t

def t_BLOCK_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_BLOCK_APOSTROPHE(t):
    r'\''
    t.lexer.begin('STRING')

def t_STRING_APOSTROPHE(t):
    r'\''
    t.lexer.begin('BLOCK')
    
def t_STRING_STR(t):
    r"[^']+"  
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)   

def t_TXT(t):
    r'[^({{)]+'
    t.lexer.lineno += str(t.value).count("\n")
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

lexer = lex.lex()

if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))


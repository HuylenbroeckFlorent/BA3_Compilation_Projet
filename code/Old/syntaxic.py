import ply.lex as lex
import ply.yacc as yacc
from lexical import tokens

operations = {
        '+' : lambda x, y : x+y,
        '-' : lambda x, y : x-y,
        '*' : lambda x, y : x*y,
        '/' : lambda x, y : x/y,
        '>' : lambda x, y : x>y,
        '<' : lambda x, y : x<y,
        '=' : lambda x, y : x==y,
        '!=' : lambda x, y : x!=y,
        '<=' : lambda x, y : x<=y,
        '>=' : lambda x, y : x>=y,
        'and' : lambda x, y : x and y,
        'or' : lambda x, y : x or y,
        }

precedence = (
        ('left','COMPARE'),
        ('left','POINT'),
        ('left','ADD_OP'),
        ('left', 'MUL_OP'),
        ('right', 'COMPARE'),
        )

def finalPrint(t):
    print(t)   #FONCTION TEMPORAIRE
    return t

def p_programme_txt(p):
    '''programme : txt'''
    p[0]=p[1]

def p_programme_txtprog(p):
    '''programme : txt programme'''
    p[0]=p[1]+p[2]

def p_programme_dumboblock(p):
    '''programme : dumbo_bloc'''
    p[0]=p[1]
    
def p_programme_dumboblockprog(p):
    '''programme : dumbo_bloc programme'''
    p[0]=p[1]+p[2]

def p_txt(p):
    '''txt : TXT'''
    p[0]=p[1]
    
def p_dumbo_block(p):
    '''dumbo_bloc : BLOCKstart expression_list BLOCKend'''
    #A FINIR
    return 1

def p_expression_list_exprl(p):
    '''expression_list : expression SEMICOLON expression_list'''
    p[0]=[p[1],p[3]]
    
def p_expression_list(p):
    '''expression_list : expression SEMICOLON'''
    p[0]=[p[1]]
    
def p_expression_print(p):
    '''expression : PRINT string_expression'''
    p[0]=finalPrint(p[2])

def p_expression_forstr(p):
    '''expression : FOR VARIABLE IN string_list DO expression_list ENDFOR'''
    #FOR IMPLEMENTATION
    p[0]=p[2]
    
def p_expression_forvar(p):
    '''expression : FOR VARIABLE IN VARIABLE DO expression_list ENDFOR'''
    #FOR IMPLEMENTATION
    
def p_expression_varstring(p):
    '''expression : VARIABLE AFFECT string_expression'''
    p[0]=1 #Assignement p[0]=("p[1]=p[3]")
    
def p_expression_varlist(p):
    '''expression : VARIABLE AFFECT string_list'''
    
def p_string_expression_string(p):
    '''string_expression : STR'''
    p[0]=str(p[1])
    
def p_string_expression_var(p):
    '''string_expression : VARIABLE'''
    p[0]=p[1] #VARIABLE
    
def p_string_expression_strstr(p):
    '''string_expression : string_expression POINT string_expression'''
    p[0]=p[1]+p[3]
    
def p_string_list(p):
    '''LPAREN string_list_interior RPAREN'''
    p[0]=p[2]
    
def p_string_list_interior(p):
    '''string_list_interior : string COMA string_list_interior'''
    
def p_string_list_interior_end(p):
    '''string_list_interior : STR'''
    p[0]=[str(p[1])]
    
    
def p_error(p):
    print("Yacc Error")
    yacc.error()

yacc.yacc()

if __name__ == "__main__":
	import sys
	lexer = lex.lex()
	lexer.input(sys.stdin.read())
	for token in lexer:
		print("line %d : %s (%s) " % (token.lineno, token.type, token.value))


"""
yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys
    input = file(sys.argv[1]).read()
    result = yacc.parse(input)
    print(result)
"""
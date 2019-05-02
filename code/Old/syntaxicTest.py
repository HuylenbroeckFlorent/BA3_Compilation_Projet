import ply.lex as lex
import ply.yacc as yacc
from lexical import tokens

operations = {
        '+' : lambda x, y : x+y,
        '-' : lambda x, y : x-y,
        '*' : lambda x, y : x*y,
        '/' : lambda x, y : x/y,
        }



def p_programme_txt(p):
    '''programme : txt'''
    p[0]=p[1]

def p_programme_txtprog(p):
    '''programme : txt programme'''
    p[0]=p[1]+p[2]
    
def p_txt(p):
    '''txt : TXT'''
    p[0]=p[1]

def p_programme_and(p):
    '''programme : AND'''
    p[0]=p[1]
    
def p_error(p):
    print("Yacc Error")
    yacc.error()



yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys
    input = file(sys.argv[1]).read()
    result = yacc.parse(input)
    print(result)

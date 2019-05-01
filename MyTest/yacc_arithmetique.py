import ply.yacc as yacc
from lex_arithmetique import tokens

operations = {
'+' : lambda x, y : x+y ,
'-' : lambda x, y : x-y ,
'*' : lambda x, y : x*y ,
'/' : lambda x, y : x/y ,
}

precedence = (
        ("left", "ADD_OP"),
        ("left", "MUL_OP"),
        )

def p_expression_num(p):
    '''expression : NUMBER'''
    p[0]=p[1]
    
def p_expression_op(p):
    '''expression : expression ADD_OP expression
	expression : expression MUL_OP expression'''
    p[0] = operations[p[2]](p[1],p[3])
    
def p_error(p):
    print("Syntax error in line {]".format(p.lineno))
    yacc.error()

#yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys
    input = open(sys.stdin.read(),'r')
    result = yacc.parse(input)
    print(result)
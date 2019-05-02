import ply.lex as lex
import ply.yacc as yacc
from lexical import tokens
from lexical import usednames


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

class VariableNode:
    def __init__(self,v):
        self.v=v
    
    def compute(self):
        if(usednames[self.v] is None):
            raise Exception("Variable ",self.v,"not defined")
        else:
            usednames[self.v]
            
    def __str__(self):
        return "VARIABLE:"+str(self.v)
    
    
class AffectationNode:
    def __init__(self,v,el):
        self.v=v
        self.el=el

    def compute(self):
            usednames[self.v] = self.el.compute()
            return '' 

    def __str__(self):
        return "AFFECT:"+str(self.v)+":="+str(self.el)
    
    
class OperationNode:
    def __init__(self,oper,e_1=None,e_2=None):
        self.oper=oper
        self.e_1=e_1
        self.e_2=e_2

    def compute(self):
        try:
            return operations[self.oper](self.e_1.compute(),self.e_2.compute()) 
        except:
            raise Exception("Error with this operation:",self.e_l,self.oper,self.e_r,".")
                
    def __str__(self):
        return "OPERATION:"+str(self.e_1)+str(self.oper)+str(self.e_2)


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
    result=""
    for elem in p[2]:
        result=result+elem.compute()
    p[0]=result

def p_expression_list_exprl(p):
    '''expression_list : expression SEMICOLON expression_list'''
    p[0]=[p[1],p[3]]
    
def p_expression_list(p):
    '''expression_list : expression SEMICOLON'''
    p[0]=[p[1]]
    
def p_expression_print(p):
    '''expression : PRINT string_expression'''
    print(p[2])
    p[0]=p[2]
    
def p_expression_forstr(p):
    '''expression : FOR VARIABLE IN string_list DO expression_list ENDFOR'''
    #FOR IMPLEMENTATION
    p[0]=p[2]
    
def p_expression_forvar(p):
    '''expression : FOR VARIABLE IN VARIABLE DO expression_list ENDFOR'''
    #FOR IMPLEMENTATION
    p[0]=p[2]
    
def p_expression_varstring(p):
    '''expression : VARIABLE AFFECT string_expression'''
    p[0]=AffectationNode(p[1],p[3])  #Assignement p[0]=("p[1]=p[3]")
    
def p_expression_varlist(p):
    '''expression : VARIABLE AFFECT string_list'''
    p[0]=AffectationNode(p[1],p[3])
    
def p_string_expression_string(p):
    '''string_expression : string'''
    p[0]=p[1]
    
def p_string_expression_var(p):
    '''string_expression : variable'''
    p[0]=p[1] #VARIABLE
    
def p_string_expression_strstr(p):
    '''string_expression : string_expression POINT string_expression''' #A CORRIGER
    p[0]=p[1]+p[3]
    
def p_string_list(p):
    '''string_list : LPAREN string_list_interior RPAREN'''
    p[0]=p[2]
    
def p_string_list_interior(p):
    '''string_list_interior : string COMA string_list_interior'''
    p[0]=[p[1],p[3]]
    
def p_string_list_interior_end(p):
    '''string_list_interior : string'''
    p[0]=[str(p[1])]
    
def p_variable(p):
    '''variable : VARIABLE'''
    p[0]=p[1]
    
def p_string(p):
    '''string : STR'''
    p[0]=p[1]

def p_error(p):
    print("Syntax error line",p.value)


yacc.yacc()

if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
    
    
    
""" #yacc.yacc(outputdir='generated') 
if __name__ == '__main__':
    import sys
    input = open(sys.stdin.read(),'r')
    result = yacc.parse(input)
    print(result)
"""

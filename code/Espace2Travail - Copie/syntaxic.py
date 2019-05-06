import sys
import ply.lex as lex
import ply.yacc as yacc
from lexical import tokens
from lexical import usednames
from abc import ABC, abstractmethod

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
        ('left','INT_OP'),
        ('right', 'COMPARE'),
        )

def execute(inputt):
    #print(str(inputt),type(inputt),"@",usednames)
    if(isinstance(inputt,ExecNode)):
        return inputt.execute()
    elif(isinstance(inputt,str) or isinstance(inputt,int) or isinstance(inputt,bool)):
        return inputt
    else:
        message="Object "+str(inputt)+" "+str(type(inputt))+" here. (should be str int or ExecNode)"
        raise Exception(message)

class ExecNode(ABC):
    @abstractmethod
    def execute(self):
        pass
    
class PrintingNode(ABC):
    pass

#Inutile actuellement, a supprimer
class ThingNode(ExecNode):
    def __init__(self,el):
        self.el=el
        
    def execute(self):
        return self.el
    
    def __str__(self):
        return "[THING:"+str(self.el)+"]"

class VariableNode(ExecNode):
    def __init__(self,v):
        self.v=v
    
    def execute(self):
        if(usednames[self.v] is None):
            message="Variable "+str(self.v)+" has no value"
            raise Exception(message)
        else:
            return usednames[self.v]
            
    def __str__(self):
        return "VARIABLE:"+str(self.v)
    
    
class AffectationNode(ExecNode):
    def __init__(self,v,el):
        #print("    Affect-> ",v," := ",el, "(type: ",type(el),")")
        self.v=v
        self.el=el
        
    def execute(self):
        usednames[self.v]=execute(self.el)
        return '' 

    def __str__(self):
        return "AFFECT:"+str(self.v)+":="+str(self.el)
    
    
class OperationNode(ExecNode):
    def __init__(self,e_1,oper,e_2):
        self.e_1=e_1
        self.oper=oper
        self.e_2=e_2

    def execute(self):
        try:
            aoa=operations[self.oper](execute(self.e_1),execute(self.e_2)) 
            return aoa
        except:
            message="Error with this operation: "+str(self.e_l)+str(self.oper)+str(self.e_r)+" !"
            raise Exception(message)
                
    def __str__(self):
        return "OPERATION:"+str(self.e_1)+str(self.oper)+str(self.e_2)

class ConcatNode(ExecNode):
    def __init__(self,e_1,e_2):
        self.e_1=e_1
        self.e_2=e_2
    
    def execute(self):
        return str(execute(self.e_1))+str(execute(self.e_2))
    
    def __str__(self):
        return "CONCAT:<"+str(self.e_1)+">,<" + str(self.e_2)+">"
    
class ListNode(ExecNode):
    def __init__(self,el):
        self.el=el
        
    def execute(self):
        return self.el
    
    def __str__(self):
        return "LIST:"+str(self.el)
    
class PrintNode(ExecNode,PrintingNode):
    def __init__(self,el):
        self.el=el
        
    def execute(self):
        return str(execute(self.el))
    
    def __str__(self):
        return "PRINT:"+str(self.el)
    
 
class ForNode(ExecNode,PrintingNode):
    def __init__(self,i,listelem,expressionlist):
        self.i=i
        self.listelem=listelem
        self.expressionlist=expressionlist
    
    def execute(self):
        toPrint=""
        beforeFor=None
        if(self.i in usednames): #Si jamais la variable d'itération existe en dehors du for
            beforeFor=usednames[self.i] 
        for elem in execute(self.listelem):        #Pour chaque element de l'iterateur
            usednames[self.i] = execute(elem)
            for expression in self.expressionlist: #Pour chaque truc à faire dans le for
                if(isinstance(expression,PrintingNode)):
                    toPrint=toPrint+execute(expression)
                else:
                    execute(expression)
        usednames[self.i]=beforeFor
        return toPrint
    
    def __str__(self):
        return "FOR["+str(self.i)+"]in["+str(self.listelem)+"]do["+str(self.expressionlist)+"]"
            


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
       # print("Objet:",elem," de type: ",type(elem))
       #print("       -> ",elem)
       result=result+execute(elem)
       # print("ok \n")
    p[0]=result

def p_expression_list_exprl(p):
    '''expression_list : expression SEMICOLON expression_list'''
    #p[0]=[p[1],p[3]]
    p[0]=[p[1]]
    p[0].extend(p[3])
    
def p_expression_list(p):
    '''expression_list : expression SEMICOLON'''
    p[0]=[p[1]]
    
def p_expression_print(p):
    '''expression : PRINT string_expression'''
    p[0]=PrintNode(p[2])
    #print(p[2])
    #p[0]=p[2]
    
"""    
def p_expression_forstr(p):
    '''expression : FOR VARIABLE IN string_list DO expression_list ENDFOR'''
    #p[0] = ForNode(p[2], Variable(p[4]), p[6]) 
"""
    
def p_expression_for(p):   #Noter 'VARIABLE' et 'variable'
    '''expression : FOR VARIABLE IN variable DO expression_list ENDFOR 
    expression : FOR VARIABLE IN string_list DO expression_list ENDFOR'''   
    p[0]=ForNode(p[2],p[4],p[6])
    
def p_expression_varstring(p):
    '''expression : VARIABLE AFFECT string_expression
    expression : VARIABLE AFFECT string_list'''
    print("WELL")
    p[0]=AffectationNode(p[1],p[3])  #Assignement p[0]=("p[1]=p[3]")

"""    
def p_expression_varlist(p):
    '''expression : VARIABLE AFFECT string_list'''
    p[0]=AffectationNode(p[1],p[3])
"""   
    
def p_string_expression_string(p):
    '''string_expression : string
    string_expression : integer
    string_expression : boolean'''
    p[0]=p[1]    
    
def p_string_expression_var(p):
    '''string_expression : variable'''
    p[0]=p[1] #VARIABLE
    
def p_string_expression_strstr(p):
    '''string_expression : string_expression POINT string_expression''' 
    p[0]=ConcatNode(p[1],p[3])

def p_boolean_andorresult(p):
    '''boolean : string_expression ANDOR string_expression'''
    print("YOYOYOYOY")
    print(p[1],p[2],p[3])
    p[0]=OperationNode(p[1],p[2],p[3])   
    
    
def p_string_list(p):
    '''string_list : LPAREN string_list_interior RPAREN'''
    p[0]=ListNode(p[2])
    
def p_string_list_interior(p):
    '''string_list_interior : string COMA string_list_interior'''
    if(isinstance(p[3],list)):
        p[0]=[p[1]]
        p[0].extend(p[3])
    else:
        p[0]=[p[1],p[3]]
    
def p_string_list_interior_end(p):
    '''string_list_interior : string'''
    p[0]=p[1]

def p_variable(p):
    '''variable : VARIABLE'''
    p[0]=VariableNode(p[1])
    
def p_string(p):
    '''string : STR'''
    p[0]=str(p[1])

def p_int_operation(p): #RENAME
    '''integer : string_expression INT_OP string_expression'''
    p[0]=OperationNode(p[1],p[2],p[3])      

def p_int(p):
    '''integer : INT'''
    p[0]=int(p[1])
    
def p_bool(p):
    '''boolean : BOOL'''
    p[0]=bool(p[1])
    


def p_error(p):
    print("Syntax error: "+str(p.value)+"  line: "+str(p.lineno))
    #print("Syntax error line",p.value)


currentFile=""

def doTheJob(data,template,output):
    print("yo")
"""
    global currentFile
    currentFile="Data"
    parser.parse(data.read(), debug=False)
 
    currentFile="Template"
    result=parser.parse(template.read(), debug=False)
    outputfile=output
    outputfile.write(str(result))
    outputfile.close()
"""

parser=yacc.yacc()

if __name__ == "__main__":
    print("\n")
    datass=open(sys.argv[1], 'r')
    datass=datass.read()
    result = yacc.parse(datass)
    print(usednames)
    print("\n \n        <><><> Parsing <><><> ")
    template=open(sys.argv[2], 'r')
    template=template.read()
    result = yacc.parse(template)
    print("result: \n \n",result)
    print(usednames)

    #if len(sys.argv)==4:
        #data = open(sys.argv[1], 'r')
        #template = open(sys.argv[2], 'r')
        #output = open(sys.argv[3] ,'w')
        #doTheJob(data,template,output)

"""
if __name__ == "__main__":
    import sys
    lexer = lex.lex()
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
"""
    
    
""" #yacc.yacc(outputdir='generated') 
if __name__ == '__main__':
    import sys
    input = open(sys.stdin.read(),'r')
    result = yacc.parse(input)
    print(result)
"""

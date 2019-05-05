from abc import ABC, abstractmethod
"""
Created on Sun May  5 06:19:03 2019

@author: Alfatta
"""


class X(ABC):
    @abstractmethod
    def execute(self):
        pass

class A(X):
    def __init__(self,data):
        self.data=data
        
    def execute(self):
        print("niBBa")
        return self.data
    
    
def execute(q):
    if(isinstance(q,X)):
        q.execute()
    else:
        print(q)
        
"""
uno="bonjou"
duo=A("yoyo")

execute(uno)
execute(duo)

q1="bonjour"
q2="okay"
tab=[q1]
tab.extend(q2)
print(isinstance(tab,list))
print(isinstance(3,int))
print(isinstance('a',int))
"""

a=4
a+=1
print(a)

b=4
b=+1
print(b)
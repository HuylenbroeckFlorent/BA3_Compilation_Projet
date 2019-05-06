import sys
from syntaxic import doTheJob


if __name__ == "__main__":
    data=open(sys.argv[1],'r')
    template=open(sys.argv[2],'r')
    output=open(sys.argv[3] ,'w')
    doTheJob(data,template,output)
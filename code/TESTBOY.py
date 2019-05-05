import sys
"""
def doTheJob(data,template,output):
    global currentFile
    currentFile="Data"
    parser.parse(data.read(), debug=False)
    currentFile="Template"
    result=parser.parse(template.read(), debug=False)
    outputfile=output
    outputfile.write(str(result))
    outputfile.close()
"""
    
if __name__ == "__main__":
    if len(sys.argv)==4:
        data = open(sys.argv[1], 'r')
        template = open(sys.argv[2], 'r')
        output = open(sys.argv[3] ,'w')
        result=data.read()
        result+=template.read()
        output.write(str(result))

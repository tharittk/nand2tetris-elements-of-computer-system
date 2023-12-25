from JackTokenizer import Tokenizer
from CompilationEngine import CompilationEngine

import sys, os
if __name__ == '__main__':
    pathName =sys.argv[1]

    #folderName = os.path.dirname(inputFile)
    #fileName = os.path.basename(inputFile)



for fileName in os.listdir(pathName):
    if fileName.endswith(".jack"):

        #print(os.path.join(pathName, file))
        #outTokenizedFile = folderName + '/' + fileName[:-5] + 'T' + '.xml'
        #outXMLFile = folderName + '/' + fileName[:-5]  + '.xml'

        outTokenizedFile = pathName + '/' + fileName[:-5] + 'T' + '.xml'
        outXMLFile = pathName + '/' + fileName[:-5]  + '.xml'

        tkn = Tokenizer(pathName + '/' + fileName)
        tkn.run()
        tkn.outputting(outTokenizedFile)

        cpe = CompilationEngine(tkn.result)
        cpe.run()
        cpe.outputting(outXMLFile)



'''
    if inputFile != '.\Square\Square.jack':

        inputFiles = ['./ArrayTest/Main.jack', './ExpressionLessSquare/Main.jack',
                    './ExpressionLessSquare/Square.jack', './ExpressionLessSquare/SquareGame.jack',
                    './Square/Main.jack', './Square/SquareGame.jack', './Square/Square.jack']
    

        for inputFile in inputFiles:
            print('>>>>>>>>>>>>> Compiling: ', inputFile )
            folderName = os.path.dirname(inputFile)
            fileName = os.path.basename(inputFile)

            outTokenizedFile = folderName + '/' + fileName[:-5] + 'T_OUT' + '.xml'
            outXMLFile = folderName + '/' + fileName[:-5] + '_OUT' + '.xml'


            print(outTokenizedFile)
            print(outXMLFile)


            #
            tkn = Tokenizer(inputFile)
            tkn.run()


            # output tokenized File
            tkn.outputting(outTokenizedFile)

            cpe = CompilationEngine(tkn.result)
            cpe.run()
            cpe.outputting(outXMLFile)


        #with open('./compiled.xml', 'w') as f:
        #    for token in cpe.result:
        #        f.write(token + '\n')
'''

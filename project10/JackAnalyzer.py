from JackTokenizer import Tokenizer
from CompilationEngine import CompilationEngine

import sys, os
if __name__ == '__main__':
    inputFile =sys.argv[1]

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

    else:
        tkn = Tokenizer(inputFile)
        tkn.run()

        cpe = CompilationEngine(tkn.result)
        cpe.run()
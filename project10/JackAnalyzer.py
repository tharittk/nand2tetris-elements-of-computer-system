from JackTokenizer import Tokenizer
from CompilationEngine import CompilationEngine

import sys
if __name__ == '__main__':
    inputFile =sys.argv[1]

    if inputFile != '.\Square\Square.jack':

        inputFiles = ['./ArrayTest/Main.jack', './ExpressionLessSquare/Main.jack',
                    './ExpressionLessSquare/Square.jack', './ExpressionLessSquare/SquareGame.jack',
                    './Square/Main.jack', './Square/SquareGame.jack']
    

        for inputFile in inputFiles:
            print('>>>>>>>>>>>>>>> >>>>>>>>>>>>>>>>>>>>>>>>>Input:  ', inputFile )
            tkn = Tokenizer(inputFile)
            tkn.run()

            cpe = CompilationEngine(tkn.result)
            cpe.run()

        #with open('./compiled.xml', 'w') as f:
        #    for token in cpe.result:
        #        f.write(token + '\n')
    else:
        tkn = Tokenizer(inputFile)
        tkn.run()

        cpe = CompilationEngine(tkn.result)
        cpe.run()
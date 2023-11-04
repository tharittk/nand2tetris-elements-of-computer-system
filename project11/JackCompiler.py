from JackTokenizer import Tokenizer
from CompilationEngine import CompilationEngine

import sys, os
if __name__ == '__main__':

    inputName =sys.argv[1]

    #folderName = os.path.dirname(inputFile)
    #fileName = os.path.basename(inputFile)
    
    # single file
    if not os.path.isdir(inputName):

        outTokenizedFile = inputName[:-5] + 'T' + '.xml'
        outVMFile = inputName[:-5]  + '.vm'

        # output xml file - tokenized
        tkn = Tokenizer(inputName)
        tkn.run()
        tkn.outputting(outTokenizedFile)

        # output vm file


    # a folder
    else:

        for fileName in os.listdir(inputName):

            if fileName.endswith(".jack"):

                outTokenizedFile = inputName + '/' + fileName[:-5] + 'T' + '.xml'
                outVMFile = inputName + '/' + fileName[:-5]  + '.vm'

                # output xml file - tokenized
                tkn = Tokenizer(inputName + '/' + fileName)
                tkn.run()
                tkn.outputting(outTokenizedFile)

                # output vm file





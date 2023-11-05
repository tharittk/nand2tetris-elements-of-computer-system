# VMWriter


class VMWriter():

    def __init__(self, outputFileName):
        self.outputName = outputFileName

    def _open_and_write(self, toWrite):
        with open(self.outputName, 'a') as f:
            f.write(toWrite + '\n')      

    # write VM push command
    def writePush(self, segment, idx):
        toWrite = '''push {segment} {idx}'''.format(segment = segment.lower(), idx = idx)

        self._open_and_write(toWrite)

    # write VM pop command
    def writePop(self, segment, idx):
        toWrite = '''pop {segment} {idx}'''.format(segment = segment.lower(), idx = idx)

        self._open_and_write(toWrite)

    # write VM arithmatic command
    def writeArithmatic(self, command):
        
        self._open_and_write(command.lower())

            
    # write VM label command
    def writeLabel(self, labelName):
        toWrite = '''label {labelName}'''.format(labelName = labelName)

        self._open_and_write(toWrite)

    # write VM go-to command
    def writeGoto(self, labelName):

        toWrite = '''goto {labelName}'''.format(labelName = labelName)

        self._open_and_write(toWrite)

    # write VM if-goto command
    def writeIf(self, labelName):

        toWrite = '''if-goto {labelName}'''.format(labelName = labelName)

        self._open_and_write(toWrite)


    # write VM call command
    def writeCall(self, callName, nArgs):
        toWrite = '''call {callName} {nArgs}'''.format(callName = callName, nArgs = str(nArgs))

        self._open_and_write(toWrite)


    # write VM Function command
    def writeFunction(self, funcName, nVars):
        toWrite = '''function {funcName} {nVars}'''.format(funcName = funcName, nVars = str(nVars))
        self._open_and_write(toWrite)

    def writeReturn(self):
        self._open_and_write('return')
     
# Parser subroutine for VMTranslator

class Parser():

    # Open the input file and gets ready to parse it
    def __init__(self, vmFile):
        self.vmFile = vmFile
        self.vmCommands = self._preprocess()
        self.currentCommandIndex = 0
        self.currentCommand = self.vmCommands[0]
        #print(self.vmCommands)

    # Eliminate non-command text
    def _preprocess(self):
        with open(self.vmFile) as f:
            # process text file
            lines = f.readlines()
            commandList = []
            for line in lines:
                line = line.strip()
                # Comment of empty line
                if line[0:2] == "//" or line[0:2] == "\n" or line == '':
                    pass
                else:
                    line = line.strip('\n')
                    line = line.strip('\t')
                    # inline comment
                    line = line.split("//")[0]
                    commandList.append(line)
        return commandList
    
    # Return True if there are more lines in the input, false otherwise
    def hasMoreLines(self):
        totalLines = len(self.vmCommands)

        if self.currentCommandIndex < totalLines:
            return True
        else:
            return False
        
    # Read the next command from the input and makes it current command
    # call only if has moreLines, initially there is no current command
    def advance(self):
        self.currentCommandIndex += 1
        # see if at the last line already
        if self.hasMoreLines():
            self.currentCommand = self.vmCommands[self.currentCommandIndex]
        # prevent out of range accessing
        else:
            pass
    
    # Return 'constant' representating the type of current command
    def commandType(self):
        ops = self.currentCommand.split(" ")[0]
        if ops == "push":
            return "C_PUSH"
        elif ops == "pop":
            return "C_POP"
        elif ops == "label":
            return "C_LABEL"
        elif ops == "goto":
            return "C_GOTO"
        elif ops == "if-goto":
            return "C_IF"
        elif ops == "function":
            return "C_FUNCTION"
        elif ops == "return":
            return "C_RETURN"
        elif ops == "call":
            return "C_CALL"
        else:
            return "C_ARITHMETIC"
        
    
    # Return first argument of the current command, in case of C_ARITHMATIC (add, etc)
    # the command itself is returned, should not be called if the current command is C_RETURN
    def arg1(self):
        cmdType = self.commandType()

        assert cmdType != "C_RETURN"

        if cmdType == "C_ARITHMETIC":
            return self.currentCommand.split(" ")[0]        
        else:
            return self.currentCommand.split(" ")[1]

    # Return second argument of the current command, should be called only if 
    # the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL
    def arg2(self):
        cmdType = self.commandType()

        assert cmdType in ["C_PUSH", "C_POP", "C_FUNCTION","C_CALL"]

        argument2 = self.currentCommand.split(" ")[2]

        return int(argument2)

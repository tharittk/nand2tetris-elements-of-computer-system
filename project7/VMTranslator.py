
# VM Translator

# This object parses each VM commands into its lexical elements
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
        # FOR NOW
        else:
            return "C_ARITHMETIC"
        
        # handle pop 7 ?
    
    # Return first argument of the current command, in case of C_ARITHMATIC (add, etc)
    # the command itself is returned, should not be called if the current command is C_RETURN
    def arg1(self):
        cmdType = self.commandType()

        assert cmdType != "C_RETURN"

        if cmdType == "C_ARITHMETIC":
            return self.currentCommand.split(" ")[0]
        
        if cmdType == "C_PUSH" or cmdType == "C_POP":
            return self.currentCommand.split(" ")[1]
    
    # Return second argument of the current command, should be called only if 
    # the current command is C_PUSH, C_POP, C_FUNCTION, or C_CALL
    def arg2(self):
        argument2 = self.currentCommand.split(" ")[2]
        return int(argument2)

# This objects takes the parsed command and write the assembly code
class CodeWrite():
    # Open the output file and gets ready to write into it
    def __init__(self, vmFile):

        # FIX LATER
        self.outName = vmFile[:-2] + 'asm'


    # Write to the output file the assembly code of the
    # arithmetic-logical command
    def writeArithmetic(self, command):
        toWrite = ''
        # you can tell at the garbarge at | 0  | 1 | > the zero becomes 0+1 while the 1 stays the same with SP points at
        if command == 'add':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M + D\n'
        elif command == 'sub':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M - D\n'
        elif command == 'neg':
            toWrite = '@SP\nA = M - 1\nM = -M\n'

        # Store value issue
        elif command == 'eq':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M - D\nD=M\n@R1\nD;JEQ\n@R0\n'
        elif command == 'gt':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M - D\nD=M\n@R1\nD;JGT\n@R0\n'
        elif command == 'lt':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M - D\nD=M\n@R1\nD;JLT\n@R0\n'
        # jump to R0 or R1 if A-D JEQ, JLT, JGT

        elif command == 'and':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M & D\n'
        elif command == 'or':
            toWrite = '@SP\nA = M - 1\nD = M\n@SP\nM = M -1\n@SP\nA = M -1\nM = M | D\n'
        elif command == 'not':
            toWrite = '@SP\nA = M - 1\nM = !M\n'
        

        with open(self.outName, 'a') as f:
            f.write(toWrite)
    
    # Write to the output filethe assembly code of the
    # push or pop command
    def writePushPop(self):
        return 0
    
        '@SP'
        '@LCL'
        '@ARG'
        '@THIS'
        '@THAT'
        'constant directly to stack'
        'static starts 16 to 255'
        'temp addr = 5 to 12'
        'pointer' 'push pop pointer 0 == push pop THIS' ', push pop pointer 1 === push pop THAT'
    
    # Close the output file
    def close(self):
        return 0


# Drive the process
class Main():
    def __init__(self):
        
        # File read
        print("Start a VM Translator...")
        fname = "./SimpleAdd.vm"
        #fname = "./BasicTest.vm"
        #fname = "./PointerTest.vm"
        #fname = "./StackTest.vm"
        #fname = "./StaticTest.vm"
        
        commands = Parser(fname)
        writer = CodeWrite(fname)

        while commands.hasMoreLines():
            # do sth
            print("Full Command: ", commands.currentCommand)
            print(commands.commandType())
            print(commands.arg1())
            if commands.commandType() in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
                print(commands.arg2())
            elif commands.commandType() == "C_ARITHMETIC":
                writer.writeArithmetic(commands.arg1())
            
            



            # finish the command    
            commands.advance()

        # Construct the parser

        # iteratite through the input file

            # pass each line to parser

            # generate assembly code

if __name__ == "__main__":
    Main()

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
        self.fileName = vmFile
        self.outName = vmFile[:-2] + 'asm'
        self.staticBaseAddr = 16
        self.tempBaseAddr = 5


    # Write to the output file the assembly code of the
    # arithmetic-logical command
    def writeArithmetic(self, command, line_num):
        toWrite = ''
        # you can tell at the garbarge at | 0  | 1 | > the zero becomes 0+1 while the 1 stays the same with SP points at
        if command == 'add':
            toWrite = """
            // add
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M + D
            """
        elif command == 'sub':
            toWrite = """
            // sub
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M - D
            """
        elif command == 'neg':
            toWrite = """
            // neg
            @SP
            A = M - 1
            M = -M
            """

        # Store value issue
        elif command == 'eq':
            toWrite = """
            // eq
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @EQ_{line_num}
            D;JEQ
            @SP
            A = M - 1
            M = 0
            @END_{line_num}
            0;JMP
            (EQ_{line_num})
            @SP
            A = M - 1
            M = -1
            (END_{line_num})
            """.format(line_num = line_num)
        elif command == 'gt':
            toWrite = """
            // gt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @GT_{line_num}
            D;JGT
            @SP
            A = M - 1
            M = 0
            @END_{line_num}
            0;JMP
            (GT_{line_num})
            @SP
            A = M - 1
            M = -1
            (END_{line_num})
            """.format(line_num = line_num)
        elif command == 'lt':
            toWrite = """
            // lt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @LT_{line_num}
            D;JLT
            @SP
            A = M - 1
            M = 0
            @SP
            @END_{line_num}
            0;JMP
            (LT_{line_num})
            @SP
            A = M - 1
            M = -1
            (END_{line_num})
            """.format(line_num = line_num)        # jump to R0 or R1 if A-D JEQ, JLT, JGT

        elif command == 'and':
            toWrite = """
            // and
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M & D
            """
        elif command == 'or':
            toWrite = """
            // or
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M | D
            """        
        elif command == 'not':
            toWrite = """
            @SP
            A = M - 1
            M = !M
            """
        
        with open(self.outName, 'a') as f:
            f.write(toWrite)
    
    # Write to the output filethe assembly code of the
    # push or pop command
    def writePushPop(self, command, segment, i, line_num):

        if segment == 'local':
            baseAddr = 'LCL'
        elif segment == 'argument':
            baseAddr = 'ARG'
        elif segment == 'this':
            baseAddr = 'THIS'
        elif segment == 'that':
            baseAddr = 'THAT'    

        if command == "C_PUSH":
            if segment == 'constant':
                toWrite = """
                // push {segment} {i}
                @{i}
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i = i)

            elif segment in ['local', 'argument', 'this', 'that']:

                toWrite = """
                // push {segment} {i}
                @{i}
                D = A
                @{baseAddr}
                A = M + D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i= i, baseAddr = baseAddr)

            elif segment == 'static':
                toWrite = """
                // push {segment}} {i}
                @{filename}.{i}
                A = M 
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i= i, filenme = self.fileName)
            elif segment == 'temp':
                toWrite = """
                // push {segment} {i}
                @5
                D = A 
                @{i}
                D = D + A
                A = D
                D = M
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i= i)
            elif segment == "pointer":
                toWrite = """
                // push pointer {i}
                @{i}
                D = A
                @3
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                """.format(i= i)

        elif command == "C_POP":


            if segment in ['local', 'argument', 'this', 'that']:

                toWrite = """
                // pop {segment} {i}
                @{i}
                D = A
                @{baseAddr}
                D = D + A
                @addrTemp_{line_num}
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_{line_num}
                A = M
                M = D            
                """.format(segment = segment, i= i, line_num = line_num,  baseAddr=baseAddr)

            elif segment == 'static':
                toWrite = """
                // pop {segment}} {i}
                @SP
                M = M - 1
                A = M
                D = M
                @{filename}.{i}
                M = D
      
                """.format(segment = segment, i= i, filenme = self.fileName)

            elif segment == 'temp':
                toWrite = """
                // pop {segment} {i}
                @{i}
                D = A
                @5
                D = D + A
                @addrTemp_{line_num}
                M = D
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_{line_num}
                A = M
                M = D          
                """.format(segment = segment, i= i, line_num = line_num)

            elif segment == "pointer":
                toWrite = """
                // pop pointer {i}
                @{i}
                D = A
                @3
                D = D + A
                @addrTemp_{line_num}
                M = D
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_{line_num}
                A = M
                M = D          
                """.format(i= i, line_num = line_num)

        else:
            raise ValueError 
        with open(self.outName, 'a') as f:
            f.write(toWrite)
    
    # Close the output file
    def close(self):
        return 0


# Drive the process
class Main():
    def __init__(self):
        
        # File read
        print("Start a VM Translator...")
        #fname = "./SimpleAdd.vm"
        #fname = "./BasicTest.vm" # fail
        #fname = "./PointerTest.vm"
        fname = "./StackTest.vm"
        #fname = "./StaticTest.vm"
        
        commands = Parser(fname)
        writer = CodeWrite(fname)

        while commands.hasMoreLines():
            # Write
            if commands.commandType() in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
                writer.writePushPop(commands.commandType(), commands.arg1(), commands.arg2(), commands.currentCommandIndex)
            elif commands.commandType() == "C_ARITHMETIC":
                writer.writeArithmetic(commands.arg1(),commands.currentCommandIndex)
            
            # finish the command    
            commands.advance()

if __name__ == "__main__":
    Main()
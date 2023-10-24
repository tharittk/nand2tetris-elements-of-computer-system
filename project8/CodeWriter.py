
# Code writer subroutine for VM translator



# This objects takes the parsed command and write the assembly code
class CodeWrite():
    # Open the output file and gets ready to write into it
    def __init__(self, vmFile):

        # FIX LATER
        #self.fileName = vmFile[2:-3]
        self.fileName = vmFile.split('/')[-1][:-3]
        self.outName = vmFile[:-2] + 'asm'
        self.staticBaseAddr = 16
        self.tempBaseAddr = 5
        # bootstrap here
        self._bootstrap()
    
    def _bootstrap(self):
        with open(self.outName, 'a') as f:
            f.write("//bootstrap here")
    
    def setFileName(self, newVmFile):
        self.fileName = newVmFile.split('/')[-1][:-3]
        self.outName = newVmFile[:-2] + 'asm'
        
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
                @{baseAddr}
                D = M
                @{i}
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i= i, baseAddr = baseAddr)

            elif segment == 'static':
                toWrite = """
                // push {segment} {i}
                @{filename}.{i} 
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                """.format(segment = segment, i= i, filename = self.fileName)
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
                @{baseAddr}
                D = M
                @{i}
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
                // pop {segment} {i}
                @SP
                M = M - 1
                A = M
                D = M
                @{filename}.{i}
                M = D
                """.format(segment = segment, i= i, filename = self.fileName)

            elif segment == 'temp':
                toWrite = """
                // pop {segment} {i}
                @5
                D = A 
                @{i}
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
    

    # write label
    def writeLabel(self, label):
        toWrite = '''
            // label
            ({label})
        '''.format(label=label)
        with open(self.outName, 'a') as f:
            f.write(toWrite)

    # write Goto
    def writeGoto(self, label):
        toWrite = '''
            // go to label
            @{label}
            0; JMP
        '''.format(label=label)
        with open(self.outName, 'a') as f:
            f.write(toWrite)
    # write if
    def writeIf(self, label):
        toWrite = '''
            // if-goto label
            @SP
            A = M -1
            D = M
            @SP
            M = M - 1
            @{label}
            D; JNE
        '''.format(label=label)
        with open(self.outName, 'a') as f:
            f.write(toWrite)
    

    # write Function
    def writeFunction(self, functionName, nVars):
        tmp1 ='''
        // function
        ({functionName}) 
        '''.format(functionName = functionName)
        
        tmp2 = ''
        # push local 0 nVars times
        for i in range(nVars):
            tmp2 += '''
                // push local 0 nVars times {i} of {nVars}
                @0
                D = A
                @SP
                A = M 
                M = D
                @SP
                M = M + 1 \n
            '''.format(i = i+1, nVars = nVars)
        
        toWrite = tmp1 + tmp2
        with open(self.outName, 'a') as f:
            f.write(toWrite)

    def writeCall(self, functionName, nArgs, i):
        toWrite = '''
        // Call function
        // save frame of the caller
        // push retAddrLabel
        @{functionName}$ret.{i}
        D = A
        @SP
        A = M
        M = D
        @SP
        M = M + 1
        // push LCL
        @LCL
        D = A
        @SP
        A = M
        M = D
        @SP
        M = M + 1
        // push ARG
        @ARG
        D = A
        @SP
        A = M
        M = D
        @SP
        M = M + 1
        // push THIS
        @THIS
        D = A
        @SP
        A = M
        M = D
        @SP
        M = M + 1
        // push THAT
        @THAT
        D = A
        @SP
        A = M
        M = D
        @SP
        M = M + 1
        // reposition ARG = SP -5 - nArgs
        @SP
        D = M
        D = D - 1
        D = D - 1
        D = D - 1
        D = D - 1
        D = D - 1
        @{nArgs}
        D = D - A
        @ARG
        M = D
        // reposition LCL = SP
        @SP
        D = M
        @LCL
        M = D
        // goto functionName
        @{functionName}
        0;JMP
        // inject return address 
        ({functionName}$ret.{i})
        '''.format(functionName = functionName, i = i, nArgs = nArgs)
        
        with open(self.outName, 'a') as f:
            f.write(toWrite)

    def writeReturn(self):

        toWrite ='''
        // Return

        // Replace first Arg with latested pushed value
        @SP
        A = M - 1
        D = M
        @ARG
        A = M
        M = D
        // Recycle memomey (move SP)
        @ARG
        D = M
        @SP
        M = D + 1
        // Reinstate the frame
        @9988
        @D
        // THAT = endframe -1
        @LCL
        D = M
        D = D -1
        A = D
        D = M
        @THAT
        M = D
        
        // THIS = endframe - 2
        @LCL
        D = M
        D = D - 1
        D = D - 1
        A = D
        D = M
        @THIS
        M = D

        // ARG = endframe - 3
        @LCL
        D = M
        D = D - 1
        D = D - 1
        D = D - 1
        A = D
        D = M
        @ARG
        M = D
        
        // save at SP for retAddr use
        @LCL
        D = M
        @SP
        A = M
        M = D

        // LCL = endframe - 4
        @LCL
        D = M
        D = D - 1
        D = D - 1
        D = D - 1
        D = D - 1
        A = D
        D = M
        @LCL
        M = D


        // retAddr = endframe - 5
        @SP
        A = M
        D = M
        D = D - 1
        D = D - 1
        D = D - 1
        D = D - 1
        D = D - 1
        A = D
        D = M
        
        //@retAddr
        //M = D
        //@retAddr
        //A = M 
        //0;JMP

        //@D won't work
        A = D
        0;JMP


        '''
        with open(self.outName, 'a') as f:
            f.write(toWrite)
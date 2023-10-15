



JUMP_CODES = {'NULL': '000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

DEST_CODES = {'NULL':'000', 'M':'001', 'D':'010', 'DM':'011', 'A':'100', 'AM':'101', 'AD':'110', 
              'ADM':'111', 'MD':'011','MA':'101','DA':'110', 'AMD':'111','DAM':'111','DMA':'111'}


COMP_CODES = {'0': '0101010', '1': '0111111', '-1':'0111010', 'D':'0001100', 'A': '0110000', '!D': '0001101',
                   '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
                   'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D':'0000111',
                   'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011',
                   'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
                   'D&M': '1000000', 'D|M': '1010101'}



class Instruction():
    def __init__(self, text):
        self.text = text
        self.type = 'NULL'
        self.symbol = 'NULL'
        self.dest = 'NULL'
        self.comp = 'NULL'
        self.jump = 'NULL'

class SymbolTable():
    def __init__(self):
        self.table = {}
    def addEntry(self, symbol, address = 0):
        self.table[symbol] = address
    def contains(self, symbol):
        if symbol in self.table.keys():
            return True
        else:
            return False
    def getAddress(self, symbol):
        if self.contains(symbol):
            return self.table[symbol]
        else:
            raise ValueError


def ReadAsm(asmFile):
    with open(asmFile) as f:
        # process text file
        lines = f.readlines()
        cleaned_asm = []
        for line in lines:
            
            line = line.strip()
            # comment
            if line[0:2] == "//" or line[0:2] == "\n" or line == '':
                pass
            else:
                line = line.strip('\n')
                line = line.strip('\t')
                line = line.replace(' ','')
                # eliminate inline comment
                line = line.split("//")[0]

                cleaned_asm.append(line)

        return cleaned_asm

def Parser(instruction_text):

    instruction = Instruction(instruction_text)
    # instruction type handling
    if instruction.text[0] == "@":
        instruction.type = 'A_INSTRUCTION'
    elif instruction.text[0] == '(':
        instruction.type = 'L_INSTRUCTION'
    else:
        instruction.type = 'C_INSTRUCTION'

    # symbol handling
    if instruction.type == 'L_INSTRUCTION':
        instruction.symbol = instruction.text[1:-1]

        return instruction
    elif instruction.type == 'A_INSTRUCTION':
        instruction.symbol = instruction.text[1:] # works both symbol and integer -- decide later in code part (if 'symbol' starts with number of not)
        
        return instruction
    # C-instruction handling
    else:
        assert instruction.type == 'C_INSTRUCTION'
        if ';' in instruction.text:        
            ops, instruction.jump = instruction.text.split(';')
        else: # no jump clause
            ops = instruction.text[:]
            instruction.jump = 'NULL'
        if '=' in ops:
            instruction.dest, instruction.comp = ops.split("=")
        else:
            instruction.comp = ops
            instruction.dest = 'NULL'

        return instruction
    # End at slide 52 (API)


def InitializeSymboleTable():
    st = SymbolTable()
    # R0 to R15
    for i in range(0, 16):
        st.addEntry('R'+str(i), i)
    st.addEntry('SCREEN', 16384)
    st.addEntry('KBD', 24576)
    st.addEntry('SP', 0)
    st.addEntry('LCL', 1)
    st.addEntry('ARG', 2)
    st.addEntry('THIS',3)
    st.addEntry('THAT',4)

    return st

def AddLabelToSymbolTable(asmLines, symbolTable):
    # first pass: count lines and adds label symbol
    count = 0
    for line in asmLines:
        instruction = Parser(line)
        if instruction.type == 'L_INSTRUCTION':
            symbolTable.addEntry(instruction.symbol, count)
        else:
            count += 1
    # second pass
    addr = 16
    for line in asmLines:
        instruction = Parser(line)
        if instruction.type == 'A_INSTRUCTION' and not symbolTable.contains(instruction.symbol) and instruction.symbol[0].isalpha():
            symbolTable.addEntry(instruction.symbol, addr)
            addr += 1
    return symbolTable

# trascribe each line to binary
def Code(instruction ,st, dest_table, comp_table, jump_table):
    
    instruction = Parser(line)

    # A-instruction
    if instruction.type == 'A_INSTRUCTION':
        if instruction.symbol[0].isalpha(): # look up table:
            assert st.contains(instruction.symbol)
            integerValue = st.getAddress(instruction.symbol)
        else:
            integerValue = int(instruction.symbol)
        # convert to binary
        binNoleading = bin(integerValue)[2:]
        n_pad = 16 - len(binNoleading)
        binCode = '0'* n_pad
        binCode += binNoleading
        return binCode
        

    # C-instruction
    
    elif instruction.type == 'C_INSTRUCTION':

        binCode = '111'
        dest = dest_table[instruction.dest]
        comp = comp_table[instruction.comp]
        jump = jump_table[instruction.jump]

        binCode += comp
        binCode += dest
        binCode += jump

        return binCode


if __name__ == "__main__":
    

    testFiles = ["./Add.asm", "./Max.asm", "./MaxL.asm", "./Pong.asm", "./PongL.asm", "./Rect.asm", "./RectL.asm"]

    #testFiles = ["./MaxL.asm"]
    
    #testFiles = [ "./Pong.asm", "./Rect.asm"]

    #testFiles = ["./Rect.asm"]


    for file in testFiles:
        cleaned_asm = ReadAsm(file)
        hackOutName = file[2:].replace('.asm', '.hack')

        hack_file = open(hackOutName, 'w')

    
        symbolTable = InitializeSymboleTable()
        symbolTable = AddLabelToSymbolTable(cleaned_asm, symbolTable)

        for line in cleaned_asm:
            instruction = Parser(line)
            
            # L-instruction = skip no binary execution there

            if instruction.type != 'L_INSTRUCTION':

                binCode = Code(instruction, symbolTable, DEST_CODES, COMP_CODES, JUMP_CODES)
                
                '''
                print("full text:", instruction.text)
                print("type: ",instruction.type)
                print("symbol: ",instruction.symbol)
                print("dest: ", instruction.dest)
                print("comp: ", instruction.comp)
                print("jump: ", instruction.jump)
                '''

                hack_file.write(binCode + '\n')

        hack_file.close()

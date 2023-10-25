from Parser import Parser
from CodeWriter import CodeWrite


# Drive the process
class Main():
    def __init__(self):
        
        # File read
        #fname = './ProgramFlow/BasicLoop/BasicLoop.vm'
        #fname = './ProgramFlow/FibonacciSeries/FibonacciSeries.vm'
        
        #fname = './FunctionCalls/SimpleFunction/SimpleFunction.vm'
        #fname = './FunctionCalls/NestedCall/'
        #fname = './FunctionCalls/FibonacciElement/'
        #fname = './FunctionCalls/StaticsTest/'

        fname = sys.argv[1]

        # Handle single file
        if not os.path.isdir(fname):
            vmFile = fname

            commands = Parser(vmFile)
            writer = CodeWrite(vmFile)

            while commands.hasMoreLines():
                # Write
                cmdType = commands.commandType()

                if cmdType in ['C_PUSH', 'C_POP']:
                    writer.writePushPop(cmdType, commands.arg1(), commands.arg2(), commands.currentCommandIndex)
                elif cmdType == "C_ARITHMETIC":
                    writer.writeArithmetic(commands.arg1(),commands.currentCommandIndex)
                elif cmdType == 'C_LABEL':
                    writer.writeLabel(commands.arg1())
                elif cmdType == 'C_GOTO':
                    writer.writeGoto(commands.arg1())
                elif cmdType == 'C_IF':
                    writer.writeIf(commands.arg1())
                elif cmdType == 'C_FUNCTION':
                    writer.writeFunction(commands.arg1(), commands.arg2())
                elif cmdType == 'C_CALL':
                    writer.writeCall(commands.arg1(), commands.arg2(),commands.currentCommandIndex)
                elif cmdType == 'C_RETURN':
                    writer.writeReturn()
                # finish the command    
                commands.advance()

        else:
            files = os.listdir(fname)
            vmFiles = []
            for file in files:
                if file[-3:] == '.vm':
                    vmFiles.append(fname + file)
        
            bootStrap = True
            for vmFile in vmFiles:
                
                commands = Parser(vmFile)
                writer = CodeWrite(vmFile, bootStrap)

                while commands.hasMoreLines():
                    # Write
                    cmdType = commands.commandType()

                    if cmdType in ['C_PUSH', 'C_POP']:
                        writer.writePushPop(cmdType, commands.arg1(), commands.arg2(), commands.currentCommandIndex)
                    elif cmdType == "C_ARITHMETIC":
                        writer.writeArithmetic(commands.arg1(),commands.currentCommandIndex)
                    elif cmdType == 'C_LABEL':
                        writer.writeLabel(commands.arg1())
                    elif cmdType == 'C_GOTO':
                        writer.writeGoto(commands.arg1())
                    elif cmdType == 'C_IF':
                        writer.writeIf(commands.arg1())
                    elif cmdType == 'C_FUNCTION':
                        writer.writeFunction(commands.arg1(), commands.arg2())
                    elif cmdType == 'C_CALL':
                        writer.writeCall(commands.arg1(), commands.arg2(),commands.currentCommandIndex)
                    elif cmdType == 'C_RETURN':
                        writer.writeReturn()
                    # finish the command    
                    commands.advance()
                
                bootStrap = False

if __name__ == "__main__":
    import os
    Main()
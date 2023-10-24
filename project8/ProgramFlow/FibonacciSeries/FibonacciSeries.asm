
                // push argument 1
                @ARG
                D = M
                @1
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
                // pop pointer 1
                @1
                D = A
                @3
                D = D + A
                @addrTemp_1
                M = D
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_1
                A = M
                M = D          
                
                // push constant 0
                @0
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // pop that 0
                @THAT
                D = M
                @0
                D = D + A
                @addrTemp_3
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_3
                A = M
                M = D            
                
                // push constant 1
                @1
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // pop that 1
                @THAT
                D = M
                @1
                D = D + A
                @addrTemp_5
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_5
                A = M
                M = D            
                
                // push argument 0
                @ARG
                D = M
                @0
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
                // push constant 2
                @2
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // sub
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M - D
            
                // pop argument 0
                @ARG
                D = M
                @0
                D = D + A
                @addrTemp_9
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_9
                A = M
                M = D            
                
            // label
            (MAIN_LOOP_START)
        
                // push argument 0
                @ARG
                D = M
                @0
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
            // if-goto label
            @SP
            A = M -1
            D = M
            @SP
            M = M - 1
            @COMPUTE_ELEMENT
            D; JNE
        
            // go to label
            @END_PROGRAM
            0; JMP
        
            // label
            (COMPUTE_ELEMENT)
        
                // push that 0
                @THAT
                D = M
                @0
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
                // push that 1
                @THAT
                D = M
                @1
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
            // add
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M + D
            
                // pop that 2
                @THAT
                D = M
                @2
                D = D + A
                @addrTemp_18
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_18
                A = M
                M = D            
                
                // push pointer 1
                @1
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
                
                // push constant 1
                @1
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // add
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M + D
            
                // pop pointer 1
                @1
                D = A
                @3
                D = D + A
                @addrTemp_22
                M = D
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_22
                A = M
                M = D          
                
                // push argument 0
                @ARG
                D = M
                @0
                D = D + A
                A = D
                D = M
                @SP
                A = M 
                M = D
                @SP
                M = M + 1
                
                // push constant 1
                @1
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // sub
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M - D
            
                // pop argument 0
                @ARG
                D = M
                @0
                D = D + A
                @addrTemp_26
                M = D 
                @SP
                M = M - 1
                A = M
                D = M
                @addrTemp_26
                A = M
                M = D            
                
            // go to label
            @MAIN_LOOP_START
            0; JMP
        
            // label
            (END_PROGRAM)
        
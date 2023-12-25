
                // push constant 17
                @17
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 17
                @17
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // eq
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @EQ_2
            D;JEQ
            @SP
            A = M - 1
            M = 0
            @END_2
            0;JMP
            (EQ_2)
            @SP
            A = M - 1
            M = -1
            (END_2)
            
                // push constant 17
                @17
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 16
                @16
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // eq
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @EQ_5
            D;JEQ
            @SP
            A = M - 1
            M = 0
            @END_5
            0;JMP
            (EQ_5)
            @SP
            A = M - 1
            M = -1
            (END_5)
            
                // push constant 16
                @16
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 17
                @17
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // eq
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @EQ_8
            D;JEQ
            @SP
            A = M - 1
            M = 0
            @END_8
            0;JMP
            (EQ_8)
            @SP
            A = M - 1
            M = -1
            (END_8)
            
                // push constant 892
                @892
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 891
                @891
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // lt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @LT_11
            D;JLT
            @SP
            A = M - 1
            M = 0
            @SP
            @END_11
            0;JMP
            (LT_11)
            @SP
            A = M - 1
            M = -1
            (END_11)
            
                // push constant 891
                @891
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 892
                @892
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // lt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @LT_14
            D;JLT
            @SP
            A = M - 1
            M = 0
            @SP
            @END_14
            0;JMP
            (LT_14)
            @SP
            A = M - 1
            M = -1
            (END_14)
            
                // push constant 891
                @891
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 891
                @891
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // lt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @LT_17
            D;JLT
            @SP
            A = M - 1
            M = 0
            @SP
            @END_17
            0;JMP
            (LT_17)
            @SP
            A = M - 1
            M = -1
            (END_17)
            
                // push constant 32767
                @32767
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 32766
                @32766
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // gt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @GT_20
            D;JGT
            @SP
            A = M - 1
            M = 0
            @END_20
            0;JMP
            (GT_20)
            @SP
            A = M - 1
            M = -1
            (END_20)
            
                // push constant 32766
                @32766
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 32767
                @32767
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // gt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @GT_23
            D;JGT
            @SP
            A = M - 1
            M = 0
            @END_23
            0;JMP
            (GT_23)
            @SP
            A = M - 1
            M = -1
            (END_23)
            
                // push constant 32766
                @32766
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 32766
                @32766
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // gt
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            D = M - D
            @GT_26
            D;JGT
            @SP
            A = M - 1
            M = 0
            @END_26
            0;JMP
            (GT_26)
            @SP
            A = M - 1
            M = -1
            (END_26)
            
                // push constant 57
                @57
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 31
                @31
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
                // push constant 53
                @53
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
            
                // push constant 112
                @112
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
            
            // neg
            @SP
            A = M - 1
            M = -M
            
            // and
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M & D
            
                // push constant 82
                @82
                D = A
                @SP
                A = M
                M = D
                @SP
                M = M + 1
                
            // or
            @SP
            M = M -1
            @SP
            A = M 
            D = M
            @SP
            A = M - 1
            M = M | D
            
            @SP
            A = M - 1
            M = !M
            
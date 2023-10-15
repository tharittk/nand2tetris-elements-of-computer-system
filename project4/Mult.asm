// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

    // if R0 = 0 or R1 = 0, set R2 = 0
    
        @R0
        D = M
        @RETURN_ZERO
        D; JEQ

        @R1
        D = M
        @RETURN_ZERO
        D; JEQ

        // Typical multiplication
        
        @i
        M = 1
        // set R2 = R0
        @R0
        D = M
        @R2
        M = D 

    (LOOP) 
    // check if i == R1 already
        @i
        D = M
        @R1
        D = D - M // R1 - i
        @END
        //if done, end program
        D; JEQ 
        // else
        @R0
        D = M
        @R2
        M = M + D
        @i
        M = M +1

        @LOOP
        0;JMP

    (RETURN_ZERO)
        @R2
        M = D
        @END
        0;JMP

    (END)
        @END
        0;JMP
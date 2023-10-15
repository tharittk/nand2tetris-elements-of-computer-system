// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @SCREEN //fetch screen basea address value to A
    D = A
    @screen_addr
    M = D
    @255
    D = A
    @nrow
    M = D
    @32
    D = A
    @ncol
    M = D

    (PROBE)
        @irow
        M = 0
        @icol
        M = 0 
        @SCREEN
        D = A
        @screen_addr
        M = D

        @KBD
        D = M
        @FILL_ENTIRE_ROW_WHITE
        D;JEQ
        
        @FILL_ENTIRE_ROW_BLACK
        0;JMP
    
    (FILL_NEXT_ROW_WHITE)
        @irow
        D = M
        @nrow
        D = D - M
        // if done, go probe
        @PROBE
        D; JEQ

        //else continue filling
        @irow
        M = M + 1
        @icol //reset i col
        M = 0

        //shift screen_addr by ncol
        @ncol
        D = M
        @screen_addr
        M = M + D

        @FILL_ENTIRE_ROW_WHITE
        0; JMP

    (FILL_NEXT_ROW_BLACK)
        @irow
        D = M
        @nrow
        D = D - M
        // if done, go probe
        @PROBE
        D; JEQ
        //else continue filling
        @irow
        M = M + 1
        @icol //reset i col
        M = 0

        //shift screen_addr by ncol
        @ncol
        D = M
        @screen_addr
        M = M + D

        @FILL_ENTIRE_ROW_BLACK
        0; JMP

    (FILL_ENTIRE_ROW_BLACK)
        @icol
        D = M
        @ncol
        D = D - M
        @FILL_NEXT_ROW_BLACK
        D;JEQ

        @icol
        D = M
        @screen_addr
        A = M + D //make RAM[screen_adr + icol] becomes active
        M = -1
        @icol
        M = M + 1
        @FILL_ENTIRE_ROW_BLACK
        0;JMP
    (FILL_ENTIRE_ROW_WHITE)
        @icol
        D = M
        @ncol
        D = D - M
        @FILL_NEXT_ROW_WHITE
        D;JEQ

        @icol
        D = M
        @screen_addr
        A = M + D
        M = 0
        @icol
        M = M + 1
        @FILL_ENTIRE_ROW_WHITE
        0;JMP


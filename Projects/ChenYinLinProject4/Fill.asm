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

// Collaboration: Eddie Liu (Ming-Chieh)

// Initialize variables
	@SCREEN
	D=A
	@next
	M=D

// Infinite loop
(INF)
	// check the keyboard input
	@KBD
	D=M
	@WHITE
	D;JEQ

	// If input, screen to black, 
	@next
	A=M
	M=-1

	// If next - KBD >= 0, STOP 
	@next
	D=M
	@KBD
	D=D-A
	@INF
	D;JEQ
	
	//otherwise, next = next + 1
	@next
	M=M+1
	@INF
	0;JMP


	// If not, previous one to white, next = next - 1
(WHITE)
	// If input, screen to WHITE, 
	@next
	A=M
	M=0

	// If next - SCREEN <= 0, STOP 
	@next
	D=M
	@SCREEN
	D=D-A
	@INF
	D;JEQ
	
	//otherwise, next = next - 1
	@next
	M=M-1
	@INF
	0;JMP


	 



  
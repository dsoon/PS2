DECLARE TTT_Length : INTEGER
TTT_Length <- 9

DECLARE TTT : ARRAY [1 : TTT_Length] OF CHAR
DECLARE Choice : INTEGER
DECLARE Count : INTEGER
DECLARE Player1 : BOOLEAN
DECLARE Finished : BOOLEAN

// Procedure TO set-up the game
 PROCEDURE Setup

	FOR i <- 1 TO TTT_Length
		TTT[i] <- '_'
	NEXT i

	Finished <- FALSE
	Player1 <- TRUE
	Count <- 0

	// Print out instructions
	OUTPUT "TIC-TAC-TOE"
	OUTPUT "==========="
	OUTPUT "This is a 2 player game. Each player takes a turn TO pick"
	OUTPUT "a location on a 3 x 3 board. The first player, Player1 is" 
	OUTPUT "assigned a 'X', and player 2 a 'O'."
	OUTPUT ""
	OUTPUT "Board locations are as follows:"
	FOR i <- 1 TO 9 STEP 3
		OUTPUT i, i+1, i+2
	NEXT i
	OUTPUT ""
	OUTPUT "Current board"
	CALL Print
ENDPROCEDURE

// Procedure TO Print out the board 
PROCEDURE Print
	FOR i <- 1 TO TTT_Length STEP 3
		OUTPUT TTT[i], TTT[i+1], TTT[i+2]
	NEXT i
ENDPROCEDURE

// Function TO check IF there is a Winner
FUNCTION checkWin(Player1_turn: BOOLEAN) RETURNS BOOLEAN
	DECLARE Symbol : CHAR
	DECLARE Win : BOOLEAN

	Win <- FALSE
	
	IF Player1 THEN
		Symbol <- 'X'		
	ELSE
		Symbol <- 'O'
	ENDIF

	IF (TTT[1] = Symbol AND TTT[2] = Symbol AND TTT[3] = Symbol) OR
           (TTT[4] = Symbol AND TTT[5] = Symbol AND TTT[6] = Symbol) OR
           (TTT[7] = Symbol AND TTT[8] = Symbol AND TTT[9] = Symbol) OR
           (TTT[1] = Symbol AND TTT[4] = Symbol AND TTT[7] = Symbol) OR
           (TTT[2] = Symbol AND TTT[6] = Symbol AND TTT[8] = Symbol) OR
           (TTT[3] = Symbol AND TTT[6] = Symbol AND TTT[9] = Symbol) OR
           (TTT[1] = Symbol AND TTT[5] = Symbol AND TTT[9] = Symbol) OR
           (TTT[3] = Symbol AND TTT[5] = Symbol AND TTT[7] = Symbol) THEN
		Win <- TRUE
	ENDIF

	RETURN Win

ENDFUNCTION

// Function TO check IF a location is Empty
FUNCTION isEmpty(location: INTEGER) RETURNS BOOLEAN
	DECLARE Empty: BOOLEAN
	IF TTT[location] = '_' THEN 
		Empty <- TRUE
	ENDIF
    RETURN Empty
ENDFUNCTION

// Function TO get a valid location
FUNCTION getposition(prompt : STRING) RETURNS INTEGER
	OUTPUT prompt, ">"
	INPUT Choice
	WHILE Choice > 9 OR Choice < 1 OR isEmpty(Choice) = FALSE DO
		OUTPUT "Invalid Choice", Choice, "value should be 1 TO 9 and location should be Empty"
		OUTPUT prompt, ">"
		INPUT Choice
	ENDWHILE
	RETURN Choice
ENDFUNCTION

PROCEDURE play
	WHILE Count <> 9 AND Finished = FALSE DO
		IF Player1 THEN
			TTT[ getposition("Player1" )] <- 'X'
		ELSE
			TTT[ getposition("player2" )] <- 'O'
		ENDIF
	
		Count  <- Count + 1
		IF Player1 THEN
			IF checkWin(Player1) THEN
				OUTPUT "**** Player1 Wins ****"
				Finished <- TRUE
			ENDIF
			Player1 <- FALSE
		ELSE
			IF checkWin(Player1) THEN
				OUTPUT "**** Player2 Wins ****"
				Finished <- TRUE
			ENDIF
			Player1 <- TRUE
		ENDIF
		CALL Print
	ENDWHILE

ENDPROCEDURE


// Main code starts here ....
CALL Setup
CALL play
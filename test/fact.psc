// Program to calculate 5 factorial

DECLARE I : INTEGER         // Counter
DECLARE FACT : INTEGER      // Total

FACT <-1
I <- 1

WHILE I < 6 DO
    FACT <- FACT * I 
    I <- I + 1
ENDWHILE

PRINT FACT
DECLARE Unsorted : ARRAY[1 : 10] OF INTEGER
Unsorted[1] <- 5
Unsorted[2] <- 1
Unsorted[3] <- 3
Unsorted[4] <- 2
Unsorted[5] <- 8
Unsorted[6] <- 7
Unsorted[7] <- 6
Unsorted[8] <- 4
Unsorted[9] <- 10
Unsorted[10] <- 9

DECLARE Swap : BOOLEAN
DECLARE I : INTEGER

Swap <- TRUE
I <- 2

WHILE Swap = TRUE AND I < 10 DO

    Swap <- FALSE
    FOR J <- 1 TO I
        IF Unsorted[J] > Unsorted[J+1] THEN
            DECLARE Temp : INTEGER
            Temp <- Unsorted[J]
            Unsorted[J] <- Unsorted[J+1]
            Unsorted[J+1] <- Temp
            Swap <- TRUE
        ENDIF
    NEXT J

    I <- I + 1

ENDWHILE

FOR K <- 1 TO 10
    OUTPUT Unsorted [K]
NEXT K


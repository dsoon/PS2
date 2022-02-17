
DECLARE Swap : BOOLEAN
DECLARE I : INTEGER
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

Swap <- TRUE
I <- 1

WHILE Swap = TRUE AND I <= 10 DO

    I <- I + 1

ENDWHILE


DECLARE data : ARRAY[0:9] OF INTEGER
DECLARE next : ARRAY[0:9] OF INTEGER
DECLARE start : INTEGER
DECLARE free : INTEGER
DECLARE current : INTEGER
DECLARE end : INTEGER

free <- 0
start <- -1
end <- -1
FOR index <- 0 TO 9
              next[index] <- index+1
NEXT index
next[9]<- -1

FOR index<- 0 TO 9
              data[index] <- 0 
NEXT index

FUNCTION AddToHead(DATA:INTEGER) RETURNS BOOLEAN
              
              IF IsFull = TRUE THEN
                           RETURN FALSE
              ELSE
              IF IsEmpty = TRUE THEN
                            end <- free
              ENDIF
                            data[free] <- DATA
                            current <- start
                            start <- free
                            free <- next[free]
                            next[start] <- current 
                            RETURN TRUE
              ENDIF
ENDFUNCTION
              
FUNCTION RemoveFromHead() RETURNS INTEGER
              
              IF IsEmpty = TRUE THEN
                           RETURN 0
              ELSE
                           
                           DATA <- data[start]
                           data[start] <-0
                           IF start = end THEN
                                         next[start]<- free
                                         free <- end
                                         start <- -1 
                                         end <- -1
                           ELSE 
                           
                                         current <- free
                                         free <- start
                                         next[free] <- current
                                         start <- next[start]
                                         RETURN DATA
                           ENDIF
              ENDIF
ENDFUNCTION 
                            
FUNCTION RemoveFromTail RETURNS INTEGER
              
              IF IsEmpty= TRUE THEN
                           RETURN 0
              ELSE
                           DATA <- data[end]
                           data[end]<- 0
                           IF start = end THEN
                                         next[end] <- free
                                         free <- end
                                         start <- -1 
                                         end <- -1
                                         
                           ELSE 
                                         FOR X <- 1 TO LENGTH(next)
                                                       IF next[X] = end THEN
                                                                     next[X] <- -1
          end <- X
                                                       ENDIF
                                         NEXT X
                                         current <- free
                                         free <- end
                                         next[end] <- current

                                         RETURN DATA 
                           ENDIF
              ENDIF
ENDFUNCTION
              
                           
FUNCTION IsEmpty() RETURNS BOOLEAN
              
              IF free=0 THEN
                           RETURN TRUE
              ELSE
                           RETURN FALSE
              ENDIF
ENDFUNCTION

FUNCTION IsFull() RETURNS BOOLEAN
              
              IF free=-1 THEN
                           RETURN TRUE
              ELSE
                           RETURN FALSE
              ENDIF
ENDFUNCTION

FOR X <- 1 TO 10
              OUTPUT AddToHead(X)
NEXT X

FOR X<- 1 TO 10
              OUTPUT RemoveFromTail
NEXT X

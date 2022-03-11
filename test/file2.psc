DECLARE FileName : STRING
DECLARE Search : STRING
DECLARE Count : INTEGER
DECLARE Found : BOOLEAN
DECLARE Line : STRING

FileName <- "myfile"
Search <- "hello"
Count <- 0
Found <- FALSE

OPENFILE FileName FOR READ

WHILE NOT EOF(FileName) AND NOT Found DO
    READFILE FileName, Line
 
    IF LENGTH(Line) = LENGTH(Search) THEN
        Found <- MID(Line, 1, LENGTH(Search)) = Search          
        Count <- Count + 1
    ENDIF
ENDWHILE

OUTPUT Count

CLOSEFILE FileName
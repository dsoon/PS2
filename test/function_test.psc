FUNCTION add (i: INTEGER, j: INTEGER) RETURNS INTEGER    
    IF i > j THEN
        RETURN i + j
    ELSE
        RETURN i - j
    ENDIF
    //OUTPUT "Nothing returned"
ENDFUNCTION
PRINT 1+add(5,4)
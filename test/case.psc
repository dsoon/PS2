DECLARE In : STRING
OUTPUT "Type in one of the following letters (W, A, S, D)"
INPUT In
CASE OF In
    "W" : OUTPUT "You typed in W" BREAK
    "A" : OUTPUT "You typed in A" BREAK
    "S" : OUTPUT "You typed in S" BREAK
    "D" : OUTPUT "You typed in D" BREAK
    OTHERWISE : OUTPUT "Do as you are told!" BREAK
ENDCASE
OUTPUT "All Done"
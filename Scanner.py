import Token
import PS2

class Scanner:
    def __init__(self, source):
        self.start = 0
        self.current = 0
        self.line = 1

        self.tokens = []
        self.source = source

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token.Token(Token.TokenType.EOF, "", None, self.line))
        return self.tokens;

    def scanToken(self):
        c = self.advance()

        if c == "(":
            self.addToken(Token.TokenType.LEFT_PAREN)

        elif c == ")":
            self.addToken(Token.TokenType.RIGHT_PAREN)

        elif c == "{":
            self.addToken(Token.TokenType.LEFT_BRACE)

        elif c == "}":
            self.addToken(Token.TokenType.RIGHT_BRACE)

        elif c == ",":
            self.addToken(Token.TokenType.COMMA)

        elif c == ".":
            self.addToken(Token.TokenType.DOT)

        elif c == "-":
            self.addToken(Token.TokenType.OPERATOR, c)

        elif c == "+":
            self.addToken(Token.TokenType.OPERATOR, c)

        elif c == "-":
            self.addToken(Token.TokenType.SEMICOLON)

        elif c == ":":
            self.addToken(Token.TokenType.COLON)

        elif c == "*":
            self.addToken(Token.TokenType.OPERATOR, c)

        elif c == "!":
            self.addToken(Token.TokenType.OPERATOR, "!=" if self.match("=") else "!")

        elif c == "=":
            self.addToken(Token.TokenType.OPERATOR, "==" if self.match("=") else "=")

        elif c == "<":

            if self.match("=") : # matching <=
                self.addToken(Token.TokenType.OPERATOR, "<=")

            elif self.match("-"): # matching <- assignment
                self.addToken(Token.TokenType.ASSIGNMENT, "<-")

            else: # just <
                self.addToken(Token.TokenType.OPERATOR, "<")

        elif c == ">":
            self.addToken(Token.TokenType.OPERATOR, ">=" if self.match("=") else ">")

        elif c == "/":
            if self.match('/'): # got a slash
                while self.peek() != "\n" and not self.isAtEnd(): 
                    self.advance()
            else:
                self.addToken(Token.TokenType.OPERATOR, "/")

        elif c == " " or c == "\r" or c == "\t":
          pass

        elif c == "\n":
            self.line += 1

        elif c == '"':
            self.string()

        else:
            if c.isdigit():
                self.number()

            elif c.isalpha() or c == '_':
                self.identifier()

            else:
                PS2.PS2.error(self.line, f"unrecognised token '{c}'")
    
    def match(self, expected):
        if self.isAtEnd():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True


    def addToken(self, *args, **kwargs):
        if len(args) == 1:
            self.addToken(args[0], None)

        else: #length == 2
            self.tokens.append(Token.Token(args[0], self.source[self.start:self.current], args[1], self.line))

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def isAtEnd(self):
        return self.current >= len(self.source)
        

    def peek(self):
        if self.isAtEnd(): 
            return ""

        return self.source[self.current]
  
    def peekNext(self):
        if self.current + 1 > len(self.source): 
            return ""
            
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.isAtEnd():
            PS2.PS2.error(self.line, "unterminated string")
            return

        self.advance() # closing "
        # trim surrounding string

        value = self.source[self.start + 1 : self.current -1]
        self.addToken(Token.TokenType.STRING, value)

    def number(self):
        
        while self.peek().isdigit():
            self.advance()

        # Look for a fractional part.
        if self.peek() == "." and self.peekNext().isdigit():
            
            # Consume the "."
            self.advance()

            while self.peek().isdigit(): 
                self.advance()

            self.addToken(Token.TokenType.REAL, float(self.source[self.start:self.current]))
        else:
            self.addToken(Token.TokenType.INTEGER, int(self.source[self.start:self.current]))
    
    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        identifier = self.source[self.start:self.current]
        if identifier in Token.keywords:
            self.addToken(Token.keywords[identifier])
        else:    
            self.addToken(Token.TokenType.IDENTIFIER, identifier)
        
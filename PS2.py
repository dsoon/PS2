import Scanner
import Parser

class PS2:
    
    hadError = False

    def runFile(fileName):
        with open(fileName) as file:
            lines = file.readlines()
            for line in lines:
                PS2.run(line)

    def runPrompt():
        while True:
            try:
                line = input("> ")
                PS2.run(line)
            except EOFError: # catches CNTL-D - EOF
                print("quiting ...")
                break

    def run(source):
        scanner =  Scanner.Scanner(source)
        tokens = scanner.scanTokens()
        for t in tokens:
            print(f"{t}")

        parser = Parser.Parser(tokens)
        parser.parse() 

    def error(line, message):
        PS2.report(line, "", message)

    def report(line, where, message):
         print(f"[line {line}] Error {where} : {message}")
         PS2.hadError = True

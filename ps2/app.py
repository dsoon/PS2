import os

from ps2.symbol_table.environment import Environment
from ps2.scan.scanner import Scanner
from ps2.parser.parser import Parser
from ps2.interpret.interpretor import Interpretor

class PS2:
    
    hadError = False

    def report(line, where, message):
         print(f"\n[line {line}] {where} error: {message}")
         PS2.hadError = True

    # Run Interpretor from a file
    def runFile(fileName):
        try:
            with open(fileName) as file:
                lines = file.readlines()

                start_dir = os.getcwd()

                given_dir = os.path.dirname(fileName)
                new_dir   = os.path.realpath(os.path.join(start_dir, given_dir))

                os.chdir(new_dir)

                PS2.run("".join(lines))

                os.chdir(start_dir)
        except FileNotFoundError:
            print(f"Error: script '{fileName}' does not exist")

    # Run Interpretor interactively
    def runPrompt():
        while True:
            try:

                lineno = 1
                prog = []
                Environment.reset()
                PS2.hadError = False
                
                while True:
                    try :
                        line = input(f"{lineno}> ")

                        # . command to run the program
                        if len(line) == 1 and line[0] == ".":  
                            PS2.run("".join(prog))
                            break
                        
                        elif line.startswith(".run"):
                            PS2.runFile(line[4:].strip())
                            lineno = 0

                        elif line == ".quit":
                            raise EOFError

                        prog.append(line+'\n')
                        lineno += 1

                    except SyntaxError as e:
                        PS2.report(e.msg[0], "Syntax", e.msg[1])
                        PS2.hadError = False

                    except RuntimeError:
                        PS2.hadError = False


            except EOFError: # catches CNTL-D - EOF
                print("Ending session ...")
                break

    def run(source):

        try:
            tokens     = Scanner(source).scanTokens()        
            statements = Parser(tokens).parse()
        except SyntaxError as e:
            PS2.report(e.msg[0], "Syntax", e.msg[1])

        if not PS2.hadError:
            try:
                Interpretor(statements).interpret()
            except RuntimeError as e:
                PS2.report(e.args[0][0], "Runtime", e.args[0][1])
        else:
            PS2.hadError = False


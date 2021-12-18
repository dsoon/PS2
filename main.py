import sys
import PS2

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Usage: python PS2 <file>")
    elif len(sys.argv) == 2:
        PS2.PS2.runFile(sys.argv[1])
    else:
        PS2.PS2.runPrompt()

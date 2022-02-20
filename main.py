import sys
import ps2

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Usage: python PS2 <file>")
    elif len(sys.argv) == 2:
        ps2.PS2.runFile(sys.argv[1])
    else:
        ps2.PS2.runPrompt()

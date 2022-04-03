import sys
from ps2.app import PS2 as PS2

if len(sys.argv) > 1:
  if sys.argv[1] == "-file" or sys.argv[1] == "-f":
    try:
      PS2.runFile(sys.argv[2])
    except IndexError:
      print("Invalid or blank file path provided - provide path relative to exec dir")

if __name__ == "__main__":
    PS2.runPrompt()

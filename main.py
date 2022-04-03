import sys
from ps2.app import PS2 as PS2

if len(sys.argv) > 1:
  if "-f" in sys.argv or "-file" in sys.argv:
    try:
      ind = (sys.argv).index("-f")
    except ValueError:
      ind = (sys.argv).index("-file")
    try:
      PS2.runFile(sys.argv[ind+1])
    except IndexError:
      print("File argument was blank, check syntax")

if __name__ == "__main__":
    PS2.runPrompt()

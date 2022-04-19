import argparse

from ps2.app import PS2 as PS2

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="specify .psc file to run")
args = parser.parse_args()

if args.file:
  PS2.runFile(args.file)

if __name__ == "__main__":
    PS2.runPrompt()

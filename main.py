if __name__ == "__main__":
    import argparse    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="specify .psc file to run")
    args = parser.parse_args()

    from ps2.app import PS2 as PS2
    
    if args.file:
        PS2.runFile(args.file)
    else:
        PS2.runPrompt()

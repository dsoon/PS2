# Use this program to check if TokenType has all the valid tokens
# defined by Token.txt

import Token
print(f"Token test")

token_values = []
for t in Token.TokenType:
    token_values.append(t.value)

with open("Token.txt") as tokens:
    lines = tokens.readlines()
    for line in lines:
        toks = line.strip().split()
        if len(toks) > 0 and toks[0] == "#":
            continue
            
        for t in toks:
            if t not in token_values:
                print(f"{t} not found in TokenType")


print("Creating keyword dictionary")
print("---------------------------")
print("keywords = {")
for v in token_values:
    print(f"\t\"{v}\": TokenType.{v},")

print("}")

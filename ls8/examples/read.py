import sys
# try:
#     file = open("print8.ls8", 'r')
#     lines = file.read()
#     print(lines)

#     raise Exception("oh nooo")

# except Exception:
#     print(file.closed)

# Could also do...

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} filename")
    sys.exit(2)
program = []
counter = 0

# with open("print8.ls8") as file:
# with sys.argv it will pass in whichever file you declare on command line. eg.. python3 read.py print8.ls8
# argv[1] would be print8.ls8
# argv[0] would be read.py
try:
    with open(sys.argv[1]) as file:
        for line in file:
            comment_split = line.split("#")
            number_string = comment_split[0].strip()
            # program[counter] = line
            # counter += 1
            # print(line)
            if number_string == '':
                continue
            else:
                num = int(number_string, 2)  # covert from base 2 (binary) to decimal
                print(f'{number_string} binary is {num} in decimal')
except FileNotFoundError:
    print(f'{sys.argv[0]}: could not find {sys.argv[1]}')
    sys.exit(2)

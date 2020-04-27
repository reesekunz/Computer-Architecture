import sys

# commands assigned to a value
print_tim = 1
halt = 2
print_num = 3
save = 4
print_register = 5
add = 6

# put commands in memory. this is mimicking our underlying memory.
# put print_num before 14.
# each print_tim could also be replaced with 1.
# memory = [
#     print_tim,
#     print_tim,
#     print_tim,
#     print_num,
#     14,
#     save,
#     99,
#     2,
#     save,
#     101,
#     1,
#     add,
#     1,
#     2,
#     print_register,
#     1,
#     halt

# ]
memory = []  # Dont need to hardcode anymore


# store 99 into register 2.
# store 101 into register 1
# register1 = register1 + register2


running = True
counter = 0

# register - variables with fixed names (R0-R7) that are really fast to access since physically located right on the CPU (like your house).
# caches - pretty close to register but not as good (like a shed). Use when run out of registers. L1, L2
# RAM - far away from CPU (like a warehouse). use when run out of caches.

registers = [0] * 8  # [0, 0, 0, 0, 0, 0, 0, 0]

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} filename")
    sys.exit(2)
    # program = []
    # counter = 0

# with open("print8.ls8") as file:
# with sys.argv it will pass in whichever file you declare on command line. eg.. python3 read.py print8.ls8
# argv[1] would be print8.ls8
# argv[0] would be read.py


def load_memory(filename):
    try:
        address = 0  # front of memory array
        with open(filename) as file:
            for line in file:
                comment_split = line.split("#")
                number_string = comment_split[0].strip()
                # program[counter] = line
                # counter += 1
                # print(line)
                if number_string == '':
                    continue
                else:
                    # covert from base 2 (binary) to decimal
                    num = int(number_string, 2)
                    print(f'{number_string} binary is {num} in decimal')
                    memory[address] = num
                    address += 1
                    
    except FileNotFoundError:
        print(f'{sys.argv[0]}: could not find {sys.argv[1]}')
        sys.exit(2)


load_memory(sys.argv[1])


while running is True:
    command = memory[counter]
    if command == print_tim:
        print("Tim!")
        # move counter up one byte in memory (go from print_tim to next print_tim)
        counter += 1
    elif command == print_num:
        counter += 1
        print(memory[counter])
        # these two lines ^ could be simplified with print(memory[counter+1])
        counter += 1
        # but then would need counter += 2 instead of 1
    elif command == save:
        # store 99 into register 2.
        register_index = memory[counter + 2]
        number_to_save = memory[counter + 1]
        registers[register_index] = number_to_save
        # same as ... registers[memory[counter + 2]] = memory[counter + 1]
        counter += 3
    elif command == print_register:
        # print out the contents of register 2.
        register_index = memory[counter + 1]
        print(registers[register_index])
        counter += 2
    elif command == add:
        # reg1 = reg1 + reg2
        # grab indexes from memory
        register_index_1 = memory[counter+1]
        register_index_2 = memory[counter + 2]
        # grab values at each index and add them together.
        registers[register_index_1] = registers[register_index_1] + \
            registers[register_index_2]
        counter += 3

    elif command == halt:
        # break out of loop
        running = False

    else:
        print('Error!!')
        # exits python program
        sys.exit(1)

# prints out
# Tim!
# Tim!
# Tim!
# 14
# 200

# Data driven machine - stored our program as data in memory. Dont have to change any logic, just our data.

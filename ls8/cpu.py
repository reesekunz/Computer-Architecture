"""CPU functionality."""

import sys

# HLT = 1 (doing this in self.opcodes below instead)


class CPU:
    """Main CPU class."""

    # STEP 1: Add the constructor to `cpu.py

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # [0, 0, 0, ...]
        self.registers = [0] * 8
        # initialize program counter
        self.pc = 0
        # The SP points at the value at the top of the stack (most recently pushed), or at address `F4` if the stack is empty.
        self.registers[7] = 0xF4

    # STEP 4: Implement the `HLT` instruction handler
    # HLT machine code: 00000001 (from spec)

    # STEP 5: Implement the `LDI` instruction handler
    # LDI machine code: 10000010

    # STEP 6 : Implement the `PRN` instruction handler
    # PRN machine  code: 01000111

    # STEP 8: Implement a Multiply and Print the Result
    # MUL machine code: 10100010

    # Program instructions for these opcodes are being handled in the run() function

        self.opcodes = {
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b10100010: "MUL"
        }

    # STEP 9: Beautify your `run()` loop (part 2 is bottom of this file)
        self.branchtable = {
            "HLT": self.hlt,
            "LDI": self.ldi,
            "PRN": self.prn,
            # "MUL": self.mul -> MUL doesnt go here since it is an alu. Only non ALU operations need to be passed in here (see lines 191-197)
        }

    # STEP 2: Add RAM functions
    # You don't need to add the MAR or MDR to your `CPU` class, but they would make handy parameter names for

    # `ram_read()` should accept the address to read and return the value stored there.
    # The MAR contains the address that is being read or written to.
    def ram_read(self, mar):
        return self.ram[mar]

    # `ram_write()` should accept a value to write, and the address to write it to.
    # The MDR contains the data that was read or the data to write.
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    # filename param comes from cpu.load(sys.argv[1]) in ls8.p8. Were passing filename in as sys.argv[1] so we access the file through the terminal command.
    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

       # STEP 7: Un-hardcode the machine code
       # Very similar to what we did with guided project load_memory()
       # Can now run python3 ls8.py examples/print8.ls8 in terminal (returns 8)
        try:
            with open(filename) as file:
                for line in file:
                    comment_split = line.split("#")
                    number_string = comment_split[0].strip()

                    if number_string == "":
                        continue

                    num = int(number_string, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: could not find {sys.argv[1]}')
            sys.exit(2)

            for instruction in program:
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # elif op == "SUB": etc
        # Multiply command from MUL command added in step 8
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

     # STEP 3: Implement the core of `CPU`'s `run()` method


# local variables to include in run():
# Read the memory address thats stored in register 'PC'
# Store the result of that memory address in the 'IR' (instruction register)

# Some instructions requires up to the next two bytes of data _after_ the `PC` in
# memory to perform operations on. Sometimes the byte value is a register number,
# other times it's a constant value (in the case of `LDI`).

# Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
# `operand_b` in case the instruction needs them.

# Depending on the value of the opcode, perform the actions needed for the
# instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other
# options, too.

# After running code for any particular instruction, the `PC` needs to be updated
# to point to the next instruction for the next iteration of the loop in `run()`.
# The number of bytes an instruction uses can be determined from the two high bits
# (bits 6-7) of the instruction opcode. See the LS-8 spec for details.

    def run(self):
        """Run the CPU."""
        running = True

        while running is True:

            # Meanings of the bits in the first byte of each instruction: `AABCDDDD`

            # * `AA` Number of operands for this opcode, 0-2
            # * `B` 1 if this is an ALU operation
            # * `C` 1 if this instruction sets the PC
            # * `DDDD` Instruction identifier

            # Read the memory address thats stored in register 'PC'. Store the result of that memory address in the 'IR' (instruction register) as a local variable.

            IR = self.ram_read(self.pc)
            # Could also do... IR = self.ram(self.pc)

            # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # 0b 1011 1111
            num_operands = (IR >> 6)  # right shift 6 to get 'AA'
            # = 0b 10

            # * `C` 1 if this instruction sets the PC
            # Shift 4 then masking to see if C is set to 1. Will return 1 if True, 0 if False.
            sets_pc = ((IR >> 4) & 0b0001) == 1

            # `B` 1 if this is an ALU operation.
            # Shift 5 then masking to see if B is set to 1. Will return 1 if True, 0 if False.
            is_alu_operation = ((IR >> 5) & 0b0001) == 1

            opcode = self.opcodes[IR]

            # Instructions that set the PC from spec are call, return, jump.
            if not sets_pc:
                self.pc += 1 + num_operands

            if is_alu_operation:
                self.alu(opcode, operand_a, operand_b)
            # Can now run python3 ls8.py examples/mult.ls8 (returns 72) ^^

            # Not an alu operation. Need to look up in branchtable.
            else:
                self.branchtable[opcode](operand_a, operand_b)

            # Set the value of a register to an integer (already got the values out with operand_a and operand_b)
            if opcode == "LDI":
                self.registers[operand_a] = operand_b

            # Print numeric value stored in the given register.
            elif opcode == "PRN":
                print(self.registers[operand_a])

            # We can consider `HLT` to be similar to Python's `exit()` in that we stop whatever we are doing, wherever we are.
            elif opcode == 'HLT':
                # Exit the system
                sys.exit(0)
    # # STEP 9 (cont.): Beautify your `run()` loop
    # these helper functions are part of our branch table (using them to clean up our run function)

    def hlt(self, _, __): # Python needs us to pass in 3 arguments even though we dont care about the other 2.
        self.running = False
        # could also use sys.exit(0)

    def prn(self, operand_a, _): 
        print(self.registers[operand_a])

    def ldi(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b

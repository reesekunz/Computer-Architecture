"""CPU functionality."""
# SPRINT CHALLENGE MVP requirements:
    # 1. Add the `CMP` instruction and `equal` flag to your LS-8
        # CMP is an instruction handled by the ALU => like MUL it doesnt go in branchtable or have its own function.
        # CMP machine code: 10100111

    # 2. Add the `JMP` instruction

    # 3. Add the `JEQ` and `JNE` instructions

    # any note with an '*' next to it and its corresponding code is related to the sprint challenge

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
        # *initialize flag
        self.fl = 0b00000000

    # STEP 4: Implement the `HLT` instruction handler
    # HLT machine code: 00000001 (from spec)

    # STEP 5: Implement the `LDI` instruction handler
    # LDI machine code: 10000010

    # STEP 6 : Implement the `PRN` instruction handler
    # PRN machine  code: 01000111

    # STEP 8: Implement a Multiply and Print the Result
    # MUL machine code: 10100010

    # STEP 10: Implement System Stack. Add `PUSH` and `POP` instructions.
    # PUSH machine code: 01000101
    # POP machine  code: 01000110

    # STEP 11: Implement Subroutine Calls. Add 'CALL' and "RET" instructions.
    # CALL machine code: 01010000
    # RET (return) machine code: 00010001

    # *Sprint Challenge Step 2: Add the `JMP` instruction
    # *JMP machine code: 01010100

    # *Sprint Challenge Step 3: Add the `JEQ` and `JNE` instructions
    # *JEQ machine code: 01010101
    # *JNE machine code: 01010110

    # Program instructions for these opcodes are being handled in the run() function

        self.opcodes = {
            0b00000001: "HLT",
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b01010000: "CALL",
            0b00010001: "RET",
            # Was getting KeyError: 160. bin(160) = 0b10100000, which is the machine code for ADD. Error meant I was missing the ADD code. ADD is already an ALU operation so dont need to add it to branchtable or as helper function at bottom.
            0b10100000: "ADD",
            0b10100111: "CMP",
            0b01010100: "JMP",
            0b01010101: "JEQ",
            0b01010110: "JNE"

        }

    # STEP 9: Beautify your `run()` loop
    # These are all separate helper functions that we define at the bottom
        self.branchtable = {
            "HLT": self.hlt,
            "LDI": self.ldi,
            "PRN": self.prn,
            # "MUL": self.mul -> MUL doesnt go here since it is an alu. Only non ALU operations need to be passed in here (see lines 191-197)
            "PUSH": self.push,
            "POP": self.pop,
            "CALL": self.call,
            "RET": self.ret,
            # *Dont need CMP since its an alu.
            "JMP": self.jmp,
            "JEQ": self.jeq,
            "JNE": self.jne
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
        # Multiply command from MUL command added in step 8
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        # *Compare the values in two registers.
            # *If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
            # *If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
            # *If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.

        # *`FL` bits: `00000LGE`
        elif op == "CMP":
            # *Grab the values from the two registers
            register_A_value = self.registers[reg_a]
            register_B_value = self.registers[reg_b]

            # *equal
            if register_A_value == register_B_value:
                # *set Equal 'E' flag to 1. (True) => 0b00000001
                self.fl = 0b00000001

            # *less than
            elif register_A_value < register_B_value:
                # *set the Less-than `L` flag to 1 => 0b00000100
                self.fl = 0b00000100

             # *greater than
            elif register_A_value > register_B_value:
                # *set the Greater-than `G` flag to 1
                self.fl = 0b00000010

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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

            # If handler sets PC directly, we dont want to to advance PC to the next instruction (eg. 'CALL' or "JMP")
            if not sets_pc:
                self.pc += 1 + num_operands

            if is_alu_operation:
                self.alu(opcode, operand_a, operand_b)
            # Can now run python3 ls8.py examples/mult.ls8 (returns 72) ^^

            # Not an alu operation. Need to look up in branchtable.
            else:
                self.branchtable[opcode](operand_a, operand_b)

            # These are now being handled below with ldi, prn, and hlt helper functions so dont need it here. Keeping for future reference.

            # Set the value of a register to an integer (already got the values out with operand_a and operand_b)
            # if opcode == "LDI":
            #     self.registers[operand_a] = operand_b

            # # Print numeric value stored in the given register.
            # elif opcode == "PRN":
            #     print(self.registers[operand_a])

            # # We can consider `HLT` to be similar to Python's `exit()` in that we stop whatever we are doing, wherever we are.
            # elif opcode == 'HLT':
            #     # Exit the system
            #     sys.exit(0)

    # # STEP 9 (cont.): Beautify your `run()` loop
    # these helper functions are part of our branch table (using them to clean up our run function)

    # Python needs us to pass in 3 arguments even though we dont care about the other 2.
    def hlt(self, _, __):
        # exit the system
        sys.exit(0)
        # could also use self.running = False

    def prn(self, operand_a, _):
        print(self.registers[operand_a])

    def ldi(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b

    # Can now run python3 ls8.py examples/stack.ls8 with Push and Pop methods (should return: 2, 4, 1).

    def push(self, operand_a, _):
        # Decrement the SP (stack pointer)
        self.registers[7] -= 1
        # Copy the value in the given register to the address pointed to by`SP`.
        stack_pointer = self.registers[7]
        value = self.registers[operand_a]

        self.ram_write(stack_pointer, value)

    def pop(self, operand_a, _):
        # Copy the value from the address pointed to by `SP` to the given register.
        stack_pointer = self.registers[7]
        value = self.ram_read(stack_pointer)

        self.registers[operand_a] = value
        # Increment `SP`.
        self.registers[7] += 1

    # Call - Calls a subroutine (function) at the address stored in the register.
    # Can now run python3 ls8.py examples/call.ls8 (should return 20, 30, 36, 60)
    def call(self, operand_a, _):
        # push instruction onto the stack
        self.registers[7] -= 1
        stack_pointer = self.registers[7]
        self.ram_write(stack_pointer, self.pc + 2)

        # Set pc to the adress stored in the given register.
        self.pc = self.registers[operand_a]

    # Ret - Return from subroutine. Pop the value from the top of the stack and store it in the `PC`.
    def ret(self, operand_a, _):

        stack_pointer = self.registers[7]
        address = self.ram_read(stack_pointer)

        self.pc = address

    #* Sprint Challenge 
    # In these cases, the `PC` does not automatically advance to the next instruction, since it was set explicitly.
    # Checking on line 262 if sets_pc. If it doesnt set pc we need to set it down here instead.

    def jmp(self, operand_a, _ ):
        # *Set pc to the adress stored in the given register.
        self.pc = self.registers[operand_a]

    # *If `equal` flag is set to True (1), jump to the address stored in the given register.
    # Equal 'E' flag to 1. (True) => 0b00000001
    # # *`FL` bits: `00000LGE`
    def jeq(self, operand_a, _):
        # masking to see if E = 1
        is_equal_flag = (self.fl & 0b00000001) == 1
        if is_equal_flag:
            # self.pc = self.registers[operand_a] same as...
            return self.jmp(operand_a, 0)
        else:
            self.pc += 2

    # If `E` flag is clear (false, 0), jump to the address stored in the given register.
    def jne(self, operand_a, _):
        # masking to see if E = 1
        is_equal_flag = (self.fl & 0b00000001) == 1
        # if E does NOT = 1
        if not is_equal_flag:
            # jump to the address stored in the given register.
            return self.jmp(operand_a, 0)
        else:
            self.pc += 2
            
        

        



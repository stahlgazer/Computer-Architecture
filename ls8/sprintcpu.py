"""CPU functionality."""
import sys
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.FL = None
        self.table = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b10100000: self.ADD,
            0b00010001: self.RET,
            0b01010000: self.CALL,
            0b10100111: self.CMP,
            0b01010110: self.JNE,
            0b01010101: self.JEQ,
            0b01010100: self.JMP,
        }
    
    def ADD(self, operand_a, operand_b):
        self.reg[operand_a] += self.reg[operand_b]
        self.pc += 3

    def CALL(self, operand_a, operand_b):
        self.push_value(self.pc + 2)
        self.pc = self.reg[operand_a]

    def RET(self, operand_a, operand_b):
        self.pc = self.pop_value()

    def push_value(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[SP])

    def pop_value(self):
        value = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        return value      

    def PUSH(self, operand_a, operand_b):
        self.push_value(self.reg[operand_a])     
        self.pc += 2

    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_value()                                       
        self.pc +=2     

    def HLT(self, operand_a, operand_b):
        sys.exit()

    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def MUL(self, operand_a, operand_b):
        self.reg[operand_a] *= self.reg[operand_b]
        self.pc += 3

    def JMP(self, operand_a, operand_b):
        address = self.reg[operand_a]
        self.pc = address

    def JEQ(self, operand_a, operand_b):
        address = self.reg[operand_a]
        if self.FL == 0b00000001:
            self.pc = address
        else:
            self.pc += 2

    def JNE(self, operand_a, operand_b):
        address = self.reg[operand_a]
        if self.FL != 0b00000001:
            self.pc = address
        else:
            self.pc += 2

    def CMP(self, operand_a, operand_b):
        A = self.reg[operand_a]
        B = self.reg[operand_b]
        if A == B:
            self.FL = 0b00000001
        else:
            self.FL = 0
        self.pc += 3

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""
        address = 0

        with open(program) as lines:
            for line in lines:
                line = line.split('#')
                # print(line)
                try:
                    value = int(line[0], 2)
                except ValueError:
                    continue
                self.ram[address] = value
                address += 1

    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.table:
                self.table[IR](operand_a, operand_b)
            else:
                print(f'Invalid instruction # {IR} at address # {self.pc}')
                sys.exit()
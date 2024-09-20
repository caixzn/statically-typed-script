class Opcode:
    PUSH = "PUSH"
    POP = "POP"
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    LT = "LT"
    GT = "GT"
    EQ = "EQ"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    JMP = "JMP"
    JZ = "JZ"
    STORE = "STORE"
    LOAD = "LOAD"
    HALT = "HALT"
    SWAP = "SWAP"
    DUP = "DUP"
    PRINT = "PRINT"


class Instruction:
    def __init__(self, opcode, operand=None):
        self.opcode = opcode
        self.operand = operand

    def __str__(self):
        if self.operand is None:
            return f"{self.opcode}"
        return f"{self.opcode} {self.operand}"


class SAMVirtualMachine:
    def __init__(self, instructions: list[Instruction]):
        self.instructions = instructions
        self.stack = []
        self.memory = [0] * 1024  # Simplified memory model with 1024 cells
        self.pc = 0  # Program counter

    def run(self):
        while True:
            if self.pc >= len(self.instructions):
                break
            instruction = self.instructions[self.pc]
            self.execute(instruction)
            self.pc += 1

    def execute(self, instruction: Instruction):
        if not isinstance(instruction, Instruction):
            return

        if instruction.opcode == Opcode.PUSH:
            self.stack.append(instruction.operand)
        elif instruction.opcode == Opcode.POP:
            self.stack.pop()
        elif instruction.opcode == Opcode.SWAP:
            a, b = self.stack.pop(), self.stack.pop()
            self.stack.append(a)
            self.stack.append(b)
        elif instruction.opcode == Opcode.ADD:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a + b)
        elif instruction.opcode == Opcode.SUB:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a - b)
        elif instruction.opcode == Opcode.MUL:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(a * b)
        elif instruction.opcode == Opcode.DIV:
            b, a = self.stack.pop(), self.stack.pop()
            if type(a) is int and type(b) is int:
                self.stack.append(a // b)  # Integer division
            else:
                self.stack.append(a / b)
        elif instruction.opcode == Opcode.LT:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(int(a < b))
        elif instruction.opcode == Opcode.GT:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(int(a > b))
        elif instruction.opcode == Opcode.EQ:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(int(a == b))
        elif instruction.opcode == Opcode.AND:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(int(a and b))
        elif instruction.opcode == Opcode.OR:
            b, a = self.stack.pop(), self.stack.pop()
            self.stack.append(int(a or b))
        elif instruction.opcode == Opcode.NOT:
            a = self.stack.pop()
            self.stack.append(int(not a))
        elif instruction.opcode == Opcode.JMP:
            self.pc = self.find_label(instruction.operand) - 1  # -1 because pc will be incremented
        elif instruction.opcode == Opcode.JZ:
            if self.stack.pop() == 0:
                self.pc = self.find_label(instruction.operand) - 1
        elif instruction.opcode == Opcode.STORE:
            self.memory[instruction.operand] = self.stack.pop()
        elif instruction.opcode == Opcode.LOAD:
            self.stack.append(self.memory[instruction.operand])
        elif instruction.opcode == Opcode.PRINT:
            print(self.stack.pop())
        elif instruction.opcode == Opcode.HALT:
            self.pc = len(self.instructions)  # End execution

    def find_label(self, label):
        for i, instruction in enumerate(self.instructions):
            if isinstance(instruction, str) and instruction.endswith(':'):
                if instruction[:-1] == label:
                    return i
        raise ValueError(f"Label not found: {label}")

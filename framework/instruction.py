# This file defines the Instruction class, which represents one instruction in
# a program trace.

class Instruction:
    
    def __init__(self):
        self.instruction_pc = 0x0
        self.next_pc = 0x0

        self.opcode_class = 0
        self.is_load = False     # opcode_class = 0
        self.is_store = False    # opcode class = 1
        self.is_op = False       # opcode class = 2
        self.is_branch = False   # opcode class = 3
        
        self.is_indirect = False
        self.is_conditional = False
        self.is_call = False
        self.is_return = False

        self.branch_target = 0x0
        self.is_branch_taken = False
        self.is_floating_point = False

    # Parses a line from the trace and populates the instance variables.
    def parse_instruction(self, instr):
        return True

    def load(self):
        return self.is_load

    def store(self):
        return self.is_store

    def op(self):
        return self.is_op

    def branch(self):
        return self.is_branch

    def floating_point(self):
        return self.is_floating_point

    # def get_pc(self):
    #     return self.instruction_pc

    # def get_next_pc(self):
    #     return self.next_pc
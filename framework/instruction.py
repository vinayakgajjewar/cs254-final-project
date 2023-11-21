# This file defines the Instruction class, which represents one instruction in
# a program trace.

class Instruction:
    
    # Static information

    instruction_address = 0x0
    next_address = 0x0

    opcode_class = 0
    is_load = False     # opcode_class = 0
    is_store = False    # opcode class = 1
    is_op = False       # opcode class = 2
    is_branch = False   # opcode class = 3

    is_floating_point = False
    
    # TODO
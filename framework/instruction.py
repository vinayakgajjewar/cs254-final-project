# This file defines the Instruction class, which represents one instruction in
# a program trace.
from enum import Enum

class RiscVType(Enum):
    R = 1   # register
    I = 2   # immediate
    S = 3   # store
    U = 4   # upper imm
    B = 5   # branch
    J = 6   # jump

class Instruction:
    # This dictionary can be extended as per need. Current focus is branching instructions.
    RiscVInstruction = {
        'add': RiscVType.R,
        'sub': RiscVType.R,
        'or': RiscVType.R,
        'xor': RiscVType.R,
        'and': RiscVType.R,
        'sll': RiscVType.R,
        'srl': RiscVType.R,
        'sra': RiscVType.R,
        'slt': RiscVType.R,
        'sltu': RiscVType.R,
        'addi': RiscVType.I,
        'xori': RiscVType.I,
        'ori': RiscVType.I,
        'andi': RiscVType.I,
        'ssli': RiscVType.I,
        'srli': RiscVType.I,
        'srai': RiscVType.I,
        'jal': RiscVType.J,
        'jalr': RiscVType.I,
        'beq': RiscVType.B,
        'bne': RiscVType.B,
        'blt': RiscVType.B,
        'bltu': RiscVType.B,
        'bge': RiscVType.B,
        'bgeu': RiscVType.B,
        'c.beqz': RiscVType.B,
        'c.bnez': RiscVType.B,
        'beqz': RiscVType.B,
        'bnez': RiscVType.B,
        'blez': RiscVType.B,
        'bgez': RiscVType.B,
        'bltz': RiscVType.B,
        'bgtz': RiscVType.B,
        'bgt': RiscVType.B,
        'ble': RiscVType.B,
        'bgtu': RiscVType.B,
        'bleu': RiscVType.B,
        'lw': RiscVType.I,
        'lh': RiscVType.I,
        'lhu': RiscVType.I,
        'lb': RiscVType.I,
        'lbu': RiscVType.I,
        'sw': RiscVType.S,
        'sh': RiscVType.S,
        'sb': RiscVType.S,
    }
    
    def __init__(self):
        self.instruction_pc = '0x0'
        self.next_pc = '0x0'

        self.inst = None    # instruction name
        self.type = None    # enum RiscVType

        self.branch_target = '0x0'
        self.is_branch_taken = False

    # Parses a line from the trace and populates the instance variables.
    def parse_riscv_instruction(self, curr_instr, next_instr):
        curr_split = curr_instr.split()
        if len(curr_split) < 5:  # section identifier
            return True
        self.instruction_pc = curr_split[2]
        self.inst = curr_split[4]
        if self.inst in self.RiscVInstruction.keys():
            self.type = self.RiscVInstruction[self.inst]

        next_split = next_instr.split()
        if len(next_split) >= 5:
            self.next_pc = next_split[2]

        if self.type == RiscVType.B:
            if curr_split[-2] == '+':
                self.branch_target = hex(int(self.instruction_pc, 16) + int(curr_split[-1], 10))
            elif curr_split[-2] == '-':
                self.branch_target = hex(int(self.instruction_pc, 16) - int(curr_split[-1], 10))
            if int(self.branch_target, 16) == int(self.next_pc, 16):
                self.is_branch_taken = True
        return True

    # compatibility with the zipped traces
    def parse_instruction(self, instr):
        self.instruction_pc, self.is_branch_taken = instr.split()
        return True

    def load(self):
        return self.inst == 'lw' or self.inst == 'lh' or self.inst == 'lhu' or self.inst == 'lb' or self.inst == 'lbu'

    def store(self):
        return self.type == RiscVType.S

    def branch(self):
        return self.type == RiscVType.B

    def indirect(self):
        return self.type == RiscVType.I

    def jump(self):
        return self.inst == 'jal' or self.inst == 'jalr'

    def conditional(self):
        return self.inst.startswith('c.')
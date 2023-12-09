# my idea is that each branch predictor will have their own testbench.py that
# drives the verilog, but we will have a single framework.py that provides
# predictor-agnostic functionality. all the different cocotb testbenches will
# use the functionality that we implement in framework.py
from instruction import Instruction

class BranchRecord:
    def __init__(self):
        # true if the branch is indirect, false otherwise
        self.in_indirect = False

        # true if the branch is a conditional, false otherwise
        self.is_conditional = False

        # true if the branch is a call, false otherwise
        self.is_call = False

        # true if the branch is a return, false otherwise
        self.is_return = False

        # the value of the branch's PC (program counter)
        self.pc = 0x0

        # the target of the branch if it's taken; branches that aren't conditionals
        # are always taken.
        self.branch_target = 0x0

class Evaluator:
    traces = {
        'dhrystone': '../riscv_traces/dhrystone.riscv.out',
        'vec-memcpy': '../riscv_traces/vec-memcpy.riscv.out',
        'rsort': '../riscv_traces/rsort.riscv.out',
        'qsort': '../riscv_traces/qsort.riscv.out',
        'mt-memcpy': '../riscv_traces/mt-memcpy.riscv.out',
    }

    def __init__(self):

        # We want to keep a tally of both correct predictions and mispredictions
        # (even though it seems redundant) so that if the user want to get the
        # misprediction statistics before going through all the branch records,
        # the results are accurate.
        self.num_correct_predicts = 0
        self.num_mispredicts = 0
        self.num_instructions = 0
        self.instructions = []  # stored only branch instructions
        self.curr_instr = 0 # to seek into self.instructions

    # Parse a trace file and read all instructions
    def load_riscv_trace(self, name):
        if not name in self.traces.keys():
            print("Requested trace does not exist!")
            return
        try:
            with open(self.traces[name], 'r') as trace:
                lines = trace.readlines()
                curr = 0
                while curr < len(lines) - 1:
                    instr = Instruction()
                    parsed = instr.parse_riscv_instruction(lines[curr].strip(), lines[curr+1].strip())
                    if not parsed:
                        print("Error parsing: ", lines[curr].strip())
                    if instr.branch():
                        self.instructions.append(instr)
                        self.num_instructions += 1
                    curr += 1
            print(f"Done loading trace file, found {self.num_instructions} instructions")
        except FileNotFoundError:
            print(f"The file '{self.traces[name]}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Parse a trace file and read all instructions
    def load_trace(self, path):
        try:
            with open(path, 'r') as trace:
                for line in trace:
                    #print(line)
                    instr = Instruction()
                    parsed = instr.parse_instruction(line)
                    if not parsed:
                        print("Error parsing: ", line)
                    if instr.branch():
                        self.instructions.append(instr)
                        self.num_instructions += 1
            print(f"Done loading trace file, found {self.num_instructions} instructions")
        except FileNotFoundError:
            print(f"The file '{path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def reset(self):
        self.num_correct_predicts = 0
        self.num_mispredicts = 0

        self.num_instructions = 0
        self.instructions.clear()
        self.curr_instr = 0

    # Return an object of type BranchRecord if there is still another branch
    # record left in the trace. Return None otherwise.
    def get_next_branch_record(self):
        if self.curr_instr >= self.num_instructions:
            print("No branch records left in the program trace")
            return None
        instr = self.instructions[self.curr_instr]
        # TODO: Populate more fields
        br = BranchRecord()
        br.pc = instr.instruction_pc
        br.branch_target = instr.branch_target
        return br

    # Reads the prediction made by the predictor and returns if the prediction
    # was correct or incorrect.
    # @param prediction: True if the prediction is correct and false otherwise.
    # prediction is of type cocotb.binary.BinaryValue
    def predict_branch(self, prediction):
        if self.curr_instr >= self.num_instructions:
            return None
        instr = self.instructions[self.curr_instr]

        print(f"Framework got {prediction} as the prediction")
        print(f"The correct prediction is {instr.is_branch_taken}")
        self.curr_instr += 1
        if prediction.integer == int(instr.is_branch_taken):
            print("Cool! Framework says you are correct")
            self.num_correct_predicts += 1
            return True
        self.num_mispredicts += 1
        return False
    
    # Print out current statistics. In my mind, the cocotb module should be able
    # to call this function multiple times even before it's finished predicting
    # the entire trace to get a sort of "running average" of mispredict rate.
    def calculate_misprediction_rate(self):
        num_total_predicts = self.num_correct_predicts + self.num_mispredicts
        mispredict_rate = (self.num_mispredicts / num_total_predicts)
        print(f"number of branches = {num_total_predicts}")
        print(f"number of correct predictions = {self.num_correct_predicts}")
        print(f"number of mispredictions = {self.num_mispredicts}")
        print(f"misprediction rate = {mispredict_rate}")
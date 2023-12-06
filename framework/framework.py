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

        # the PC of the instruction following the branch
        self.next_pc = 0x0   

class Evaluator:
    def __init__(self):
        self.num_correct_predicts = 0
        self.num_instructions = 0
        self.instructions = []  # stored only branch instructions
        self.curr_instr = 0 # to seek into self.instructions

    # Parse a trace file and read all instructions
    def load_trace(self):
        file_path = "my_file_path.txt"
        try:
            with open(file_path, 'r') as trace:
                for line in trace:
                    instr = Instruction()
                    parsed = instr.parse_instruction(line)
                    if not parsed:
                        print("Error parsing: ", line)
                    if instr.branch():
                        self.instructions.append(instr)
                        self.num_instructions += 1
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def reset(self):
        self.num_correct_predicts = 0
        self.num_instructions = 0
        self.instructions.clear()
        self.curr_instr = 0

    # Return an object of type BranchRecord if there is still another branch
    # record left in the trace. Return null otherwise.
    def get_next_branch_record(self):
        if self.curr_instr >= self.num_instructions:
            return None
        instr = self.instructions[self.curr_instr]
        # TODO: Populate more fields
        br = BranchRecord()
        br.pc = instr.instruction_pc
        br.next_pc = instr.next_pc
        br.branch_target = instr.branch_target
        return br

    # Reads the prediction made by the predictor and returns if the prediction was correct or incorrect.
    # @param prediction: True if branch taken, false if branch not taken
    def predict_branch(self, prediction):
        if self.curr_instr >= self.num_instructions:
            return None
        instr = self.instructions[self.curr_instr]
        self.curr_instr += 1
        if prediction == instr.is_branch_taken:
            self.num_correct_predicts += 1
            return True
        return False
    
    # This method provides a way for us to update the state of the predictor
    # after a prediction has been made. We'll provide the branch record and some
    # state information as well as whether or not the branch was taken.
    # Returns:
    # - 
    # TODO wrong place for this method? /bhavye: I guess so. Maybe this should be in Cocotb module?
    def update_predictor(self):
        pass
    
    # We want to give the misprediction rate per 1000 instructions
    def calculate_misprediction_rate(self):
        num_mispredicts = self.num_instructions - self.num_correct_predicts
        if (self.num_instructions != 0):
            mispredict_rate = (num_mispredicts / self.num_instructions) / 1000
        else:
            print("no instructions given; can't evaluate mispredict rate")
            return
        print(f"number of branches = {self.num_instructions}")
        print(f"number of correct predictions = {self.num_correct_predicts}")
        print(f"number of mispredictions = {num_mispredicts}")
        print(f"misprediction rate per 1000 instructions = {mispredict_rate}")

def get_prediction(dut):
    return 
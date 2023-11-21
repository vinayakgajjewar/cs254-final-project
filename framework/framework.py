# my idea is that each branch predictor will have their own testbench.py that
# drives the verilog, but we will have a single framework.py that provides
# predictor-agnostic functionality. all the different cocotb testbenches will
# use the functionality that we implement in framework.py

class BranchRecord:

    # true if the branch is indirect, false otherwise
    in_indirect = False

    # true if the branch is a conditional, false otherwise
    is_conditional = False

    # true if the branch is a call, false otherwise
    is_call = False

    # true if the branch is a return, false otherwise
    is_return = False

    # the value of the branch's PC (program counter)
    instruction_address = 0x0

    # the target of the branch if it's taken; branches that aren't conditionals
    # are always taken.
    branch_target = 0x0

    # the PC of the instruction following the branch
    next_address = 0x0

    def __init__(self):
        pass

class Framework:

    num_branches = 0
    num_correct_predicts = 0
    num_instructions = 0

    # Return an object of type BranchRecord if there is still another branch
    # record left in the trace. Return false otherwise.
    def get_next_branch_record(self):
        print("getting the next branch...")

    def predict_branch(self):
        pass
    
    # This method provides a way for us to update the state of the predictor
    # after a prediction has been made. We'll provide the branch record and some
    # state information as well as whether or not the branch was taken.
    # Returns:
    # - 
    # TODO wrong place for this method?
    def update_predictor(self):
        pass
    
    # we want to give the misprediction rate per 1000 instructions
    def calculate_misprediction_rate(self):
        num_mispredicts = self.num_branches - self.num_correct_predicts
        if (self.num_instructions != 0):
            mispredict_rate = (num_mispredicts / self.num_instructions) / 1000
        else:
            print("no instructions given; can't evaluate mispredict rate")
            return
        print(f"number of branches = {self.num_branches}")
        print(f"number of correct predictions = {self.num_correct_predicts}")
        print(f"number of instructions = {self.num_instructions}")
        print(f"number of mispredictions = {num_mispredicts}")
        print(f"misprediction rate per 1000 instructions = {mispredict_rate}")

def get_prediction(dut):
    return 
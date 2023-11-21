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

    def say_hi(self):
        print("HELLO HELLO HELLO")

    # Return an object of type BranchRecord if there is still another branch
    # record left in the trace. Return false otherwise.
    def get_next_branch_record():
        pass

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
        pass

def get_prediction(dut):
    return 

def calculate_misprediction_rate(
    num_branchs,
    num_correct_predicts,
    num_instructions
    ):

    # calculate misprediction rate
    num_mispredictions = num_branchs - num_correct_predicts
    misprediction_rate = (num_mispredictions / num_instructions) / 1000

    # print out the statistics
    print(f"number of branches = {num_branches}")
    print(f"number of correct predictions = {num_correct_predicts}")
    print(f"number of instructions = {num_instructions}")
    print(f"number of mispredictions = {num_mispredictions}")
    print(f"misprediction rate per 1000 instructions = {misprediction_rate}")
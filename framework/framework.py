# my idea is that each branch predictor will have their own testbench.py that
# drives the verilog, but we will have a single framework.py that provides
# predictor-agnostic functionality. all the different cocotb testbenches will
# use the functionality that we implement in framework.py

class Framework:
    def get_prediction(self):
        pass
    def update_predictor(self):
        pass
    
    # we want to give the misprediction rate per 1000 instructions
    def calculate_misprediction_rate(self):
        pass

def get_prediction(dut):
    return 

def calculate_misprediction_rate(num_branchs, num_correct_predicts, num_instructions):

    # calculate misprediction rate
    num_mispredictions = num_branchs - num_correct_predicts
    misprediction_rate = (num_mispredictions / num_instructions) / 1000

    # print out the statistics
    print(f"number of branches = {num_branches}")
    print(f"number of correct predictions = {num_correct_predicts}")
    print(f"number of instructions = {num_instructions}")
    print(f"number of mispredictions = {num_mispredictions}")
    print(f"misprediction rate per 1000 instructions = {misprediction_rate}")
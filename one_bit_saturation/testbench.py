import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

# Ugly hack to import a sibling package
# https://stackoverflow.com/questions/6323860/sibling-package-imports
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from framework.framework import Evaluator

@cocotb.test()
async def one_bit_saturation(dut):

    # create an instance of our evaluator
    evaluator = Evaluator()

    # TODO We want to be able to specify which trace here.
    #evaluator.load_trace("../traces/trace_10")
    evaluator.load_riscv_trace("dhrystone")

    # generate a clock with a 10 ns period
    cocotb.start_soon(Clock(dut.clk, 10, 'ns').start())

    # reset the module and wait 2 rising edges before we release the reset
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0

    dut.counter.value = 1
    dut.branch_taken.value = 0

    # Get the next branch record from the trace (if there is one left.)
    next_branch = evaluator.get_next_branch_record()
    #while (next_branch):
    for i in range(1000):
        await RisingEdge(dut.clk)
        print(f"instruction pc: {next_branch.pc}")

        print(f"state: {dut.counter_reg.value}")
        print(f"prediction: {dut.predict.value}")

        # Report our current prediction and get the actual result.
        if (evaluator.predict_branch(dut.predict.value)):
            print("Yay! Correctly predicted")
            dut.branch_taken.value = dut.predict.value
        else:
            print("Aw :( Incorrectly predicted")
            dut.branch_taken.value = not dut.predict.value

        # Get the next branch
        next_branch = evaluator.get_next_branch_record()
    
    # get misprediction statistics
    evaluator.calculate_misprediction_rate()
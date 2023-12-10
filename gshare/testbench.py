# Testbench for the gshare branch predictor.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

# Ugly hack to import a sibling package
# https://stackoverflow.com/questions/6323860/sibling-package-imports
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from framework.framework import Evaluator

@cocotb.test()
async def gshare(dut):

    # Create an instance of our evaluator.
    evaluator = Evaluator()
    evaluator.load_trace("../traces/trace_01")

    # generate a clock with a 10 ns period
    cocotb.start_soon(Clock(dut.clk, 10, 'ns').start())

    # reset the module and wait 2 rising edges before we release the reset
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0

    # Get the first branch record from the trace.
    next_branch = evaluator.get_next_branch_record()

    # Run our evaluation loop 10 times for now.
    for i in range(10):
        await RisingEdge(dut.clk)

        print(f"instruction pc: {next_branch.pc}")

        # Tell gshare what the PC of the next branch is. We strip the "0x" from
        # the string and convert it to a binary buffer of bytes.
        dut.pc.value.buff = bytes.fromhex(next_branch.pc[2:])

        print(f"prediction: {dut.predict.value}")
        print(f"type(dut.predict.value)={type(dut.predict.value)}")

        # Report our current prediction and get the actual result.
        if (evaluator.predict_branch(dut.predict.value)):
            print("Yay! Correctly predicted")
            dut.taken.value = dut.predict.value
        else:
            print("Aw :( Incorrectly predicted")
            dut.taken.value = not dut.predict.value

        # Get the next branch
        next_branch = evaluator.get_next_branch_record()
    
    # get misprediction statistics
    evaluator.calculate_misprediction_rate()
import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

# Ugly hack
# https://stackoverflow.com/questions/6323860/sibling-package-imports
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from framework.framework import Framework

@cocotb.test()
async def one_bit_saturation(dut):

    # print out top-level info
    #print(dir(dut))

    f = Framework()
    f.say_hi()
    print("HI HI HI")

    # generate a clock with a 10 ns period
    cocotb.start_soon(Clock(dut.clk, 10, 'ns').start())

    # reset the module and wait 2 rising edges before we release the reset
    dut.rst.value = 1
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.rst.value = 0

    # run for 100 ns, generating random inputs for now
    # TODO why is this sometimes printing out 'z' ???
    for count in range(10):
        await RisingEdge(dut.clk)
        dut.branch_taken.value = random.randint(0, 1)
        dut.counter.value = random.randint(0, 1)
        print(f"state: {dut.counter_reg.value}")
        print(f"prediction: {dut.predict.value}")
    
    # TODO how do we generate misprediction %?
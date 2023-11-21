import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def gshare(dut):

    # print out top-level info
    #print(dir(dut))

    # generate a clock with a 10 ns period
    cocotb.start_soon(Clock(dut.clock, 10, 'ns').start())

    # reset the module and wait 2 rising edges before we release the reset
    dut.reset.value = 1
    for _ in range(2):
        await RisingEdge(dut.clock)
    dut.reset.value = 0
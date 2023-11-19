import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def one_bit_saturation(dut):

    # print out top-level info
    #print(dir(dut))

    # generate a clock with a 10 ns period
    cocotb.start_soon(Clock(dut.clk, 10, 'ns').start())
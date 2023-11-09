import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def basic_count(dut):

    # generate a clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())

    # reset dut
    dut.reset.value = 1

    # reset the module
    # wait 2 rising edges until we release reset
    for _ in range(2):
        await RisingEdge(dut.clk)
    dut.reset.value = 0

    # run for 50ns checking count on each rising edge
    for count in range(50):
        await RisingEdge(dut.clk)
        v_count = dut.count.value
        mod_count = count % 16
        assert v_count.integer == mod_count, "counter result is incorrect: %s != %s" % (str(dut.count.value), mod_count)
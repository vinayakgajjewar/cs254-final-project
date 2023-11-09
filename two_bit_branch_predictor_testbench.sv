module test;

logic clock;
logic reset_in;
logic action_in;
logic valid_in;
logic branch_out;

initial begin
    $dumpfile("dump.vcd");
    $dumpvars;
end

two_bit_branch_predictor DUT(
    clock,
    reset_in,
    valid_in,
    action_in,
    branch_out
);

initial begin
    clock = 0;
    reset_in = 0;
    valid_in = 0;
    action_in = 0;
    @(negedge clock) reset_in = 1;
    valid_in = 1;
    action_in = 0;
    @(negedge clock) valid_in = 1; action_in = 0;
end
endmodule
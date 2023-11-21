module one_bit_saturation (
    input wire clk,          // Clock input
    input wire rst,          // Reset input
    input wire branch_taken,
    input wire counter,       // 1-bit counter
    output reg predict
);

    // Saturation counter states
    parameter NOT_TAKEN = 1'b0;
    parameter TAKEN = 1'b1;

    // Internal counter register
    reg counter_reg;

    // Synchronous reset
    always @(posedge clk or posedge rst) begin
        if (rst)
            counter_reg <= NOT_TAKEN;
        else
            counter_reg <= counter;
    end

    // Update counter based on branch outcome
    always @(posedge clk) begin
        if (branch_taken) begin
            if (counter_reg == NOT_TAKEN)
                counter_reg <= TAKEN;
        end else begin
            if (counter_reg == TAKEN)
                counter_reg <= NOT_TAKEN;
        end
    end

    // Predict branch outcome based on counter
    always @* begin
        predict = counter_reg;
    end

endmodule

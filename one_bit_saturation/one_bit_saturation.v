module one_bit_saturation (
    input wire clk,          // Clock input
    input wire rst,          // Reset input
    input wire branch_taken,
    input wire [1:0] counter,
    output reg predict
);

    // Saturation counter states
    parameter IDLE = 2'b00;
    parameter WEAKLY_NOT_TAKEN = 2'b01;
    parameter WEAKLY_TAKEN = 2'b10;
    parameter STRONGLY_TAKEN = 2'b11;

    // Internal counter register
    reg [1:0] counter_reg;

    // Synchronous reset
    always @(posedge clk or posedge rst) begin
        if (rst)
            counter_reg <= IDLE;
        else
            counter_reg <= counter;
    end

    // Update counter based on branch outcome
    always @(posedge clk) begin
        if (branch_taken) begin
            case (counter_reg)
                IDLE: counter_reg <= WEAKLY_NOT_TAKEN;
                WEAKLY_NOT_TAKEN: counter_reg <= WEAKLY_TAKEN;
                WEAKLY_TAKEN: counter_reg <= STRONGLY_TAKEN;
                STRONGLY_TAKEN: counter_reg <= STRONGLY_TAKEN;
            endcase
        end
    end

    // Predict branch outcome based on counter
    always @* begin
        case (counter_reg)
            IDLE, WEAKLY_NOT_TAKEN: predict = 1'b0;
            WEAKLY_TAKEN, STRONGLY_TAKEN: predict = 1'b1;
        endcase
    end

endmodule

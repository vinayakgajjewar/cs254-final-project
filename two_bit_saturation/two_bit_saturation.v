module two_bit_saturation_module (
    input wire clk,
    input wire reset,
    input wire branch_history,
    output reg branch_prediction
);

    // 2-bit saturating counter
    reg [1:0] counter;

    // Always block for clocked behavior
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            // Reset the counter to a neutral state
            counter <= 2'b01; // Weakly taken
        end else begin
            // Update the counter based on the branch history
            if (branch_history) begin
                // Branch taken
                if (counter < 2'b11) begin
                    // Increment the counter if it's not saturated
                    counter <= counter + 1;
                end
            end else begin
                // Branch not taken
                if (counter > 2'b00) begin
                    // Decrement the counter if it's not saturated
                    counter <= counter - 1;
                end
            end
        end
    end

    // Output the branch prediction
    assign branch_prediction = (counter == 2'b11) || (counter == 2'b10);

endmodule

module static_always_taken (
  input wire clk,      // Clock input
  input wire rst,      // Reset input
  output reg branch_prediction
);

// Register to store the branch prediction
reg branch_prediction_reg;

// Always predict the branch as taken
always @(posedge clk or posedge rst) begin
  if (rst) begin
    // Reset the predictor on a positive edge of the reset signal
    branch_prediction_reg <= 1'b1;
  end else begin
    // Update the branch prediction on the positive edge of the clock
    branch_prediction_reg <= 1'b1;
  end
end

// Output the branch prediction
assign branch_prediction = branch_prediction_reg;

endmodule
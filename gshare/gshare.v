module gshare (
  input wire clk,      // Clock input
  input wire rst,      // Reset input
  input wire [31:0] pc, // Program counter input
  input wire taken,    // Branch taken input
  output reg predict   // Branch prediction output
);

  // Parameters
  parameter integer history_bits = 8; // Number of history bits
  parameter integer table_size = 256; // Size of the pattern history table (PHT)

  // Internal registers and wires
  reg [history_bits-1:0] history;         // Global history register
  reg [table_size-1:0] pattern_history;   // Pattern history table
  wire [7:0] index;                       // Index into the pattern history table

  // Update the global history and pattern history table on each clock edge
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      // Reset the predictor
      history <= 0;
      pattern_history <= 0;
    end else begin
      // Update the global history and pattern history table
      history <= {history[history_bits-2:0], taken};
      pattern_history[index] <= taken;
    end
  end

  // Compute the index into the pattern history table
  assign index = pc ^ history;

  // Make a prediction based on the pattern history table
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      // Reset prediction to not taken during reset
      predict <= 0;
    end else begin
      // Make a prediction based on the pattern history table
      predict <= pattern_history[index] >= 4;
    end
  end

endmodule

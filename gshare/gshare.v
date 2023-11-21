module gshare (
    input wire clock,
    input wire reset,
  input wire [31:0] pc,          // Program Counter
  input wire branch,             // Branch instruction
  input wire actual_outcome,      // Actual outcome of the branch (1 for taken, 0 for not taken)
  output reg predicted_outcome    // Predicted outcome (1 for taken, 0 for not taken)
);

  parameter TABLE_SIZE = 1024;    // Size of the GShare table
  parameter HISTORY_BITS = 10;    // Number of bits for the global history register

  reg [HISTORY_BITS-1:0] global_history;   // Global history register
  reg [TABLE_SIZE-1:0] gshare_table;      // GShare table

  // Function to compute the index into the GShare table
  function [TABLE_SIZE-1:0] compute_index;
    input [31:0] pc;
    input [HISTORY_BITS-1:0] history;
    begin
      // XOR the PC with the global history to get the index
      compute_index = (pc ^ history) % TABLE_SIZE;
    end
  endfunction

  // Function to update the GShare predictor table
  function void update_table;
    input [31:0] pc;
    input [HISTORY_BITS-1:0] history;
    input actual_outcome;
    begin
      // Compute the index into the table
      reg [TABLE_SIZE-1:0] index;
      index = compute_index(pc, history);

      // Update the predictor table based on the actual outcome
      if (actual_outcome == 1 && gshare_table[index] < 3)
        gshare_table[index] = gshare_table[index] + 1;
      else if (actual_outcome == 0 && gshare_table[index] > 0)
        gshare_table[index] = gshare_table[index] - 1;
    end
  endfunction

  // Function to predict the outcome of a branch
  function void predict_outcome;
    input [31:0] pc;
    input [HISTORY_BITS-1:0] history;
    begin
      // Compute the index into the table
      reg [TABLE_SIZE-1:0] index;
      index = compute_index(pc, history);

      // Make the prediction based on the counter value
      if (gshare_table[index] >= 2)
        predicted_outcome = 1;
      else
        predicted_outcome = 0;
    end
  endfunction

  // Initial values
  initial begin
    global_history = 0;
    gshare_table = 2'b01;
    predicted_outcome = 0;
  end

  // Always block to perform prediction and update
  always @(posedge clock or posedge reset) begin
    if (reset) begin
      // Reset the predictor state
      global_history <= 0;
      gshare_table <= 2'b01;
      predicted_outcome <= 0;
    end else begin
      // Shift in the current branch outcome into the global history register
      global_history <= {global_history[HISTORY_BITS-2:0], branch};

      // Predict the outcome based on the current state
      predict_outcome(pc, global_history);

      // Update the table based on the actual outcome
      update_table(pc, global_history, actual_outcome);
    end
  end

endmodule

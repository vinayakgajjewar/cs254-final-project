// adapted from:
// https://github.com/jjhemphill/CS254_Final/blob/one_bit_saturation/piton/design/chip/tile/ariane/src/frontend/bht.sv

/*
1-bit Branch-Prediction Buffer: In this case, the Branch History Table (BHT) or
Branch Prediction Buffer stores 1-bit values to indicate whether the branch is
predicted to be taken / not taken. The lower bits of the PC address index this
table of 1-bit values and get the prediction. This says whether the branch was
recently taken or not. Based on this, the processor fetches the next instruction
from the target address / sequential address. If the prediction is wrong, flush
the pipeline and also flip prediction. So, every time a wrong prediction is made,
the prediction bit is flipped. Usage of only some of the address bits may give us
prediction about a wrong branch. But, the best option is to use only some of the
least significant bits of the PC address.
*/

// https://www.cs.umd.edu/~meesh/411/CA-online/chapter/dynamic-branch-prediction/index.html

// branch history table - 1 bit saturation counter
module bht #(
    parameter int unsigned NR_ENTRIES = 1
)(
    input  logic                        clk_i,
    input  logic                        rst_ni,
    input  logic                        flush_i,
    input  logic                        debug_mode_i,
    input  logic [riscv::VLEN-1:0]      vpc_i,          // throwing syntax error here, also wtf is this?
    input  ariane_pkg::bht_update_t     bht_update_i,
    // we potentially need INSTR_PER_FETCH predictions/cycle
    output ariane_pkg::bht_prediction_t [ariane_pkg::INSTR_PER_FETCH-1:0] bht_prediction_o
);
    // the last bit is always zero, we don't need it for indexing
    localparam OFFSET = 1;
    // re-shape the branch history table
    localparam NR_ROWS = NR_ENTRIES / ariane_pkg::INSTR_PER_FETCH;
    // number of bits needed to index the row
    localparam ROW_ADDR_BITS = $clog2(ariane_pkg::INSTR_PER_FETCH);
    // number of bits we should use for prediction
    localparam PREDICTION_BITS = $clog2(NR_ROWS) + OFFSET + ROW_ADDR_BITS;
    // we are not interested in all bits of the address
    unread i_unread (.d_i(|vpc_i));

    struct packed {
        logic       valid;
        logic       saturation_counter;
    } bht_d[NR_ROWS-1:0][ariane_pkg::INSTR_PER_FETCH-1:0], bht_q[NR_ROWS-1:0][ariane_pkg::INSTR_PER_FETCH-1:0];

    logic [$clog2(NR_ROWS)-1:0]  index, update_pc;
    logic [ROW_ADDR_BITS-1:0]    update_row_index;
    logic                        saturation_counter;

    assign index     = vpc_i[PREDICTION_BITS - 1:ROW_ADDR_BITS + OFFSET];
    assign update_pc = bht_update_i.pc[PREDICTION_BITS - 1:ROW_ADDR_BITS + OFFSET];
    assign update_row_index = bht_update_i.pc[ROW_ADDR_BITS + OFFSET - 1:OFFSET];

    // prediction assignment
    for (genvar i = 0; i < ariane_pkg::INSTR_PER_FETCH; i++) begin : gen_bht_output
        assign bht_prediction_o[i].valid = bht_q[index][i].valid;
        assign bht_prediction_o[i].taken = bht_q[index][i].saturation_counter;
    end

    always_comb begin : update_bht
        bht_d = bht_q;
        saturation_counter = bht_q[update_pc][update_row_index].saturation_counter;

        if (bht_update_i.valid && !debug_mode_i) begin
            bht_d[update_pc][update_row_index].valid = 1'b1;

            bht_q[update_pc][update_row_index].saturation_counter = bht_update_i.taken;

        end
    end

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (!rst_ni) begin
            for (int unsigned i = 0; i < NR_ROWS; i++) begin
                for (int j = 0; j < ariane_pkg::INSTR_PER_FETCH; j++) begin
                    bht_q[i][j].valid <= 1'b0;
                    bht_q[i][j].saturation_counter <= 1'b0;
                end
            end
        end else begin
            // evict all entries
            if (flush_i) begin
                for (int i = 0; i < NR_ROWS; i++) begin
                    for (int j = 0; j < ariane_pkg::INSTR_PER_FETCH; j++) begin
                        bht_q[i][j].valid <=  1'b0;
                        // init to all taken
                        bht_q[i][j].saturation_counter <= 1'b0;
                    end
                end
            end else begin
                bht_q <= bht_d;
            end
        end
    end
endmodule
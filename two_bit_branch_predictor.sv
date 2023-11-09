module two_bit_branch_predictor(
    input logic clock,
    input logic reset_in,
    input logic valid_in,
    input logic action_in,
    output logic branch_out
);

typedef enum logic[1:0] {
    TAKEN=2'b00,
    WEAK_TAKEN=2'b01,
    NOT_TAKEN=2'b11,
    WEAK_NOT_TAKEN=2'b10
} state;

state p_state;
state next_state;

assign branch_out = (p_state == TAKEN) || (p_state == WEAK_TAKEN);

always_ff@(posedge clock, negedge reset_in) begin
    if (!reset_in) begin
        p_state <= TAKEN;
    end
    else begin
        p_state <= n_state;
    end
end

always_comb begin
    next_state = TAKEN;
    if (valid_in) begin
        case (p_state)

        TAKEN: begin
            if (action_in) begin
                next_state = TAKEN;
            end
            else next_state = WEAK_TAKEN;
        end

        WEAK_TAKEN: begin
            if (action_in) next_state = TAKEN;
            else next_state = WEAK_NOT_TAKEN;
        end

        NOT_TAKEN: begin
            if (action_in) next_state = WEAK_NOT_TAKEN;
            else next_state = NOT_TAKEN;
        end

        WEAK_NOT_TAKEN: begin
            if (action_in) next_state = WEAK_TAKEN;
            else next_state = NOT_TAKEN;
        end

        default: next_state = TAKEN;
        endcase
    end
    else next_state = p_stage;
end
endmodule
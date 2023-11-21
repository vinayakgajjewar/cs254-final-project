# this file defines a class BranchRecord which basically acts as a struct that
# holds the information for a single branch in a trace

class BranchRecord:

    # true if the branch is indirect, false otherwise
    in_indirect = False

    # true if the branch is a conditional, false otherwise
    is_conditional = False

    # true if the branch is a call, false otherwise
    is_call = False

    # true if the branch is a return, false otherwise
    is_return = False

    # the value of the branch's PC (program counter)
    instruction_address = 0x0

    # the target of the branch if it's taken; branches that aren't conditionals
    # are always taken.
    branch_target = 0x0

    # the PC of the instruction following the branch
    next_address = 0x0

    def __init__(self):
        pass
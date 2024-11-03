from enum import Enum


class Instruction(Enum):
    NO_INSTRUCTION_TYPE = 0,
    GOTO = 1,              # branch, possibly guarded
    ASSUME = 2,            # non-failing guarded self loop
    ASSERT = 3,            # assertions
    OTHER = 4,             # anything else
    SKIP = 5,              # just advance the PC
    START_THREAD = 6,      # spawns an asynchronous thread
    END_THREAD = 7,        # end the current thread
    LOCATION = 8,          # semantically like SKIP
    END_FUNCTION = 9,      # exit point of a function
    ATOMIC_BEGIN = 10,     # marks a block without interleavings
    ATOMIC_END = 11,       # end of a block without interleavings
    SET_RETURN_VALUE = 12, # set function return value (no control-flow change)
    ASSIGN = 13,           # assignment lhs:=rhs
    DECL = 14,             # declare a local variable
    DEAD = 15,             # marks the end-of-live of a local variable
    FUNCTION_CALL = 16,    # call a function
    THROW = 17,            # throw an exception
    CATCH = 18,            # push, pop or enter an exception handler
    INCOMPLETE_GOTO = 19   # goto where target is yet to be determined

    def is_guarded(self) -> bool:
        return self.name in {'GOTO', 'ASSUME', 'ASSERT', 'END_FUNCTION'}


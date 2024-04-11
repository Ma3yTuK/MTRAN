from enum import IntEnum, auto
from ..lexic.identifiers_and_types import INT_SIZE
from struct import pack



code = bytes()
var_stack = bytes()
operands_stack = bytes()


class Commands(IntEnum):

# binary commands
    SUM = auto()
    SUMF = auto()
    SUB = auto()
    SUBF = auto()
    MUL = auto()
    MULF = auto()
    DIV = auto()
    DIVF = auto()
    PERC = auto()
    PERCF = auto()
    EQ = auto()
    NQ = auto()
    GE = auto()
    GEF = auto()
    LE = auto()
    LEF = auto()
    GT = auto()
    GTF = auto()
    LT = auto()
    LTF = auto()
    AND = auto()
    OR = auto()
    ASS = auto()
    REF = auto()

# unary commands
    DEREF = auto()
    NEG = auto()
    NEGF = auto()
    NOT = auto()
    TOI = auto()
    TOF = auto()
    RMS = auto()

# other commands
    LD = auto()
    PUSH = auto()
    POP = auto()
    ULD = auto()

# jumps
    CALL = auto()
    JMP = auto()
    JMPIF = auto()

    RET = auto()

    SUBV = auto()

    PRINTI = auto()
    PRINTF = auto()
    PRINTS = auto()



def gen_prefix(value_size, is_addressable):
    result = bytes()

    if value_type is None:
        return result

    value_size = value_type.size
    
    if is_addressable:
        current_byte = 128
    else:
        current_byte = 0

    if value_size > 126:
        current_byte += 127
        value_size -= 127
        result += pack('!B', current_byte)

        while value_size > 254:
            result += pack('!B', 255)
            value_size -= 255

        current_byte = 0
    
    current_byte += value_size
    result += pack('!B', current_byte)

    return result

def add_command(command):
    code += pack('!B', command)

def add_literal(value, value_type):
    code += gen_prefix(value_type.size, True) + value

def add_reference(reference, value_type):
    code += gen_prefix(value_type.size, False) + pack('!i', reference)

def ld(byte_string, index):
    current_index = index
    size = 0

    if byte_string[current_index] == 127 or byte_string[current_index] == 255:
        size += 127
        current_index += 1
        
        while byte_string[current_index] == 255:
            size += 255
            current_index += 1
        
        size += byte_string[current_index]
    
    current_index += 1

    if byte_string[index] > 127:
        result = current_index + INT_SIZE
    else:
        result = current_index + size
    
    byte_string[current_index : result]
    operands_stack += reversed(byte_string[index : current_index])

    return result

def rms():
    current_index = -1

    if operands_stack[current_index] == 127 or operands_stack[current_index] == 255:
        current_index -= 1
        
        while operands_stack[current_index] == 255:
            current_index -= 1

    operands_stack = operands_stack[: current_index]

def uld():
    current_index = -1
    size = 0

    if operands_stack[current_index] == 127 or operands_stack[current_index] == 255:
        size += 127
        current_index -= 1
        
        while operands_stack[current_index] == 255:
            size += 255
            current_index -= 1
        
        size += operands_stack[current_index]
    
    current_index -= 1

    result_prefix = operands_stack[current_index + 1 :]
    
    if operands_stack[-1] > 127:
        result = operands_stack[current_index - INT_SIZE + 1 : current_index + 1]
        operands_stack = operands_stack[: current_index - INT_SIZE + 1]
    else:
        result = operands_stack[current_index - size + 1 : current_index + 1]
        operands_stack = operands_stack[: current_index - size + 1]

    return result_prefix, result

def get_value(prefix, ptr):
    size = prefix[-1]

    if len(prefix) > 1:
        size += (len(prefix) - 2) * 255 + 127

    return var_stack[ptr : ptr + size]

def push(value):
    var_stack += value

def pop(size):
    var_stack = var_stack[: -size]

def assign(shift, value):

    for index, byte in enumerate(value):
        var_stack[shift + index] = byte
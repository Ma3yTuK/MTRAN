from enum import IntEnum, auto
from ..lexic.identifiers_and_types import INT_SIZE, identifier_tables, TypeName
from struct import pack
from .runtime_exception import RuntimeException



code = bytearray()
global_code = bytearray()
var_stack = bytearray()
operands_stack = bytearray()


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
    LDP = auto()
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


def set_code(new_code):
    global code
    code = new_code


def get_code():
    return code


def switch_global():
    global code
    global global_code
    tmp = code
    code = global_code
    global_code = tmp


def unswitch_global():
    global code
    global global_code
    tmp = global_code
    global_code = code
    code = tmp


def apply_global():
    global code
    global global_code
    code = code + global_code


def gen_prefix(value_size, is_addressable):
    result = bytes()

    if value_size is None:
        return result
    
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
    global code
    code += pack('!B', command)

def add_literal(value, value_type):
    global code
    
    if value_type is None:
        value_size = None
    else:
        value_size = value_type.size

    code += gen_prefix(value_size, False) + value

def add_reference(reference, value_type):
    global code
    code += gen_prefix(value_type.size, True) + pack('!i', reference)

def ld(byte_string, index):
    global operands_stack

    current_index = index
    size = 0

    if byte_string[current_index] == 127 or byte_string[current_index] == 255:
        size += 127
        current_index += 1
        
        while byte_string[current_index] == 255:
            size += 255
            current_index += 1
        
        size += byte_string[current_index]
    else:
        size += byte_string[index]
    
    current_index += 1

    if byte_string[index] > 127:
        result = current_index + INT_SIZE
        ptr = identifier_tables[0][TypeName.T_INT].to_python(byte_string[current_index : result])

        if ptr < 0:
            ptr = len(var_stack) + ptr
        
        ptr = identifier_tables[0][TypeName.T_INT].from_python(ptr)
    else:
        result = current_index + size
        ptr = byte_string[current_index : result]
    
    operands_stack += bytearray(reversed(byte_string[index : current_index] + ptr))

    return result

def ldp(byte_string, index):
    global operands_stack
    
    current_index = index

    if byte_string[current_index] == 127 or byte_string[current_index] == 255:
        current_index += 1
        
        while byte_string[current_index] == 255:
            current_index += 1
    
    current_index += 1
    
    operands_stack += bytearray(reversed(byte_string[index : current_index]))

    return current_index

def rms():
    global operands_stack

    current_index = -1

    if operands_stack[current_index] == 127 or operands_stack[current_index] == 255:
        current_index -= 1
        
        while operands_stack[current_index] == 255:
            current_index -= 1

    operands_stack = operands_stack[: current_index]

def uld():
    global operands_stack

    current_index = -1
    size = 0

    if operands_stack[current_index] == 127 or operands_stack[current_index] == 255:
        size += operands_stack[current_index]
        current_index -= 1
        
        while operands_stack[current_index] == 255:
            size += 255
            current_index -= 1
        
    size += operands_stack[current_index]

    if operands_stack[-1] > 127:
        size -= 128
    
    current_index -= 1

    result_prefix = operands_stack[current_index + 1 :]
    
    if operands_stack[-1] > 127:
        result = operands_stack[current_index - INT_SIZE + 1 : current_index + 1]
        operands_stack = operands_stack[: current_index - INT_SIZE + 1]
    else:
        result = operands_stack[current_index - size + 1 : current_index + 1]
        operands_stack = operands_stack[: current_index - size + 1]

    return bytearray(reversed(result_prefix)), bytearray(reversed(result))

def get_value(prefix, ptr):
    global var_stack
    
    if len(prefix) > 1:
        size = (len(prefix) - 2) * 255 + 127 + prefix[-1]
    else:
        size = prefix[-1] - 128

    ptr = identifier_tables[0][TypeName.T_INT].to_python(ptr)

    end = ptr + size
    if end == 0:
        end = len(var_stack)

    return var_stack[ptr : end]

def push(value):
    global var_stack
    var_stack += value

def pop(size):
    global var_stack

    if size == 0:
        return

    var_stack = var_stack[: -size]

def assign(shift, value):
    global var_stack

    shift = identifier_tables[0][TypeName.T_INT].to_python(shift)

    for index, byte in enumerate(value):
        var_stack[shift + index] = byte



call_stack = []


def execute():
    index = 0

    while index != len(code):

        match code[index]:

            case Commands.SUM: 
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result1) + identifier_tables[0][TypeName.T_INT].to_python(result2))
                ld(prefix + result, 0)

                index += 1
            
            case Commands.SUMF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result1) + identifier_tables[0][TypeName.T_FLOAT32].to_python(result2))
                ld(prefix + result, 0)

                index += 1

            case Commands.SUB:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) - identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.SUBF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) - identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(prefix + result, 0)

                index += 1
            
            case Commands.MUL:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) * identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.MULF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result1) * identifier_tables[0][TypeName.T_FLOAT32].to_python(result2))
                ld(prefix + result, 0)

                index += 1

            case Commands.DIV:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) / identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.DIVF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) / identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.PERC:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) % identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(prefix + result, 0)

                index += 1
            
            case Commands.PERCF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) % identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.EQ:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(result1 == result2)
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.NQ:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(result1 != result2)
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.GE:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) >= identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.GEF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) >= identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.LE:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) <= identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.LEF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) <= identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.GT:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) > identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.GTF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) > identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.LT:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) < identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.LTF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) < identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.T_BOOL].size, False) + result, 0)

                index += 1

            case Commands.AND:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_BOOL].to_python(result2) and identifier_tables[0][TypeName.T_BOOL].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.OR:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_BOOL].from_python(identifier_tables[0][TypeName.T_BOOL].to_python(result2) or identifier_tables[0][TypeName.T_BOOL].to_python(result1))
                ld(prefix + result, 0)

                index += 1

            case Commands.ASS:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                assign(result2, result1)
                
                index += 1

            case Commands.REF:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                index += 1

                prefix = gen_prefix(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]), True)
                ld(prefix + result, 0)

                index += INT_SIZE

            case Commands.DEREF:
                prefix, result = uld()
                ld(gen_prefix(INT_SIZE, False) + result, 0)

                index += 1

            case Commands.NEG:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(- identifier_tables[0][TypeName.T_INT].to_python(result))
                ld(prefix + result, 0)

                index += 1

            case Commands.NEGF:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(- identifier_tables[0][TypeName.T_FLOAT32].to_python(result))
                ld(prefix + result, 0)

                index += 1

            case Commands.NOT:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_BOOL].from_python(not identifier_tables[0][TypeName.T_BOOL].to_python(result))
                ld(prefix + result, 0)

                index += 1

            case Commands.TOI:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_INT].from_python(int(identifier_tables[0][TypeName.T_FLOAT32].to_python(result)))
                ld(prefix + result, 0)

                index += 1

            case Commands.TOF:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.T_FLOAT32].from_python(float(identifier_tables[0][TypeName.T_INT].to_python(result)))
                ld(prefix + result, 0)

                index += 1

            case Commands.RMS:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                    prefix[0] -= 128

                ld(prefix + result, 0)
                rms()

                index += 1

            case Commands.LD:
                index += 1
                index = ld(code, index)

            case Commands.LDP:
                index += 1
                index = ldp(code, index)

            case Commands.PUSH:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                push(result)

                index += 1

            case Commands.POP:
                index += 1
                pop(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]))
                
                index += INT_SIZE

            case Commands.ULD:
                uld()

                index += 1

            case Commands.CALL:

                if (len(call_stack) > 10000):
                    raise RuntimeException("Stack overflow")

                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                call_stack.append(index + 1)
                index = identifier_tables[0][TypeName.T_INT].to_python(result)

            case Commands.JMP:
                index += 1
                index = identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE])

            case Commands.JMPIF:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)
                
                index += 1

                if identifier_tables[0][TypeName.T_BOOL].to_python(result):
                    index = identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE])
                else:
                    index += INT_SIZE

            case Commands.RET:
                index = call_stack.pop()

            case Commands.SUBV:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)
                    
                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                prefix, result3 = uld()

                if prefix[0] > 127:
                    assignable = True
                    prefix[0] -= 128
                else:
                    assignable = False

                result_size = identifier_tables[0][TypeName.T_INT].to_python(result1)
                shift = identifier_tables[0][TypeName.T_INT].to_python(result2)
                result_prefix = gen_prefix(result_size, assignable)

                if len(prefix) > 1:
                    size = (len(prefix) - 2) * 255 + 127 + prefix[-1]
                else:
                    size = prefix[-1]

                shift = size - result_size - shift
                if shift < 0 or shift + result_size > size:
                    raise RuntimeException("Index out of range!")

                if assignable:
                    ld(result_prefix + identifier_tables[0][TypeName.T_INT].from_python(identifier_tables[0][TypeName.T_INT].to_python(result3) + shift), 0)
                else:
                    ld(result_prefix + result3[shift : shift + result_size], 0)

                index += 1

            case Commands.PRINTI:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                print(identifier_tables[0][TypeName.T_INT].to_python(result))
                
                index += 1

            case Commands.PRINTF:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                print(identifier_tables[0][TypeName.T_FLOAT32].to_python(result))
                
                index += 1

            case Commands.PRINTS:
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                print(identifier_tables[0][TypeName.T_STRING].to_python(result))
                
                index += 1

def debug():
    index = 0

    while index != len(code):

        match code[index]:

            case Commands.SUM: 
                print('sum')
                index += 1
            
            case Commands.SUMF:
                print('sumf')
                index += 1

            case Commands.SUB:
                print('sub')
                index += 1

            case Commands.SUBF:
                print('subf')
                index += 1
            
            case Commands.MUL:
                print('mul')
                index += 1

            case Commands.MULF:
                print('mulf')
                index += 1

            case Commands.DIV:
                print('div')
                index += 1

            case Commands.DIVF:
                print('divf')
                index += 1

            case Commands.PERC:
                print('perc')
                index += 1
            
            case Commands.PERCF:
                print('percf')
                index += 1

            case Commands.EQ:
                print('eq')
                index += 1

            case Commands.NQ:
                print('nq')
                index += 1

            case Commands.GE:
                print('ge')
                index += 1

            case Commands.GEF:
                print('gef')
                index += 1

            case Commands.LE:
                print('le')
                index += 1

            case Commands.LEF:
                print('lef')
                index += 1

            case Commands.GT:
                print('gt')
                index += 1

            case Commands.GTF:
                print('gtf')
                index += 1

            case Commands.LT:
                print('lt')
                index += 1

            case Commands.LTF:
                print('ltf')
                index += 1

            case Commands.AND:
                print('and')
                index += 1

            case Commands.OR:
                print('or')
                index += 1

            case Commands.ASS:
                print('ass')
                index += 1

            case Commands.REF:
                print('ref')
                index += 1
                print(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]))
                index += INT_SIZE

            case Commands.DEREF:
                print('deref')
                index += 1

            case Commands.NEG:
                print('neg')
                index += 1

            case Commands.NEGF:
                print('negf')
                index += 1

            case Commands.NOT:
                print('not')
                index += 1

            case Commands.TOI:
                print('toi')
                index += 1

            case Commands.TOF:
                print('tof')
                index += 1

            case Commands.RMS:
                print('rms')
                index += 1

            case Commands.LD:
                print('ld')
                index += 1
                saved_index = index
                index = ld(code, index)
                print(list(code[saved_index : index]))
            
            case Commands.LDP:
                print('ld')
                index += 1
                saved_index = index
                index = ldp(code, index)
                print(list(code[saved_index : index]))

            case Commands.PUSH:
                print('push')
                index += 1

            case Commands.POP:
                print('pop')
                index += 1
                print(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]))
                index += INT_SIZE

            case Commands.ULD:
                print('uld')
                index += 1

            case Commands.CALL:
                print('call')
                index += 1

            case Commands.JMP:
                print('jmp')
                index += 1
                print(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]))
                index += INT_SIZE

            case Commands.JMPIF:
                print('jmpif')
                index += 1
                print(identifier_tables[0][TypeName.T_INT].to_python(code[index : index + INT_SIZE]))
                index += INT_SIZE

            case Commands.RET:
                print('ret')
                index += 1

            case Commands.SUBV:
                print('subv')
                index += 1

            case Commands.PRINTI:
                print('print')
                index += 1

            case Commands.PRINTF:
                print('print')
                index += 1

            case Commands.PRINTS:
                print('print')
                index += 1
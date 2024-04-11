from ..lexic.identifiers_and_types import INT_SIZE, identifier_tables, TypeName
from .runtime_exception import RuntimeException
from commands import code, push, pop, ld, uld, Commands, get_value, gen_prefix, assign, rms
from struct import pack



call_stack = []


def execute():
    index = len(code) - 3 - INT_SIZE

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
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

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
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.GE:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) >= identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.GEF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) >= identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.LE:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) <= identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.LEF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) <= identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.GT:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) > identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.GTF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) > identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.LT:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_INT].to_python(result2) < identifier_tables[0][TypeName.T_INT].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.LTF:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_FLOAT32].to_python(result2) < identifier_tables[0][TypeName.T_FLOAT32].to_python(result1))
                ld(gen_prefix(identifier_tables[0][TypeName.BOOL].size, False) + result, 0)

                index += 1

            case Commands.AND:
                prefix, result1 = uld()

                if prefix[0] > 127:
                    result1 = get_value(prefix, result1)

                prefix, result2 = uld()

                if prefix[0] > 127:
                    result2 = get_value(prefix, result2)
                    prefix[0] -= 128

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_BOOL].to_python(result2) and identifier_tables[0][TypeName.T_BOOL].to_python(result1))
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

                result = identifier_tables[0][TypeName.BOOL].from_python(identifier_tables[0][TypeName.T_BOOL].to_python(result2) or identifier_tables[0][TypeName.T_BOOL].to_python(result1))
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
                result = get_value(prefix, result)
                prefix[0] -= 128
                ld(prefix + result, 0)

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

                result = identifier_tables[0][TypeName.BOOL].from_python(not identifier_tables[0][TypeName.T_BOOL].to_python(result))
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
                rms()

                index += 1

            case Commands.LD:
                index += 1
                index = ld(code, index)

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
                prefix, result = uld()

                if prefix[0] > 127:
                    result = get_value(prefix, result)

                call_stack.append(index)
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
                    result3 = get_value(prefix, result3)
                    assignable = True
                else:
                    assignable = False

                result_size = identifier_tables[0][TypeName.T_INT].to_python(result1)
                shift = identifier_tables[0][TypeName.T_INT].to_python(result1)
                prefix = gen_prefix(result_size, assignable)
                ld(prefix + result3[shift : shift + result_size], 0)

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
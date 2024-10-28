from translator.lexic.lexical_generator import lexical_generator
from translator.lexic.tokens import token_table
from translator.syntaxis.syntax_analizer import syntax_analizer
from translator.vm.commands import code, switch_global, execute, debug, get_code, set_code
import sys



def main():
    # filepath = "test2.txt"
    # lexical_generator(filepath)
    # print(syntax_analizer())
    # return

    lexical_generator("test2.txt")
    syntax_analizer().gen_code()
    #execute()
    debug()

    return
    
    if len(sys.argv) > 4 or len(sys.argv) == 1 or len(sys.argv) == 3:
        raise Exception("Invalid number of arguments")

    if len(sys.argv) == 4:

        if sys.argv[1] != '-c':
            raise Exception("Invalid arguments")
        
        else:
            lexical_generator(sys.argv[2])
            syntax_analizer().gen_code()
            code = get_code()

            with open(sys.argv[3], "wb") as binary_file:
                binary_file.write(code)

            return

    with open(sys.argv[1], "rb") as binary_file:
        code = bytearray()
        
        while (byte := binary_file.read(1)):
            code += byte

        set_code(code)

    execute()
    
if __name__ == "__main__":
    main()
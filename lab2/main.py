from translator.lexic.lexical_generator import lexical_generator
from translator.lexic.tokens import token_table
from translator.syntaxis.syntax_analizer import syntax_analizer
from .translator.vm.commands import code
import sys



def main():
    # filepath = "test.txt"
    # lexical_generator(filepath)
    # print(syntax_analizer())
    # return
    
    if len(sys.argv > 3 or len(sys.argv == 0)):
        raise Exception("Invalid number of arguments")

    if len(sys.argv == 3):

        if argv[1] != '-c':
            raise Exception("Invalid arguments")
        
        else:
            lexical_generator(filepath)
            syntax_analizer().gen_code()

            with open(argv[2], "wb") as binary_file:
                binary_file.write(code)

            return

    with open(argv[1], "rb") as binary_file:

        while (byte := binary_file.read(1)):
            code += byte

if __name__ == "__main__":
    main()
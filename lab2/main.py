from translator.lexic.lexical_generator import lexical_generator
from translator.lexic.tokens import token_table
from translator.syntaxis.syntax_analizer import syntax_analizer

filepath = "test.txt"

def main():
    lexical_generator(filepath)
    print(syntax_analizer())

if __name__ == "__main__":
    main()
from lexical_generator import lexical_generator
from tokens import token_table

filepath = "test.txt"

def main():
    lexical_generator(filepath)
    for token in token_table:
        print(str(token.row) + ',' + str(token.col) + ': ' + token.name + ' ' + token.token_type)

if __name__ == "__main__":
    main()
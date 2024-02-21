from tokens import Token, TokenType, token_table
from identifiers import get_identifier
from keywords import is_keyword, KeywordName
from operators_punctuation import get_operator_or_punctuation, OperatorName, PunctuationName
from literals import add_literal
from characters import skip_blank


def lexical_generator(filepath):

    with open(filepath) as file:

        for (line_index, line) in enumerate(file):
            pos = 0

            while pos + 1 < len(line):

                try:
                    pos = skip_blank(line, pos)
                    tmp = get_identifier(line, pos)

                    if tmp != pos:
                        value = line[pos:tmp]
                        token_table.append(Token(value, TokenType.keyword if is_keyword(value) else TokenType.identifier, line_index, pos))

                    else:
                        tmp = get_operator_or_punctuation(line, pos)

                        if tmp != pos:
                            value = line[pos:tmp]
                            token_table.append(Token(value, TokenType.operator, line_index, pos))

                        else:
                            tmp = add_literal(line, pos)

                            if tmp != pos:
                                value = line[pos:tmp]
                                token_table.append(Token(value, TokenType.literal, line_index, pos))

                            else:
                                raise Exception(f"{pos}: Unsupported syntax")
                            

                    pos = tmp

                except Exception as e:
                    raise Exception(str(line_index) + ',' + str(e))
            
            if token_table[-1].token_type in {TokenType.identifier, TokenType.literal} or token_table[-1].name in {KeywordName.K_BREAK, KeywordName.K_CONTINUE, KeywordName.K_FALLTHROUGH, KeywordName.K_RETURN, OperatorName.O_INCREMENT, OperatorName.O_DECREMENT, PunctuationName.P_PARENTHESES_C, PunctuationName.P_BRACES_C, PunctuationName.P_BRACKETS_C}:
                token_table.append(Token(";", TokenType.operator, line_index, pos))
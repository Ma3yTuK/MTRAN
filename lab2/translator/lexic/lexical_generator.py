from .tokens import Token, TokenType, token_table
from .identifiers_and_types import get_identifier
from .keywords import is_keyword, KeywordName
from .operators_punctuation import get_operator_or_punctuation, OperatorName, PunctuationName
from .literals import add_literal
from .characters import skip_blank, character
from .comments import get_comment, CommentName


def lexical_generator(filepath):
    commented = False

    with open(filepath) as file:

        for (line_index, line) in enumerate(file):
            pos = skip_blank(line, 0)

            if line[pos] == character.newline:
                continue

            if line[-1] != character.newline:
                line += character.newline

            while pos + 1 < len(line):
                
                if commented:
                    tmp = get_comment(line, pos)

                    if tmp != pos and line[pos:tmp] == CommentName.C_MULTILINE_END:
                        commented = False
                        pos = tmp
                    else:
                        pos += 1

                    continue

                try:
                    tmp = get_comment(line, pos)

                    if tmp != pos and line[pos:tmp] != CommentName.C_MULTILINE_END:
                        value = line[pos:tmp]

                        if value == CommentName.C_MULTILINE_START:
                            commented = True

                        tmp = len(line)

                    else:
                        tmp = add_literal(line, pos)

                        if tmp != pos:
                            value = line[pos:tmp]
                            token_table.append(Token(value, TokenType.literal, line_index, pos))

                        else:
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
                                    raise Exception(f"{pos}: Unexpected character: {line[pos]}")

                    pos = tmp

                except Exception as e:
                    raise Exception(str(line_index) + ',' + str(e))

                pos = skip_blank(line, pos)
            
            if token_table[-1].token_type in {TokenType.identifier, TokenType.literal} or token_table[-1].name in {KeywordName.K_BREAK, KeywordName.K_CONTINUE, KeywordName.K_RETURN, OperatorName.O_INCREMENT, OperatorName.O_DECREMENT, PunctuationName.P_PARENTHESES_C, PunctuationName.P_BRACES_C, PunctuationName.P_BRACKETS_C}:
                token_table.append(Token(";", TokenType.operator, line_index, pos))
    
    token_table.append(Token("", TokenType.file_end, -1, -1))
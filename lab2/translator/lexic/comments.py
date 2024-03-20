from enum import StrEnum



C_LEN = 2


class CommentName(StrEnum):
    C_MULTILINE_START = "/*"
    C_MULTILINE_END = "*/"
    C_SINGLELINE = "//"


comments = {
    CommentName.C_MULTILINE_START,
    CommentName.C_MULTILINE_END,
    CommentName.C_SINGLELINE
}


def get_comment(line, pos):
    end_pos = pos + C_LEN

    if end_pos < len(line):
        if line[pos : end_pos] in comments:
            return end_pos
    
    return pos
from enum import StrEnum


ENCODING_TYPE="utf-8"


class character(StrEnum):
    let_a = 'a'
    let_b = 'b'
    let_c = 'c'
    let_d = 'd'
    let_e = 'e'
    let_f = 'f'
    let_g = 'g'
    let_h = 'h'
    let_i = 'i'
    let_j = 'j'
    let_k = 'k'
    let_l = 'l'
    let_m = 'm'
    let_n = 'n'
    let_o = 'o'
    let_p = 'p'
    let_q = 'q'
    let_r = 'r'
    let_s = 's'
    let_t = 't'
    let_u = 'u'
    let_v = 'v'
    let_w = 'w'
    let_x = 'x'
    let_y = 'y'
    let_z = 'z'
    let_A = 'A'
    let_B = 'B'
    let_C = 'C'
    let_D = 'D'
    let_E = 'E'
    let_F = 'F'
    let_G = 'G'
    let_H = 'H'
    let_I = 'I'
    let_J = 'J'
    let_K = 'K'
    let_L = 'L'
    let_M = 'M'
    let_N = 'N'
    let_O = 'O'
    let_P = 'P'
    let_Q = 'Q'
    let_R = 'R'
    let_S = 'S'
    let_T = 'T'
    let_U = 'U'
    let_V = 'V'
    let_W = 'W'
    let_X = 'X'
    let_Y = 'Y'
    let_Z = 'Z'
    dig_0 = '0'
    dig_1 = '1'
    dig_2 = '2'
    dig_3 = '3'
    dig_4 = '4'
    dig_5 = '5'
    dig_6 = '6'
    dig_7 = '7'
    dig_8 = '8'
    dig_9 = '9'
    underline = '_'
    space = ' '
    newline = '\n'
    tab = '\t'
    gt = '>'
    lt = '<'
    eq = '='
    exclamation_mark = '!'
    question_mark = '?'
    and_mark = '&'
    or_mark = '|'
    plus = '+'
    minus = '-'
    slash = '/'
    star = '*'
    percent = '%'
    comma = ','
    period = '.'
    semicolon = ';'
    colon = ':'
    parantheses_o = '('
    parentheses_c = ')'
    braces_o = '{'
    braces_c = '}'
    brackets_o = '['
    brackets_c = ']'
    quotes = '"'


uppercase_letters = {
    character.let_A,
    character.let_B,
    character.let_C,
    character.let_D,
    character.let_E,
    character.let_F,
    character.let_G,
    character.let_H,
    character.let_I,
    character.let_J,
    character.let_K,
    character.let_L,
    character.let_M,
    character.let_N,
    character.let_O,
    character.let_P,
    character.let_Q,
    character.let_R,
    character.let_S,
    character.let_T,
    character.let_U,
    character.let_V,
    character.let_W,
    character.let_X,
    character.let_Y,
    character.let_Z
}


lowercase_letters = {
    character.let_a,
    character.let_b,
    character.let_c,
    character.let_d,
    character.let_e,
    character.let_f,
    character.let_g,
    character.let_h,
    character.let_i,
    character.let_j,
    character.let_k,
    character.let_l,
    character.let_m,
    character.let_n,
    character.let_o,
    character.let_p,
    character.let_q,
    character.let_r,
    character.let_s,
    character.let_t,
    character.let_u,
    character.let_v,
    character.let_w,
    character.let_x,
    character.let_y,
    character.let_z
}


letters = lowercase_letters | uppercase_letters


digits = {
    character.dig_0,
    character.dig_1,
    character.dig_2,
    character.dig_3,
    character.dig_4,
    character.dig_5,
    character.dig_6,
    character.dig_7,
    character.dig_8,
    character.dig_9,
}


word_characters = letters | digits | {character.underline,}


word_separators = {
    character.gt,
    character.lt,
    character.eq,
    character.newline,
    character.space,
    character.tab,
    character.exclamation_mark,
    character.question_mark,
    character.and_mark,
    character.or_mark,
    character.plus,
    character.minus,
    character.slash,
    character.star,
    character.percent,
    character.comma,
    character.period,
    character.semicolon,
    character.parantheses_o,
    character.parentheses_c,
    character.braces_o,
    character.braces_c,
    character.brackets_o,
    character.brackets_c,
    character.colon
}


valid_characters = word_characters | word_separators | {character.quotes,}


blank = {
    character.space,
    character.tab
}


exponent = {
    character.let_e,
    character.let_E
}


def skip_word(line, pos):

    while pos + 1 < len(line) and line[pos] in word_characters:
        pos += 1

    return pos


def skip_blank(line, pos):

    while pos + 1 < len(line) and line[pos] in blank:
        pos += 1

    return pos


def skip_number(line, pos):

    while pos + 1 < len(line) and line[pos] in digits:
        pos += 1

    return pos

def convertToCompareFormat(name):
    compare_string = name.lower()
    if len(compare_string) > 1:
        tmp_str = compare_string.replace('#ACTOR#', '').lower().replace('$', '').replace('[', '').replace(']', '') \
            .replace('_', '+').replace(' ', '+').replace('\t', '')
        tmp_str = remove_text_paranthesis(tmp_str)
        if len(tmp_str) > 2 and tmp_str[0] == '+':
            tmp_str = tmp_str[1:]
        elif len(tmp_str) > 2 and tmp_str[-1] == '+':
            tmp_str = tmp_str[:-1]
        compare_string = tmp_str
    return compare_string


def remove_text_paranthesis(sentence):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in sentence:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')' and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret
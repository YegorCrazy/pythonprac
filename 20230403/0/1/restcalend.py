"""This is a module that crates rest-table with calendar."""
import calendar
import sys


def derive_string(s):
    """Derive date string with '|'"""
    res = '|'
    for i in range(0, len(s), 3):
        res += s[i:i+2]
        res += '|'
    return res


def restcalend(year, month):
    """Make a rest calendar teble."""
    cal = calendar.month(year, month).split('\n')
    if cal[-1] == '':
        del cal[-1]
    width = max([len(s) for s in cal])
    cal[0] += ' ' * (width - len(cal[0]))
    cal[-1] += ' ' * (width - len(cal[-1]))
    derivative_string = '+' + '+'.join(
        ['--' for i in range(7)]
        ) + '+'
    output = 'Calendar\n========\n\n'
    output += '+' + ('-' * width) + '+\n'
    output += '|' + cal[0] + '|\n'
    output += derivative_string + '\n'
    for s in cal[1:]:
        output += derive_string(s) + '\n'
        output += derivative_string + '\n'
    return output


if __name__ == '__main__':
    print(restcalend(int(sys.argv[1]), int(sys.argv[2])))

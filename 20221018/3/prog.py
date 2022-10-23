from collections import Counter

def only_lower_letters(s):
    res = ''
    for ch in s:
        if ch.isalpha():
            res += ch.lower()
        else:
            res += ' '
    return res

if __name__ == '__main__':
    
    word_len = int(input())
    cnt = Counter()
    
    while True:
        try:
            s = input().strip()
        except EOFError:
            break
        if s == '':
            break
        s = only_lower_letters(s).split()
        for word in s:
            if len(word) == word_len:
                cnt[word] += 1

max_num = max(cnt.values())
print(*sorted([x for x in cnt if cnt[x] == max_num]), sep = ' ')

    
    
    

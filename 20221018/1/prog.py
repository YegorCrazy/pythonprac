text = input().lower()
d = {}
for i in range(len(text) - 1):
    if text[i].isalpha() and text[i + 1].isalpha():
        key = text[i] + text[i + 1]
        d[key] = d.get(key, 0)
print(len(d))

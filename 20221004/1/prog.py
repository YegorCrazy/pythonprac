def rec_find(ch, string):
	if len(string) == 0:
		return False
	center = (len(string) // 2) if (len(string) % 2) else ((len(string) // 2) - 1)
	if ch == string[center]:
		return True
	elif ch > string[center]:
		return rec_find(ch, string[center + 1:])
	else:
		return rec_find(ch, string[:center])

ch, string = eval(input())
print(rec_find(ch, string))

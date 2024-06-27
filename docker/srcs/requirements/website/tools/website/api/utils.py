def parse_name(name: str) -> str:
	result = str()
	for i in range(0, len(name), 1):
		if name[i].isspace():
			continue
		if i > 0 and name[i].isupper() and not name[i - 1].isupper():
			result += ' '
		result += name[i]
	return result

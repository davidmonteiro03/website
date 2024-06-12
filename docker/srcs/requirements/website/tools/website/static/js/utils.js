function ft_strchr(str, c) {
	for (let i = 0; i < str.length; i++)
		if (str[i] == c)
			return true;
	return false;
}

function ft_split(str, c) {
	let ret = [];
	let it = 0;
	while (it < str.length) {
		while (it < str.length && str[it] === c) it++;
		let start = it;
		while (it < str.length && str[it] !== c) it++;
		let end = it;
		if (end > start) ret.push(str.substring(start, end));
		while (it < str.length && str[it] === c) it++;
	}
	return ret;
}

function ft_strcntchr(str, c) {
	let count = 0;
	for (let i = 0; i < str.length; i++)
		if (str[i] == c)
			count++;
	return count;
}

function ft_strschchr(str, charset) {
	for (let i = 0; i < str.length; i++)
		if (ft_strchr(charset, str[i]))
			return true;
	return false;
}

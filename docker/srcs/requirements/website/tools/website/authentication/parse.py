from django.contrib.auth.hashers import make_password

def name(name: str) -> str:
	name = name.strip()
	if len(name) < 3:
		return None
	if len(name) > 32:
		return None
	if not name.isalpha():
		return None
	return name.capitalize()

def username(username: str) -> str:
	username = username.strip()
	if len(username) < 3:
		return None
	if len(username) > 32:
		return None
	for i in range(len(username)):
		if username[i].isupper():
			return None
		if username[i] in '-_.' or username[i].isalnum():
			continue
		return None
	if not username[0].isalnum():
		return None
	return username

def email(email: str) -> str:
	email = email.strip()
	if len(email) < 5:
		return None
	if len(email) > 97:
		return None
	main_values = email.split('@')
	at_count = email.count('@')
	main_count = len(main_values)
	if main_count != 2 or at_count != main_count - 1:
		return None
	if username(main_values[0]) == None:
		return None
	domain_values = main_values[1].split('.')
	dot_count = main_values[1].count('.')
	domain_count = len(domain_values)
	if domain_count < 2 or dot_count != domain_count - 1:
		return None
	if len(main_values[1]) < 2:
		return None
	if len(main_values[1]) > 64:
		return None
	for i in range(domain_count):
		if not domain_values[i].isalnum():
			return None
	return main_values[0] + '@' + main_values[1]

def password(password: str) -> str:
	password = password.strip()
	if len(password) < 8:
		return None
	if len(password) > 32:
		return None
	if password.isspace():
		return None
	if not any(char.isdigit() for char in password):
		return None
	if not any(char.islower() for char in password):
		return None
	if not any(char.isupper() for char in password):
		return None
	if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
		return None
	return make_password(password)

def ligaportugal(data):
	try:
		ret_data = data[0]['Classificacoes']
		for club in ret_data:
			club['DiferencaGolos'] = club['GolosMarcados'] - club['GolosSofridos']
		return ret_data
	except:
		return None

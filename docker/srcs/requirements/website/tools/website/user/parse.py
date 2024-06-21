# import Django modules
from django.contrib.auth.hashers import make_password

# Function to parse name
def name(name: str) -> str:
	if len(name) < 3: # Check if name is less than 3 characters
		return None # Return None
	if len(name) > 32: # Check if name is greater than 32 characters
		return None # Return None
	if not name.isalpha(): # Check if name is not alphabetic
		return None # Return None
	return name.capitalize() # Return capitalized name

# Function to parse username
def username(username: str) -> str:
	if len(username) < 3: # Check if username is less than 3 characters
		return None # Return None
	if len(username) > 32: # Check if username is greater than 32 characters
		return None # Return None
	for i in range(len(username)): # Iterate over username
		if username[i].isupper(): # Check if character is uppercase
			return None # Return None
		if username[i] in '-_.' or username[i].isalnum(): # Check if character is alphanumeric or in '-_.'
			continue # Continue
		return None # Return None
	if not username[0].isalnum(): # Check if first character is alphanumeric
		return None # Return None
	return username # Return username

# Function to parse email
def email(email: str) -> str:
	if len(email) < 5: # Check if email is less than 5 characters
		return None # Return None
	if len(email) > 97: # Check if email is greater than 97 characters
		return None # Return None
	main_values = email.split('@') # Split email by '@'
	at_count = email.count('@') # Count '@' in email
	main_count = len(main_values) # Count main values
	if main_count != 2 or at_count != main_count - 1: # Check if main count is not 2 or at count is not main count - 1
		return None # Return None
	if username(main_values[0]) == None: # Check if username is None
		return None # Return None
	domain_values = main_values[1].split('.') # Split domain values
	dot_count = main_values[1].count('.') # Count '.' in domain values
	domain_count = len(domain_values) # Count domain values
	if domain_count < 2 or dot_count != domain_count - 1: # Check if domain count is less than 2 or dot count is not domain count - 1
		return None # Return None
	if len(main_values[1]) < 2: # Check if domain is less than 2 characters
		return None # Return None
	if len(main_values[1]) > 64: # Check if domain is greater than 64 characters
		return None # Return None
	for i in range(domain_count): # Iterate over domain values
		if not domain_values[i].isalnum(): # Check if domain value is not alphanumeric
			return None # Return None
	return main_values[0] + '@' + main_values[1] # Return email

# Function to parse password
def password(password: str) -> str:
	if len(password) < 8: # Check if password is less than 8 characters
		return None # Return None
	if len(password) > 32: # Check if password is greater than 32 characters
		return None # Return None
	if password.isspace(): # Check if password is whitespace
		return None # Return None
	if not any(char.isdigit() for char in password): # Check if any character is a digit
		return None # Return None
	if not any(char.islower() for char in password): # Check if any character is lowercase
		return None # Return None
	if not any(char.isupper() for char in password): # Check if any character is uppercase
		return None # Return None
	if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password): # Check if any character is a special character
		return None # Return None
	return make_password(password) # Return hashed password

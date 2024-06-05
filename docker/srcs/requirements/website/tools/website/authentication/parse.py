# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parse.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 12:41:30 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 12:41:33 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from django.contrib.auth.hashers import make_password
from .models import Users

def name(name):
	name = name.strip()
	if len(name) < 3:
		return None
	if len(name) > 32:
		return None
	if not name.isalpha():
		return None
	return name.capitalize()

def username(username):
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

def email(email):
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

def password(password):
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
	if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
		return None
	return make_password(password)

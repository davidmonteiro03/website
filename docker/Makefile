# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:34:55 by dcaetano          #+#    #+#              #
#    Updated: 2024/08/29 15:18:27 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: build up

build:
	@docker-compose -f ./srcs/docker-compose.yml build

up:
	@docker-compose -f ./srcs/docker-compose.yml up

down:
	@docker-compose -f ./srcs/docker-compose.yml down

restart:
	@docker-compose -f ./srcs/docker-compose.yml restart

clean: down
	@docker-compose -f ./srcs/docker-compose.yml down -v

fclean: clean
	@docker system prune -af

rerun: down up

re: fclean all

.PHONY: all up down restart clean fclean rerun re

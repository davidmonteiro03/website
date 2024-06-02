# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:34:55 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/02 16:07:20 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: up

up:
	@docker-compose -f ./srcs/docker-compose.yml up --build -d

down:
	@docker-compose -f ./srcs/docker-compose.yml down

clean: down
	-@docker volume ls -q | xargs -r docker volume rm -f 2>&1

fclean: clean
	-@docker images -qa | xargs -r docker rmi 2>&1
	@docker system prune -af

re: clean up

.PHONY: all up down clean fclean re

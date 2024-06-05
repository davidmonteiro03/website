# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:16:05 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 13:30:03 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: setup run

setup:
	@cd tools && sh ./setup.sh && cd ..

clean:
	@cd tools && sh ./clean.sh && cd ..

run:
	@cd tools && sh ./run.sh && cd ..

re: clean all

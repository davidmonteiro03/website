# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:13:46 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 13:29:14 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./website
python3 manage.py makemigrations authentication
python3 manage.py migrate
python3 manage.py collectstatic --noinput
cd ..

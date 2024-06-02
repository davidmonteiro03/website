# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    entrypoint.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:42:25 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/02 15:30:46 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd /website
python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000

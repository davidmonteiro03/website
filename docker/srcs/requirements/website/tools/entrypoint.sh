# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    entrypoint.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:42:25 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/15 16:06:38 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd /website
python manage.py makemigrations backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:5000

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    entrypoint.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:42:25 by dcaetano          #+#    #+#              #
#    Updated: 2024/08/29 15:38:20 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd /website
python manage.py makemigrations api user
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:$PORT

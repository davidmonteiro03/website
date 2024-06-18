# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:38:01 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/18 15:07:46 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

< ./docker/srcs/.env
if [ $? -ne 0 ]; then
	echo "You need to create a .env file in the ./docker/srcs folder"
	exit 1
fi
cd ./docker/srcs/requirements/website/tools/website
if [ -f ../../../../.env ]; then
	export $(cat ../../../../.env | xargs)
	output="from django.contrib.auth.models import User\n\
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD')"
fi
python3 manage.py makemigrations api backend
python3 manage.py migrate
echo $output | python3 manage.py shell
python3 manage.py collectstatic --noinput
cd ../../../../../..

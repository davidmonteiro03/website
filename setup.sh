# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:38:01 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/18 10:27:41 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

< $PWD/docker/srcs/.env
if [ $? -ne 0 ]; then
	exit 1
fi
cd ./docker/srcs/requirements/website/tools/website
if [ -f ../../../../.env ]; then
	export $(cat ../../../../.env | xargs)
	output="from django.contrib.auth.models import User\n\
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD')"
fi
python3 manage.py makemigrations backend
python3 manage.py migrate
echo $output | python3 manage.py shell
python3 manage.py collectstatic --noinput
cd ../../../../../..

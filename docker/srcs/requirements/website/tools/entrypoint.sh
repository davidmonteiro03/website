# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    entrypoint.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:42:25 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/19 10:25:02 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh
output="from django.contrib.auth.models import User\n\
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD')"
cd /website
python manage.py makemigrations api auth
python manage.py migrate
echo $output | python3 manage.py shell
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:$PORT

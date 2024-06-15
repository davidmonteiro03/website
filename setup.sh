# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:38:01 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/15 16:07:46 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./docker/srcs/requirements/website/tools/website
python manage.py makemigrations backend
python manage.py migrate
python manage.py collectstatic --noinput
cd ../../../../../..

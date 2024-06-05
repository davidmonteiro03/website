# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    setup.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:38:01 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 13:40:57 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./docker/srcs/requirements/website/tools/website
python3 manage.py makemigrations authentication
python3 manage.py migrate
python3 manage.py collectstatic --noinput
cd ../../../../../..

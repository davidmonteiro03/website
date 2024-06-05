# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    run.sh                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:41:41 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 13:42:05 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./docker/srcs/requirements/website/tools/website
python3 manage.py runserver 0.0.0.0:5000
cd ../../../../../..

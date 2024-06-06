# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    clean.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:39:02 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/06 19:17:53 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./docker/srcs/requirements/website/tools/website
rm -rf ./*.sqlite3 ./backend/migrations/ ./staticfiles/
find . -name "__pycache__" -type d -exec rm -rf {} +
cd ../../../../../..

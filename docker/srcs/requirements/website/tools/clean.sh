# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    clean.sh                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 13:09:09 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 13:27:57 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

cd ./website
rm -rf ./*.sqlite3 ./authentication/migrations/ ./staticfiles/
find . -name "__pycache__" -type d -exec rm -rf {} +
cd ..

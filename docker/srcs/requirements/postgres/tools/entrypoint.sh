# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    entrypoint.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/17 07:51:24 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/17 09:05:17 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

service postgresql start

if service postgresql status | grep -q "online"; then
	echo "PostgreSQL is running."
else
	echo "Failed to start PostgreSQL."
	exit 1
fi

eval "psql <<eof
CREATE USER website WITH PASSWORD 'website';
ALTER USER website WITH SUPERUSER;
CREATE DATABASE website;
GRANT ALL PRIVILEGES ON DATABASE website TO website;
\q
eof"

while true; do
	if ! service postgresql status | grep -q "online"; then
		echo "PostgreSQL is not running. Starting it..."
		service postgresql start
	fi
	sleep 10
done

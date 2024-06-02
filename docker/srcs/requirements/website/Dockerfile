# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:35:50 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/02 10:34:12 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y\
	python3 python3-pip python3-django

COPY ./tools/website /website
COPY ./tools/entrypoint.sh /tmp/entrypoint.sh

RUN chmod +x /tmp/entrypoint.sh

ENTRYPOINT [ "sh", "/tmp/entrypoint.sh" ]

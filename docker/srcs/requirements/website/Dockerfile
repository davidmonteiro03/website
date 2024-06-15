# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dockerfile                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/02 08:35:50 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/07 13:04:06 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

FROM debian:bullseye

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip python-is-python3

COPY ./tools/website /website
COPY ./tools/entrypoint.sh /tmp/entrypoint.sh
COPY ./tools/requirements.txt /tmp/requirements.txt

RUN chmod +x /tmp/entrypoint.sh
RUN pip install -r /tmp/requirements.txt

ENTRYPOINT [ "sh", "/tmp/entrypoint.sh" ]

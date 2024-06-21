# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    info.sh                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/18 12:44:49 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/21 23:22:02 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

clear
echo -n "\n\
██████╗  ██████╗  ██████╗██╗  ██╗███████╗██████╗    ██╗███╗   ██╗███████╗ ██████╗\n\
██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗   ██║████╗  ██║██╔════╝██╔═══██╗\n\
██║  ██║██║   ██║██║     █████╔╝ █████╗  ██████╔╝   ██║██╔██╗ ██║█████╗  ██║   ██║\n\
██║  ██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗   ██║██║╚██╗██║██╔══╝  ██║   ██║\n\
██████╔╝╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║   ██║██║ ╚████║██║     ╚██████╔╝\n\
╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝\n\
"
printf '\n%*s' "$(tput cols)" '' | tr ' ' '='
echo "CONTAINERS"
printf '%*s' "$(tput cols)" '' | tr ' ' '-'
docker ps -a
printf '\n%*s' "$(tput cols)" '' | tr ' ' '='
echo "IMAGES"
printf '%*s' "$(tput cols)" '' | tr ' ' '-'
docker images -a
printf '\n%*s' "$(tput cols)" '' | tr ' ' '='
echo "NETWORKS"
printf '%*s' "$(tput cols)" '' | tr ' ' '-'
docker network ls
printf '\n%*s' "$(tput cols)" '' | tr ' ' '='
echo "VOLUMES"
printf '%*s' "$(tput cols)" '' | tr ' ' '-'
docker volume ls
printf '\n%*s' "$(tput cols)" '' | tr ' ' '='
echo "SYSTEM"
printf '%*s' "$(tput cols)" '' | tr ' ' '-'
docker system df

echo

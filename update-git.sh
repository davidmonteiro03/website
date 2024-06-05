# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    update-git.sh                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dcaetano <dcaetano@student.42porto.com>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/05 12:36:11 by dcaetano          #+#    #+#              #
#    Updated: 2024/06/05 12:36:11 by dcaetano         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/sh

clear
str=""
for arg in "$@"; do
	str="$str$arg"
done
if [ -z "$str" ]; then
	str="git updates"
fi
echo "=========== GIT STATUS ==========="
echo
git status
echo
echo "============= GIT ADD ============"
echo
echo "         adding files...          "
git add .
echo
echo "=========== GIT STATUS ==========="
echo
git status
echo
echo "=========== GIT COMMIT ==========="
echo
git commit -m "$str"
echo
echo "============ GIT PUSH ============"
echo
git push
echo

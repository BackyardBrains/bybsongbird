#!/usr/bin/env bash

# Update apt-get first (system package installer)
sudo apt-get update

# Install the only editors you'll ever need.
sudo apt-get install vim emacs --yes

sudo apt-get install git

# Install Python pip with --yes as the default argument
sudo apt-get install python-pip --yes

# Install virtualenv used for 485 projects
sudo pip install virtualenv

# By default, while installing MySQL, there will be a blocking prompt asking you to enter the password
# Next two lines set the default password of root so there is no prompt during installation
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'

# Install MySQL server with the default argument --yes
sudo apt-get install mysql-server --yes
sudo apt-get install build-essential python-dev libmysqlclient-dev --yes

# So that we can load XML infile for SQL purposes (used in project 1)
sudo printf "\n[mysqld]\nlocal-infile\n\n[mysql]\nlocal-infile\n" >> /etc/mysql/my.cnf


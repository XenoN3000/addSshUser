#!/usr/bin/env python

from __future__ import print_function
from builtins import *

import csv

import sys
import getpass
import re
import pwd
import os

file_path = 'users.csv'


def csv_reader(file):
    with open(f'{file}') as file:
        csvdata = list(csv.reader(file))
        data_list = []
        for row in csvdata:
            data_list.append(User(row[0], row[1], row[2]))

        return data_list


class User:
    def __init__(self, username, password, group):
        self.username = username
        self.password = password
        self.group = group


def root_check():
    """Exit if login name not root."""

    if not getpass.getuser() == 'root':
        print("ERROR: THIS PROGRAM REQUIRES ROOT PRIVILEGES. EXITING.")
        sys.exit()


def is_username_valid(username):
    if len(username) < 3:
        print(f"SORRY, THAT'S NOT ALLOWED. TRY AGAIN. {username}")
        return False

    print(f"OK ...")
    return True


def username_check(username):
    """Check if username exists."""
    check = is_username_valid(username)
    if not check:
        return False

    try:
        pwd.getpwnam(username)
        print(f"USER {username} EXISTS. TRY A DIFFERENT USERNAME.")
        return False

    except KeyError:
        print(f"User {username} does not exist. Continuing...")
        return check


def check_password(password):
    if len(password) < 4:
        print("SORRY, THAT'S NOT ALLOWED. TRY AGAIN.")
        return False
    return True


def add_usr(user: User):
    """Call the useradd command to create an account with given parameters."""

    print(f"Adding user: {user.username}")

    # create user
    # create group with same name as user, adding user to group
    # comment (lastname, firstname)
    # create home directory
    # login shell
    # password (encrypted via openssl)

    os.system("useradd --create-home \
    --home /home/" + user.username + " \
    --shell /bin/bash \
    --password $(printf %s " + user.password + " |openssl passwd -1 -stdin) " + user.username + "")

    print("Done.")


def create_group(group_name):
    os.system("groupadd " + group_name)


def add_to_group(group, username):
    os.system(f"usermod -a -G {group} {username}")


def add_usres(users: [User]):
    """Add user to Linux OS."""

    root_check()

    create_group("maxlogin_2")

    for user in users:
        if username_check(user.username) and check_password(user.password):
            add_usr(user)

        if len(user.group) > 0:
            add_to_group(user.group, user.username)


if __name__ == '__main__':
    users_list = csv_reader(file_path)
    add_usres(users_list)

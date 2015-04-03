# Rameel Sethi
# CS 305
# Project 1 Part 1
# SimpleWebBrowser.py
# A simple web client.
# Enter host (can only do so once in program runtime,
# please no www. prefix), followed by object name
# (please enter full path with slashes before each
# directory, no slash after filename)
# Shortcuts:
# b: Get previous page
# f: Get next page
# r: Refresh current page
# q: Quit the web client
# NOTE: os module needed for finding client file 
# directories for caching purposes, sys for exceptions,
# and email.utils for formatting file timestamp into 
# RFC 2822 compliant date

import os
import sys
from email.utils import *
from socket import *

# Use port 80
PORT_NUMBER = 80

# Finds the given object on the given host.
# If the file has been cached previously, the client
# file is displayed. Otherwise, the page is fetched 
# from the host and cached on the client.
def browse(host_name, object_name):
	# Get current working directory
	cwd = os.getcwd()

	# Get full directory by joining with object
	filedir = cwd + object_name

	# Split into filepath and filename
	filepath, filename = os.path.split(filedir)
	
	# Construct GET request
	req = "GET " + object_name + " HTTP/1.1\r\n"
	
	# Insert Host header
	req = req + "Host: www." + host_name + "\r\n"
	
	# If file is cached on client, add If-Modified-
	# Since header and put in dat file was created
	if(os.path.isfile(filedir)):
		req = req + "If-Modified-Since: "
		req = req + formatdate(os.path.getctime(filedir)) + "\r\n"
	
	# Add empty line to mark end of GET request
	req = req + "\r\n"
	
	# Setup client socket
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((host_name, PORT_NUMBER))
	clientSocket.send(req)
	
	# Fetch HTTP response
	res = clientSocket.recv(4096)

	# Get status code which is first header of response
	res = res.split("\r\n")
	status_code = res[0]
	
	# If file needed to be retrieved and was 
	# succesfully found
	if status_code == "HTTP/1.1 200 OK":
		# Get content which is last header
		# and strip trailing whitespace
		content = res[len(res) - 1].rstrip()

		# If file does not exist on client, cache it
		# by making new directory, navigating there,
		# writing new file and heading back into top 
		# level directory (where program was run)
		# If writing error occurs, tell user so 
		try:
			if not os.path.isdir(filepath):
				os.makedirs(filepath)
			os.chdir(filepath)
			file_writer = open(filename, 'w')
			file_writer.write(content)
			file_writer.close()
			os.chdir(cwd)
			# Display the content
			print "Retrieved object:"
			print content
		except IOError:
			print "Sorry, error writing file."

	# Otherwise if the file was not modified on the
	# server since it was last saved on the client
	elif status_code == "HTTP/1.1 304 Not Modified":	
		# Navigate to file, read and display the 
		# contents, and navigate back
		# If reading error occurs, tell user so
		try: 
			os.chdir(filepath)
			file_reader = open(filename, 'r')
			print "Cached copy:"
			print file_reader.read() 
			file_reader.close()
			os.chdir(cwd)
		except IOError:
			print "Sorry, error reading file."

	# If neither fetched nor cached copy found, display
	# error along with status code
	else:
		print("Sorry, there was an error getting the page: " +
			  status_code)

	# Close the socket
	clientSocket.close()

# Main method
def main():
	# Stack for maintaining previous pages
	back_stack = []

	# Stack for maintaining next pages
	forward_stack = []

	# Name of currently visited object
	curr_object = ""

	# Prompt user for host name
	host_name = raw_input('Enter host name: ')
	
	# While user has not yet quit
	while True:
		# Prompt user for object name
		object_name = raw_input('Enter object name: ')
		# If previous page requested
		if object_name == 'b':
			# If no previous pages, tell user so
			if len(back_stack) == 0:
				print "Sorry, no more previous pages."
			# Otherwise push current object on next page
			# stack, pop previous page stack, make it
			# current object and browse
			else:
				forward_stack.append(curr_object)
				object_name = back_stack.pop()
				curr_object = object_name
				browse(host_name, object_name)
		# If next page requested
		elif object_name == 'f':
			# If no next pages, tell user so
			if len(forward_stack) == 0:
				print "Sorry, no more next pages."
			# Otherwise push current object on previous 
			# page stack, pop next page stack, make it
			# current object and browse
			else:
				back_stack.append(curr_object)
				object_name = forward_stack.pop()
				curr_object = object_name
				browse(host_name, object_name)
		# If current page refresh requested
		elif object_name == 'r':
			# If no current page yet, tell user so
			if curr_object == "":
				print "Sorry, no current page to refresh."
			# Otherwise browse current object
			else:
				object_name = curr_object
				browse(host_name, object_name)
		# If user wants to quit
		elif object_name == 'q':
			# Say goodbye and exit
			print "Goodbye..."
			break
		# Otherwise
		else:
			# If there is a current object, push
			# onto previous stack
			if not curr_object == "":
				back_stack.append(curr_object)
			# clear next stack, make object current 
			# one and browse
			forward_stack = []
			curr_object = object_name
			browse(host_name, object_name)

# Execute main on running file
if  __name__ =='__main__':
    main()

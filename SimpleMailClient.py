# Rameel Sethi
# CS 305
# Project 1 Part 2
# SimpleMailClient.py
# A simple SMTP email client.
# Enter SMTP server, sender address (Lafayette only please), 
# recipient addresses (separated by comma only, please) and 
# message (end with blank line) to send email!

from socket import *

# Use port 25
PORT_NUMBER = 25

# Client name should be Lafayette server to avoid
# connection refusal
CLIENT_NAME = "incoming.lafayette.edu"

# Sends request to server and returns response
# status code (3 digits)
def talk_to_server(socket, req):
	# Send request followed by CRLF
	socket.send(req + "\r\n")
	
	# Receive response in 1024 byte buffer
	res = socket.recv(1024)

	# Only return 3 digit status code
	return res[0:3]

# Checks status code against expected code
# and quits and printing error if mismatch
def check_error(socket, actual_code, 
				expected_code, error_message):
	if actual_code != expected_code:
		print error_message + " Closing connection..."
		socket.close()
		quit()

# Main method
def main():
	# Prompt user for SMTP server
	server_name = raw_input('Enter SMTP server name: ')
	
	# Prompt user for sender address and attach
	# open-close tags
	sender = raw_input('Enter sender email address: ')
	sender = '<' + sender + '>'
	
	# Prompt user for receiver addresses separated 
	# by commas, then extract into list and add tags
	rcv = raw_input('Enter receiver email addresses, '
					+ 'comma separated: ')
	rlist = rcv.split(',')
	receivers = []
	for receiver in rlist:
		receivers.append('<' + receiver + '>')
	
	# Prompt user for message, end with Enter on
	# empty line and assemble message from
	# individual entered lines
	print 'Enter message, empty line for end:'
	message = ""
	while True:
		line = raw_input()
		if line.strip() == "":
			break
		message += "%s\n" % line
	
	# Setup client socket
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((server_name, PORT_NUMBER))
	
	# Check if server is ready
	server_ready = client_socket.recv(1024)
	check_error(client_socket, server_ready[0:3], '220', 
				"Sorry, the server is offline.")
	
	# Check if server is willing to accept requests
	server_ok = talk_to_server(client_socket, 
							   "HELO " + CLIENT_NAME)
	check_error(client_socket, server_ok, '250', 
				"Sorry, the server didn't acknowledge your request.")
	
	# Check if sender address is valid (should
	# be Lafayette address only)
	sender_ok = talk_to_server(client_socket, "MAIL FROM: " + sender)
	check_error(client_socket, sender_ok, '250', 
				"Sorry, the sender address you entered is invalid.")
	
	# Loop through recipient list and check if
	# addresses are valid
	for receiver in receivers:
		receiver_ok = talk_to_server(client_socket, "RCPT TO: " + 
									 receiver)
		check_error(client_socket, receiver_ok, '250', 
					"Sorry, the recipient address " +
					receiver + " you entered is invalid.")
	
	# Check if client is clear to send data
	data_ok = talk_to_server(client_socket, "DATA")
	check_error(client_socket, data_ok, '354', 
				"Sorry, the server cannot accept new emails.")
	
	# Check if message is able to be sent
	message_ok = talk_to_server(client_socket, message + "\r\n.")
	check_error(client_socket, message_ok, '250', 
				"Sorry, the server cannot send this message.")
	
	# Check if quitting is possible
	quit_ok = talk_to_server(client_socket, "QUIT")
	check_error(client_socket, quit_ok, '221', 
				"Message sent, but the server could not quit.")
	
	# Indicate that email has been sent
	# and close socket
	print "Sent!"
	client_socket.close()

# Execute main on running file
if  __name__ =='__main__':
    main()
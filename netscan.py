#!/usr/bin/python
import re
import socket

IPv4__PATTERN__=r'\b(?:25[0-5]\.|2[0-4]\d\.|1\d\d\.|\d\d\.|\d\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|\d\d|\d)\b'
FQDN__PATTERN__=r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}$)'

__REQUESTS__={
	"GET":r'''GET / HTTP/1.1\r\n
Host: google.com\r\n
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0\r\n
Accept: */*\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate, br\r\n
Cache-Control: no-cache\r\n
Pragma: no-cache\r\n
Connection: keep-alive\r\n
'''
}

def prompt():
	host_mode_prompt="enter host> "
	port_mode_prompt="enter port> "
	mode="hostmode"


	__TARGET__=""
	last_message=""
	while ( last_message != "exit" ):
		if ( mode == "portmode" ):
			message=input(f'enter port [{__TARGET__}]> ')
			if ( message == "exit"):	
				break
			if ( message == "back" ):
				mode="hostmode"

			ports=re.findall(r'\d{1,5}',message)

			for port in ports:
				print(f'[ * ] Scanning port {port} on host {__TARGET__}\r\n')
				try:
					sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					sock.settimeout(1)
					server=(__TARGET__,int(port))
					sock.connect(server)
					##SUCCESSFUL CONNECTION
					print(f'[ + ] Successful connection to {__TARGET__}:{port}\r\n')

					#HTTP REQUESTS
					if ( int(port) == 80 or int(port) == 443 ):
							request=r'''GET / HTTP/1.1\r\n
							Host: {__TARGET__}\r\n
							Accept: */*\r\n
							Connection: keep-alive\r\n'''	
							try:
								Request=(input(f'enter web request [{__TARGET__}:{port}]> '))
								if ( Request.upper() == "GET" ):
									sock.sendall(__REQUESTS__.get("GET").encode('utf-8'))
									response = b''
									while True:
										data = sock.recv(4096)  # Receive data in chunks
										if not data:
											break
										response += data
									print(re.search(r'(?s)\r?\n\r?\n(.*)',response.decode()).group(1))

							except ValueError:
								print("[ - ] Invalid request")
					sock.close()

				except ConnectionRefusedError:
					print(f'[ - ] Could not connect to {__TARGET__}:{port}')
					sock.close()
				except socket.timeout:
					print(f'[ - ] Connection timeout to {__TARGET__}:{port}')
					sock.close()
				except KeyboardInterrupt:
					sock.close()	
			
		elif ( mode == "hostmode" ):
			host=input(host_mode_prompt)
			match=re.search(IPv4__PATTERN__,host)
			if match:
				mode="portmode"
				last_message=match.group(0)
				__TARGET__=match.group(0)
				continue
			else:
				match=re.search(FQDN__PATTERN__,host)
				if match:
					mode="portmode"
					last_message=match.group(0)
					__TARGET__=match.group(0)
					continue

			last_message=host
		else:
			#Exit prompt
			message="exit"
			continue
	

prompt()

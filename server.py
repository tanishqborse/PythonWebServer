import socket
import ssl
import os
import sys
import threading
import subprocess
import datetime 

# Define HTTP response codes
RESPONSE_CODES = {
    200: 'OK',
    201: 'Created',
    400: 'Bad Request',
    403: 'Forbidden',
    404: 'Not Found',
    411: 'Length Required',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    505: 'HTTP Version Not Supported'
}

# Define supported HTTP methods
SUPPORTED_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

SUPPORTED_PROTOCOLS = ['HTTP/1.0', 'HTTP/1.1']

# Define function to handle incoming connections
def handle_connection(conn, client_address):
    # Read HTTP request
    request_data = conn.recv(1024)
    request = request_data.decode('utf-8')
    print("\n THIS IS THE REQUEST-\n" + request)
    log_first_line(request)
    

    # Parse HTTP request
    method, path, protocol = request.split('\n')[0].split()
    method=method.strip()
    print("Method =",method,"Path =",path,"Protocol =",protocol)
    print("\n\n")
    
    # Check if method is supported
    if method not in SUPPORTED_METHODS:
        send_response(conn, 501)
        return
    # Check if protocol is supported
    if protocol not in SUPPORTED_PROTOCOLS:
        send_response(conn, 502)
        return
    
    query=path.strip()
    filename=path.strip()
    protocol=protocol.strip()
    
    #Check for Query String 
    if '?' in path:
        query=path.strip().split('?')[1]
        filename=path.strip().split('?')[0]
        print("? exists")
        print("Filename =",filename,"query =",query,)
    else:
        query=""   
        print("? not exists")
        print("path =",path,"query =",query,"Filename =",filename)
    
    path2=os.getcwd() + filename
    print("\nRequested File Location =",path2,"\n")
    # Check if path exists and is accessible
    try:
        if not os.path.exists(path2):
            print("FILE NOT FOUND - ", path2)
            print("CURRENT DIRECTORY - " + os.getcwd())
            send_response(conn, 404)
        elif not os.access(path2, os.R_OK):
            print("CANNOT ACCESS REQUESTED FILE - ", path2)
            send_response(conn, 403)
        else:
            print("FILE ACCESS GRANTED - ", path2)
    except:
        print("ERROR OCCURRED")
        send_response(conn, 500)
    print("\n")
    # Handle HTTP method
    print("METHOD =",method)
    if method == 'GET':
        return getmethod(request, path2, query, conn)
    
    if method == 'POST':
        return postmethod(request,filename,conn)

    if method == 'PUT':
        return postmethod(request,path,conn)

    if method == 'DELETE':
        return putmethod(method, path2, filename, conn)

    if method == 'CONNECT':
        return putmethod(ipaddr, port, certpath, keypath)

def log_first_line(request):
    # Open the log file in append mode
    with open('log.txt', 'a') as f:
        # Get the current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Write the first line of the request to the log file
        f.write(f"{timestamp} {request.splitlines()[0]}\n")

def getmethod(request, path2, query, conn):
    # Extract the requested path from the HTTP GET request.
    print("GET FUNCTION 1")
    scriptname = path2
    query_string = query
    method= "GET"
    # Check if the request ends with a valid terminator.
    if not request.endswith('\r\n\r\n'):
        print("bad request")
        return '400 BAD REQUEST\r\n\r\n'
    
    # Check if file exists and is readable
    if not os.path.exists(path2):
        send_response(conn, 404)
        return '404 NOT FOUND\r\n\r\n' + 'The requested file was not found on this server.'
    if not os.access(path2, os.R_OK):
        send_response(conn, 403)
        return '403 FORBIDDEN\r\n\r\n' + 'You do not have permission to access the requested file.'
    
    print("GET FUNCTION 2")
    command ="export QUERY_STRING=\"" + query_string +"\";"
    command = command + "export SCRIPT_FILENAME=" + path2 +";"
    command = command + "export REQUEST_METHOD=" + method + ";"
    command = command + "export REDIRECT_STATUS=0;"
    command = command + "php-cgi " + scriptname 
    
    print("\nCOMMAND=",command,"\n")
    
    # Execute the PHP file with the command.
    try:
      php_output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
      print(php_output)
      send_response(conn, 200, php_output)
      return ('200 OK\r\nContent-Type: text/html\r\n\r\n' + str(php_output))
    except subprocess.CalledProcessError as e:
      print("Error running command:", e.output)
      return ('500 INTERNAL SERVER ERROR\r\n\r\n' + str(e))

def postmethod(request,filename,conn):
    print("\nfilename=",filename)
    
    request_lines = request.split("\r\n")
    print("\nrequest_lines=",request_lines)

    request_line = request_lines[0]
    host= request.split(": ")[1]
    print("host",host)

    method, uri, version = request_line.split()
    print("Method=",method,"URI=",uri,"Version =",version)

    # Check if the content-length header is set
    content_length = None
    content_type = None
    for line in request_lines[1:]:
        if line.startswith("Content-Length:"):
            content_length = int(line.split(":")[1].strip())
        if line.startswith("Content-Type:"):
            content_type = line.split(":")[1].strip()

    if content_length is None:
        send_response(conn, 411)
        return

    # Read the content of the request
    content = request.split("\r\n\r\n")[1]
    if content_type == "application/x-www-form-urlencoded":
        print("content=",content)
        

      
        command=""
        command= command + "export SCRIPT_FILENAME=." + filename + ";"
        command= command + "export REQUEST_METHOD="+ method + ";"
        command= command + "export GATEWAY_INTERFACE=\"CGI/1.1\";"
        command= command + "export SERVER_PROTOCOL=" + version + ";"
        command= command + "export REMOTE_HOST="+host+";"
        command= command + "export CONTENT_LENGTH="+str(content_length)+";"
        command= command + "export CONTENT_TYPE=\"application/x-www-form-urlencoded\";"
        command= command + "export REDIRECT_STATUS="+"0" + ";"
        command= command + "echo \"" + content + "\" | " 
        command= command + "php-cgi ."+filename 
   
        try:
            output = subprocess.check_output(command, shell=True)
            print("command=",command)
            print("output=",output)
            send_response(conn, 200, output)
        except subprocess.CalledProcessError as e:
            output = e.output
            send_response(conn, 500, output)


def deletemethod(method, path2, filename, conn):
    # Check if the file exists and is readable.
    if not os.path.exists(path2):
        return '404 NOT FOUND\r\n\r\n' + 'The requested file was not found on this server.'
    if not os.access(path2, os.R_OK):
        return '403 FORBIDDEN\r\n\r\n' + 'You do not have permission to access the requested file.'

    # Delete the file.
    os.remove(path2)

    return '200 OK\r\n\r\n' + 'File deleted successfully.'

def putmethod(method, path, body):
    # Check if the path is a valid file.
    if not os.path.isfile(path):
        return '404 NOT FOUND\r\n\r\n' + 'The requested file was not found on this server.'

    # Check if the file is writable.
    if not os.access(path, os.W_OK):
        return '403 FORBIDDEN\r\n\r\n' + 'You do not have permission to modify the requested file.'

    # Write the contents of the request body to the file.
    with open(path, 'wb') as f:
        f.write(body.encode('utf-8'))

    return '200 OK\r\n\r\n' + 'File modified successfully.'

# Function to start the server on the network.
def connect(ip_address, port, certpath, keypath):
    # Establish a socket communication.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Attach the socket with IP address and PORT provided when starting the server.
    s.bind((ipaddr, port))
    conn = ''
    # Check if the server is started in HTTPS mode or HTTP.
    if certpath is None and keypath is None:
        try:
            # Listen for incomming connections.
            s.listen() 
            while True:   
                # Accept conenction from client.        
                conn, addr = s.accept()    
                # Receive data from client.
                data = conn.recv(1024)
                # Convert data from bytes to strings for further processing.
                reqdata = data.decode('utf-8')
                # Call fucntion to check the validity and format of the request data from client.
                validity = validate(reqdata)
                if validity == 'valid':
                    # If the request is valid, function is called to parse the request data and send the response back to the client.
                    conn.sendall(parse_request(reqdata).encode('utf-8'))
                    # Close the client socket after successfull response.
                    conn.close()   
                # if request is not valid.
                else:
                    # Send the error code in response to request from client if request is not valid.
                    conn.sendall(validity.encode())
                    # Close the client socket.
                    conn.close()
        # CRTL-C command to terminate the server gracefully.    
        except KeyboardInterrupt:
            # Close the client socket.
            conn.close()
            # Close the server socket and release the bind.
            s.close()
            # Exit the program with message.               
            sys.exit('\r\n'+'Server terminated due to KeyboardInterrupt')


    # Server to start in HTTPS mode if cert nd key are provided initially.           
    else:
        # object for ssl layer with purpose of client authentication.
        obj = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # Discarding the support for SSLv3 due to compatibility issues.
        obj.options |= ssl.OP_NO_SSLv3
        # Load the SSL certificate and private key.
        obj.load_cert_chain(certfile=certpath, keyfile=keypath)
        sslsock=obj.wrap_socket(s, server_side=True)
        # Listen for incomming connections.
        sslsock.listen(1)
        while True:           
            # Accept conenction from client.  
            conn, addr = sslsock.accept()
     
            try: 
                # Receive data from client.
                data = conn.recv(1024)
                # Convert data from bytes to strings for further processing.
                reqdata = data.decode('utf-8')
                # Call fucntion to check the validity and format of the request data from client.
                validity = validate(reqdata)
                # If request is valid.
                if validity == 'valid':
                    # If the request is valid, function is called to parse the request data and send the response back to the client.
                    conn.sendall(parse_request(reqdata).encode())
                    # Close the client socket.
                    conn.close()
                
                else:
                    # Send the error code in response to request from client if request is not valid.
                    conn.sendall(validity.encode())
                    # Close the client socket
                    conn.close()
            # CRTL-C command to terminate the server gracefully. 
            except KeyboardInterrupt:
                # Close the client socket.
                conn.close()
                # Close the server socket and release the bind.
                sslsock.close()
                # Exit the program with message.               
                sys.exit('\r\n'+'Server terminated due to KeyboardInterrupt')
 

#Define function to send HTTP response
def send_response(client_socket, code, body=None, headers=None):
    response = f"HTTP/1.1 {code} {RESPONSE_CODES[code]}\r\n"
    if headers:
        for header, value in headers.items():
            response += f"{header}: {value}\r\n"
    if body:
        response += f"Content-Length: {len(body)}\r\n"
        response += "\r\n"
        print(body)
    if body:
        response += str(body.decode('utf-8'))
        print(response)
    client_socket.send(response.encode())
    client_socket.close()

def main():
    # Parse command line arguments
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python server.py <ip_address> <port> [<cert_file> <key_file>]")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    cert_file = sys.argv[3] if len(sys.argv) > 3 else None
    key_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    #Set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen()

    # If HTTPS is enabled, load SSL context
    if cert_file and key_file:
        if not os.path.exists(cert_file) or not os.path.exists(key_file):
            print("Cert or Key file not found")
            sys.exit(1)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        server_socket=context.wrap_socket(server_socket,server_side=True)
    else:
        context = None
        
    #print listening message
    if context:
        server_socket = ssl.wrap_socket(server_socket, certfile=cert_file, keyfile=key_file, server_side=True)
        print(f"Listening for HTTPS connections on {ip_address}:{port}...")
    else:
        print(f"Listening for HTTP connections on {ip_address}:{port}...")

    #Accept incoming connections and handle them
    while True:
        conn, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_connection, args=(conn, client_address))
        client_handler.start() 

main()

import re
import sys

def parse_req(request):
    try:
        # Regular expression pattern to match the HTTP request line (HTTP METHOD, RESOURCE PATH, VALID HTTP VERSION)
        pattern = re.compile(r'^(GET|POST|PUT|DELETE|CONNECT)\s+(/\S*)\s+HTTP/1\.[01]$')
        match = pattern.match(request.splitlines()[0])
        # Check if the request line matches the pattern
        if not match:
            return generate_response(400, 'Bad Request')
        
        # Extract the request method and resource from the request line
        method, resource = match.groups()
        
        # Validate the resource path
        if resource == '/':
            # Serve the default page for root resource
            response_body = 'Welcome to the Home Page!'
            return generate_response(200, 'OK', response_body)
        else:
            # Return 404 Not Found for any other resource
            return generate_response(404, 'Not Found')
    except:
        return generate_response(500,'Internal Server Error')

def generate_response(status_code, status_message, response_body=''):
    # Generate the HTTP response template
    response = f'\nHTTP/1.1 {status_code} {status_message}\r\n'
    response += '\r\n'
    response += f'{response_body}\n'
    
    return response

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('\n Please provide the path to the HTTP request file as a command line argument \n')
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r') as data:
            request = data.read()
    except Exception as error:
        print(f'Failed to read the file:\n{error}')
        sys.exit(1)
    
    response = parse_req(request)
    print(response)
import socket


HOST = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
PORT = 6790
print(HOST+':'+str(PORT))

# index.html
index_content = '''
HTTP/1.x 200 OK 
Content-Type: text/html

'''
f = open('index.html', 'r')
index_content = index_content + f.read()
f.close()

# client.js
js_content = '''
HTTP/1.x 200 OK 
Content-Type: text/javascript

'''
f = open('client.js', 'r')
js_content = js_content + f.read()
f.close()

# pic
background_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('background.png', 'rb')
background_content = background_content.encode(encoding='UTF-8') + f.read()
f.close()

blackStone_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('blackStone.png', 'rb')
blackStone_content = blackStone_content.encode(encoding='UTF-8') + f.read()
f.close()

whiteStone_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('whiteStone.png', 'rb')
whiteStone_content = whiteStone_content.encode(encoding='UTF-8') + f.read()
f.close()

favicon_content = '''
HTTP/1.x 200 OK 
Content-Type: image/ico

'''
f = open('favicon.ico', 'rb')
favicon_content = favicon_content.encode(encoding='UTF-8') + f.read()
f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

# while True:
#     try:
#         conn, addr = s.accept()
#         request = conn.recv(1024)
#         print(request.decode())
#         request = request.decode().split(' ')
#         # print(request)
#         method = request[0]
#         src = request[1]
#
#         if method == 'GET':
#             if src == '/index.html':
#                 conn.sendall(index_content.encode(encoding='UTF-8'))
#             elif src == '/client.js':
#                 conn.sendall(js_content.encode(encoding='UTF-8'))
#             elif src == '/background.png':
#                 conn.sendall(background_content)
#             elif src == '/blackStone.png':
#                 conn.sendall(blackStone_content)
#             else:
#                 conn.sendall(whiteStone_content)
#         conn.close()
#     except KeyboardInterrupt:
#         break
#     finally:
#         traceback.print_exc()
#         print('traceback.format_exc():\n%s' % traceback.format_exc())
#


while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        # print(request.decode())
        request = request.decode().split(' ')
        if len(request) > 1:
            method = request[0]
            src = request[1]
            print(src)
        else:
            continue

        if method == 'GET':
            if src == '/index.html':
                conn.sendall(index_content.encode(encoding='UTF-8'))
            elif src == '/client.js':
                conn.sendall(js_content.encode(encoding='UTF-8'))
            elif src == '/background.png':
                conn.sendall(background_content)
            elif src == '/blackStone.png':
                conn.sendall(blackStone_content)
            elif src == '/whiteStone.png':
                conn.sendall(whiteStone_content)
            elif src == '/favicon.ico':
                conn.sendall(favicon_content)
        conn.close()
    except KeyboardInterrupt:
        break



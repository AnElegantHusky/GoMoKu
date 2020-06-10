import socket


# init socket
HOST = "0.0.0.0"
PORT = 6790

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(128)

# handle http requests
while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        data = request.decode().split(' ')
        if len(data) > 1:
            method = data[0]
            src = data[1]
            print(addr[0]+':'+str(addr[1])+'-->'+src)
        else:
            continue

        if method == 'GET':
            try:
                # handle image resources
                if src[-4:] == ".png" or src[-4:] == ".ico":
                    f = open(src[1:], 'rb')
                    conn.send("HTTP/1.0 200 OK\r\n".encode())
                    conn.send("Content-Type:image/{}\r\n".format(src[-3:]).encode())
                    conn.send("\r\n".encode())
                    while 1:
                        data = f.read(1024)
                        if not data:
                            break
                        conn.send(data)
                    f.close()
                # handle text resources
                elif src[-5:] == ".html" or src[-3:] == ".js":
                    f = open(src[1:], "r")
                    outputstr = f.readlines()
                    outputdata = [line.encode() for line in outputstr]
                    conn.send("HTTP/1.0 200 OK\r\n".encode())
                    if src[-3:] == ".js":
                        content_type = "Content-Type:text/javascript\r\n"
                    else:
                        content_type = "Content-Type:text/html\r\n"
                    conn.send(content_type.encode())
                    conn.send("\r\n".encode())
                    for data in outputdata:
                        conn.send(data)
                    f.close()
            except FileNotFoundError:
                print("file not found")
                conn.send("HTTP/1.0 404 Not Found\r\n".encode())
                continue
            finally:
                conn.close()
    except KeyboardInterrupt:
        break

s.shutdown(2)
s.close()
# print(HOST+':'+str(PORT))
# f = open('client.js', 'r+')
# f.seek(16, 0)
# f.write(HOST+':'+str(PORT)+'"\n')
# f.close()

# header = "HTTP/1.x 200 OK\r\n\r\n"
# # index.html
# index_content = '''
# HTTP/1.x 200 OK
# Content-Type: text/html
#
# '''
# f = open('index.html', 'r')
# index_content = index_content + f.read()
# f.close()
#
# # client.js
# js_content = '''
# HTTP/1.x 200 OK
# Content-Type: text/javascript
#
# '''
# f = open('client.js', 'r')
# # add_line = 'var url = "ws://'+HOST+":"+str(PORT)+'"\n'
# # js_content = js_content + add_line + f.read()
# js_content = header + f.read()
# f.close()
#
# # pic
# background_content = '''
# HTTP/1.x 200 OK
# Content-Type: image/png
#
# '''
# f = open('background.png', 'rb')
# background_content = header.encode(encoding='UTF-8') + f.read()
# f.close()
#
# blackStone_content = '''
# HTTP/1.x 200 OK
# Content-Type: image/png
#
# '''
# f = open('blackStone.png', 'rb')
# blackStone_content = header.encode(encoding='UTF-8') + f.read()
# f.close()
#
# whiteStone_content = '''
# HTTP/1.x 200 OK
# Content-Type: image/png
#
# '''
# f = open('whiteStone.png', 'rb')
# whiteStone_content = header.encode(encoding='UTF-8') + f.read()
# f.close()
#
# favicon_content = '''
# HTTP/1.x 200 OK
# Content-Type: image/ico
#
# '''
# f = open('favicon.ico', 'rb')
# favicon_content = header.encode(encoding='UTF-8') + f.read()
# f.close()


# while True:
#     try:
#         conn, addr = s.accept()
#         request = conn.recv(1024)
#         data = request.decode().split(' ')
#         # request = request.decode().split(' ')
#         if len(data) > 1:
#             method = data[0]
#             src = data[1]
#             # print(conn)
#             print(addr[0]+':'+str(addr[1])+'-->'+src)
#             # print(request.decode())
#         else:
#             continue
#
#         if method == 'GET':
#             if src == '/index.html':
#                 f = open('index.html', "rb")
#                 conn.send("HTTP/1.0 200 OK\r\n".encode())
#                 conn.send("Content-Type:text/html\r\n".encode())
#                 conn.send("\r\n".encode())
#                 while 1:
#                     data = f.read(1024)
#                     if not data:
#                         break
#                     conn.send(data)
#                 f.close()
#             elif src == '/client.js':
#                 f = open('client.js', "rb")
#                 conn.send("HTTP/1.0 200 OK\r\n".encode())
#                 conn.send("Content-Type:text/javascript\r\n".encode())
#                 conn.send("\r\n".encode())
#                 while 1:
#                     data = f.read(1024)
#                     if not data:
#                         break
#                     conn.send(data)
#                 f.close()
#             elif src == '/background.png':
#                 conn.sendall(background_content)
#             elif src == '/blackStone.png':
#                 conn.sendall(blackStone_content)
#             elif src == '/whiteStone.png':
#                 conn.sendall(whiteStone_content)
#             elif src == '/favicon.ico':
#                 conn.sendall(favicon_content)
#             else:
#                 header = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
#                 conn.send(header.encode())
#         conn.close()
#     except KeyboardInterrupt:
#         break




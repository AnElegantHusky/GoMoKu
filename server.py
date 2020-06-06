import socket


HOST = "0.0.0.0"
PORT = 6790
print(HOST+':'+str(PORT))
# f = open('client.js', 'r+')
# f.seek(16, 0)
# f.write(HOST+':'+str(PORT)+'"\n')
# f.close()

header = "HTTP/1.x 200 OK\r\n\r\n"
# index.html
index_content = '''
HTTP/1.x 200 OK
Content-Type: text/html

'''
f = open('index.html', 'r')
index_content = header + f.read()
f.close()

# client.js
js_content = '''
HTTP/1.x 200 OK 
Content-Type: text/javascript

'''
f = open('client.js', 'r')
# add_line = 'var url = "ws://'+HOST+":"+str(PORT)+'"\n'
# js_content = js_content + add_line + f.read()
js_content = header + f.read()
f.close()

# pic
background_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('background.png', 'rb')
background_content = header.encode(encoding='UTF-8') + f.read()
f.close()

blackStone_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('blackStone.png', 'rb')
blackStone_content = header.encode(encoding='UTF-8') + f.read()
f.close()

whiteStone_content = '''
HTTP/1.x 200 OK 
Content-Type: image/png

'''
f = open('whiteStone.png', 'rb')
whiteStone_content = header.encode(encoding='UTF-8') + f.read()
f.close()

favicon_content = '''
HTTP/1.x 200 OK 
Content-Type: image/ico

'''
f = open('favicon.ico', 'rb')
favicon_content = header.encode(encoding='UTF-8') + f.read()
f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        data = request.decode().split(' ')
        # request = request.decode().split(' ')
        if len(data) > 1:
            method = data[0]
            src = data[1]
            # print(conn)
            print(addr+'-->'+src)
            # print(request.decode())
        else:
            continue

        if method == 'GET':
            if src == '/index.html':
                print("src == /index.html")
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
            else:
                header = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
                conn.send(header.encode())
        conn.close()
    except KeyboardInterrupt:
        break



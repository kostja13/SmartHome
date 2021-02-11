import socket
import sqlite3
import json
import os
import time


conn = sqlite3.connect('./sqlite/sqlite.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

SERVER_ADDRESS = (HOST, PORT) = '', 80
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    request = client_connection.recv(1024)
    request = request.decode('utf-8')
    header = request.split('\r\n')[0]
    print(header)
    if len(header) == 0:
        return
    if "HTTP/1.1" not in header:
        return
    if header.split()[1] =="/test" and header.split()[0]=="GET":
        print("test")
        http_message = b"""\
test
"""
############

    elif "history" in header.split()[1] and header.split()[0]=="GET":
        id =0
        try:
            uri = header.split()[1].split('/')
            print(uri)
            if uri[2] == 'id':
                id = int(uri[3])
        except:
            id = -1
        
        if id > 0:
            query = '''
    SELECT vtime, value from sensordata WHERE id = %d
    ''' % (id)
            sensordata = c.execute(query).fetchall()
            conn.commit()
            if len(sensordata) == 0:
                notFound(client_connection)
                return
            http_message = json.dumps( [dict(ix) for ix in sensordata] )
            #http_message = json.dumps(sensordata).encode()
            jsonTop = """ 
{\"id\" : %d,
\"values\" :
""" % id
            http_message = (jsonTop + http_message + "}").encode()
        else:    
            notFound(client_connection)
            return

###########

    elif "sensordata" in header.split()[1] and header.split()[0]=="GET":
        id =0
        try:
            uri = header.split()[1].split('/')
            print(uri)
            if uri[2] == 'id':
                id = int(uri[3])
        except:
            id = -1
        
        if id > 0:
            query = '''
    select * from sensordata where vtime = (select max(vtime) from sensordata where id = %d) and id = %d
    ''' % (id,id)
            sensordata = c.execute(query).fetchall()
            conn.commit()
            if len(sensordata) == 0:
                notFound(client_connection)
                return
            http_message = json.dumps( [dict(ix) for ix in sensordata] ).encode()
        else:    
            notFound(client_connection)
            return

###########

    elif "overview" in header.split()[1] and header.split()[0]=="GET":
        query = '''
    select id, name, value, max(vtime) from sensordata group by id;
    '''
        sensordata = c.execute(query).fetchall()
        conn.commit()
        if len(sensordata) == 0:
            notFound(client_connection)
            return
        http_message = json.dumps( [dict(ix) for ix in sensordata] ).encode()

###########




    else:
        notFound(client_connection)
        return

    http_response = b"""\
HTTP/1.1 200 OK
Connection: close
Accept-Ranges: bytes
Content-Length: %d
Content-Type: application/json

""" % (len(http_message))
    http_response+= http_message
    client_connection.sendall(http_response)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))

    while True:
        client_connection, client_address = listen_socket.accept()
        pid = os.fork()
        if pid == 0:  # child
            listen_socket.close()  # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)  # child exits here
        else:  # parent
            client_connection.close()  # close parent copy and loop over

def notFound(client_connection):
    http_response = b"""\
HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: 36
Connection: close

Oh oh, da ist etwas schief gelaufen.
"""
    client_connection.sendall(http_response)
    print("404")
    return

if __name__ == '__main__':
    serve_forever()

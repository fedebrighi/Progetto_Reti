from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def incoming_connections():
    while True:
            client, client_address = SERVER.accept()
            print("%s:%s connected." % client_address)
            client.send(bytes("Please enter your name:", "utf8"))
            addresses[client] = client_address
            Thread(target=handling_client, args=(client,)).start()

def handling_client(client):
    
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you want to leave the chat type {quit}' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast_messages(bytes(msg, "utf8"))
        clients[client] = name
        try:
            while True:
                msg = client.recv(BUFSIZ)
                if msg != bytes("{quit}", "utf8"):
                    broadcast_messages(msg, name+": ")
                else:
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del clients[client]
                    broadcast_messages(bytes("%s has left the chat." % name, "utf8"))
                    handle_client_disconnect(client)
                    break
        except ConnectionResetError:
            handle_client_disconnect(client)
            
def handle_client_disconnect(client):
    name = clients.get(client)
    client_address = addresses.get(client)
    if name:
        del clients[client]
        ip,port = client_address
        msg = f"{ip}:{port} disconnected from the chat."
        broadcast_messages(bytes(msg, "utf8"))
        print(msg)
    else:
        print("Client disconnected.")


def broadcast_messages(msg, prefix=""): 
    for user in clients:
        user.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 2003
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Server online waiting for connections...")
    ACCEPT_THREAD = Thread(target=incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

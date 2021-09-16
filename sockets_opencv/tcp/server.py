import socket
import cv2
import pickle  # (de)serialize objs
import struct  # handles binary data
import imutils  # img processing

# Creating socket
# AF_NET = IPv4, SOCK_STREAM = TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
print('host name:', host_name)
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)
# Socket Listen
# will support 5 unique connections, the 6th one will be dropped
server_socket.listen(5)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)  # webcam
        while(vid.isOpened()):
            img,frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a))+a
            client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
cv2.destroyAllWindows()

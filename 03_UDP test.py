"""
This code is used to send and receive data through UDP communication between Computer and ESP8266/32

"""

import socket
UDP_TX_IP = "192.168.48.78"                                                        # IP of ESP32/8266
UDP_TX_PORT = 4210                                                                 # PORT of ESP32/8266
MESSAGE = b"RED_CUBE"                                                              # Set message to be transmitted
UDP_RX_IP = "192.168.48.205"                                                       # Computer IP Address
UDP_RX_PORT = 2020                                                                 # Computer PORT
timeout_seconds = 2                                                                # Computer RX Time out


def udp_receive(ip, port, tos=3):                                                   # tos -> Time out seconds
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ip, port))
        server_socket.settimeout(tos)                                               # Set timeout for socket operations
        print(f"\n\nUDP server listening on {ip}:{port}")
        try:
            data, addr = server_socket.recvfrom(1024)
            #print(f"Received message from {addr}: {data.decode()}")
            msg = data.decode()
        except socket.timeout:
            print("No data received within the specified timeout.")
            msg = "TimeOut"
    return msg


if __name__ == "__main__":
    print("UDP target IP: %s   PORT: %s Sending msg.." % (UDP_TX_IP, UDP_TX_PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                            # UDP Socket init transmission
    sock.sendto(MESSAGE, (UDP_TX_IP, UDP_TX_PORT))                                     # Sending msg to UDP port
    rcv = udp_receive(UDP_RX_IP, UDP_RX_PORT, timeout_seconds)                         # Receive msg from UDP
    print(f"Data response : {rcv}")

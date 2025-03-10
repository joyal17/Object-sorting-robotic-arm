
# pip install ultralytics opencv-python cvzone
# it is better to install from package list

from ultralytics import YOLO
import cv2
import cvzone
import math
import socket
import time


cap = cv2.VideoCapture(0)                                                           # For Webcam
cap.set(3, 1280)
cap.set(4, 720)
ESP_UDP_IP = "192.168.54.22"                                                       # Configure Receiver IP Address
ESP_UDP_PORT = 4210                                                                 # Configure PORT number
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                             # UDP Socket initialization


PC_UDP_IP = "192.168.54.3"
PC_UDP_PORT = 2020

msg = ""
msg_d ="ESP 32"
model = YOLO("ShapeColor.pt")
classNames = ['RED_Cylinder', 'RED_Cube', 'RED_Prisam', 'BLUE_Cube', 'BLUE_Prisam', 'BLUE_Cylinder', 'GREEN_prisam', 'GREEN_Cube', 'GREEN_Cylinder']

pt3 = ot3 = time.time() * 1000.0
pt2 = ot2 = time.time() * 1000.0
pt1 = ot1 = time.time() * 1000.0
pt = ot = time.time() * 1000.0

font_face = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
text = "Robotic color sorting"
text_color = (255, 0, 0)
text_color1 = (0, 255, 0)


def SendDataToEsp32(comand):
    MESSAGE = comand.encode('utf-8')
    print(f"Our System Detected {comand} processing request")
    sock.sendto(MESSAGE, (ESP_UDP_IP, ESP_UDP_PORT))
    udp_receive(PC_UDP_IP, PC_UDP_PORT, 1)


def udp_receive(ip, port, tos=1):                                                   # tos -> Time out seconds
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ip, port))
        server_socket.settimeout(tos)                                               # Set timeout for socket operations
        print(f"\n\nUDP server listening on {ip}:{port}")
        try:
            data, addr = server_socket.recvfrom(1024)
            print(f"Received message from {addr}: {data.decode()}")
            msg_d = data.decode()
        except socket.timeout:
            print("No data received within the specified timeout.")
            msg_d = "TimeOut"
    return msg_d


text = "Robotic Color Sorting Waiting For Shape"
x = 0
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    pt1 = time.time() * 1000.0
    pt2 = time.time() * 1000.0
    pt3 = time.time() * 1000.0
    if (pt1 - ot1) > 2000:
        ot1 = pt1
        text = "Shape Recognition System Initilizing....."
    if (pt2 - ot2) > 15000:
        ot2 = pt2
        ot = pt2
        text = "Shape Recognition System reset"
        x = 0
    if (pt3 - ot3) > 1000:
        ot3 = pt3
        x = x + 1
    results = model(img, stream=True)
    position = (10, img.shape[0] - 10)
    position1 = (10, img.shape[0] - 50)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            msg = classNames[cls] + "  cls = " + str(cls) + "  "
            pt = time.time() * 1000.0
            if (pt - ot) > 15000:
                ot = pt
                ot1 = pt
                ot2 = pt
                x = 0
                print(f"                                 DB ReFresh {cls}")
                SendDataToEsp32(classNames[cls])
                msg = classNames[cls] + "  HARDWARE UPDATE please Wait"
                text = "  HARDWARE UPDATE please Wait"
            cvzone.putTextRect(img, f'{msg} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
            if (pt - ot) > 3000 and (pt - ot) < 5000:
                text = msg + " Establishing network Connection.."
            if (pt - ot) > 4000 and (pt - ot) < 8000:
                text = msg + "Testing Hardware"
                ot1 = pt
            if (pt - ot) > 8000 and (pt - ot) < 11000:
                text = msg + "Preparing data to send.."
                ot1 = pt
            if (pt - ot) > 11000 and (pt - ot) < 14000:
                text = msg + "Sending update Please Wait..."
                ot1 = pt
            if (pt - ot) > 14000 and (pt - ot) < 15000:
                text = msg + "Sending COMMAND to HARDWARE"
                ot1 = pt

    cv2.putText(img, text, position, font_face, font_scale, text_color, font_thickness)
    cv2.putText(img, str(x), position1, font_face, font_scale, text_color1, font_thickness)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

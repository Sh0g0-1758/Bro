# This is an abstraction for the normal user which sends SYN requests to the server after every one minute and waits for a response.

from scapy.all import *
import time

def send_syn_and_receive_response(ip, port):
    syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
    
    print(f"Sending SYN request to {ip}:{port}")
    
    response = sr1(syn_packet, timeout=1)
    print(response)
    
    if response:
        if response.haslayer(TCP) and response[TCP].flags == 0x12:
            print("Received SYN-ACK response")
        elif response.haslayer(TCP) and response[TCP].flags == 0x14:
            print("Received RST response (port closed)")
        else:
            print("Received unexpected response:")
            response.show()
    else:
        print("No response received")

if __name__ == "__main__":
    target_ip = "10.81.92.228"
    target_port = 42142

    for i in range(5):
        send_syn_and_receive_response(target_ip, target_port)
        time.sleep(60)

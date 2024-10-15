# This is an abstraction for the malicious user which sends SYN requests to the server relentlessly to see which ports are open. 

import subprocess
import signal
import os
from scapy.all import sniff, TCP, IP
from datetime import datetime

processes = []
log_file = "tcp_conn.log"
opened_ports = []

def open_ports():
    print("Opening ports...")

    for i in range(42100, 42200, 2):
        command = f"netcat -vlp {i}"
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        processes.append(process)
        opened_ports.append(i)
        print(f"Port {i} opened.")

def close_ports():
    print("\nClosing all ports...")
    for process in processes:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print(f"Port {process.args.split()[-1]} closed.")
        except Exception as e:
            print(f"Error closing port: {e}")
    print("All ports closed.")

def log_tcp_packet(pkt):
    if pkt.haslayer(TCP):
        dst_port = pkt[TCP].dport

        if dst_port in opened_ports:
            src_ip = pkt[IP].src
            src_port = pkt[TCP].sport
            dst_ip = pkt[IP].dst
            flags = pkt.sprintf("%TCP.flags%")

            with open('data.txt', 'a') as f:
                f.write(f"{src_ip} {src_port} {dst_ip} {dst_port} {flags}\n")

            print(f"Logged TCP request: {src_ip}:{src_port} -> {dst_ip}:{dst_port}, Flags: {flags}")

def start_sniffing():
    print("Starting to sniff for TCP requests...")
    sniff(filter="tcp", prn=log_tcp_packet, store=0)

if __name__ == "__main__":
    open_ports()

    try:
        from threading import Thread
        sniff_thread = Thread(target=start_sniffing)
        sniff_thread.start()
        with open('data.txt', 'w') as f:
                f.write(f"src_ip src_port dst_ip dst_port flags\n")
        while True:
            user_input = input("Type 'exit' to close all ports: ")
            if user_input.strip().lower() == 'exit':
                break
    except KeyboardInterrupt:
        pass
    finally:
        close_ports()

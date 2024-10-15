# We give the abstraction of having a router by making a system that has multiple ports open
# To do that, we utilize the netcat command and open 50 ports between 42100 and 42200. 

import subprocess
import signal
import os

processes = []

def open_ports():
    print("Opening ports...")

    for i in range(42100, 42200, 2):
        command = f"netcat -vlp {i}"
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        processes.append(process)

def close_ports():
    print("\nClosing all ports...")
    for process in processes:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print(f"Port {process.args.split()[-1]} closed.")
        except Exception as e:
            print(f"Error closing port: {e}")
    print("All ports closed.")

if __name__ == "__main__":
    open_ports()

    try:
        while True:
            user_input = input("Type 'exit' to close all ports: ")
            if user_input.strip().lower() == 'exit':
                break
    except KeyboardInterrupt:
        pass
    finally:
        close_ports()

from collections import defaultdict
import pandas as pd

class Bro:
    def __init__(self, threshold):
        self.T = threshold
        
        # self.good_services is the list of port numbers to which successful connections 
        #     (SYN and ACK) should not be tracked
        self.good_services = [80, 22, 23, 25, 113, 20, 70]
        
        # self.tracked maps sending hosts to a set of destination addresses
        #     from tracked connection attempts
        self.tracked = defaultdict(list)

    def block_connection(self, host_ip):
        if host_ip in self.tracked:
            if len(self.tracked[host_ip]) >= self.T:
                return True
        return False
    
    def process_flow(self, netflow_record):
        i = netflow_record
        if i['dst_port'] not in self.good_services:
            self.tracked[i['src_ip']].append(i['dst_ip'])
            
        if i['dst_port'] in self.good_services and 'S' in i['flags'] and 'A' not in i['flags']:
            self.tracked[i['src_ip']].append(i['dst_ip'])

def run_bro(threshold,netflow_data):
    blocked_hosts = set()
    bro = Bro(threshold)
    for _,flow in enumerate(netflow_data):
        src_ip = flow["src_ip"]
        block = bro.block_connection(src_ip)
        if block:
            blocked_hosts.add(src_ip)
            continue
        bro.process_flow(flow)

    return blocked_hosts

def main():
    threshold = 5
    netflow_data = pd.read_csv('netflow.csv').to_dict('records')
    blocked_hosts = run_bro(threshold,netflow_data)
    print("Blocked hosts: ", blocked_hosts)

if __name__ == "__main__":
    main()
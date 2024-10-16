import subprocess
import os
import time

# Start server.py
server_command = "python server.py"
server_process = subprocess.Popen(server_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
print("Server started.")

# Track time to write to the file every 5 minutes
start_time = time.time()

while True:
    # Run txt_to_csv.py
    txt_to_csv_command = "python txt_to_csv.py"
    txt_to_csv_process = subprocess.Popen(txt_to_csv_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    txt_to_csv_process.wait()  # Wait for txt_to_csv.py to complete
    print("Data stored as CSV!")
    
    # Run bro_algo.py
    bro_algo_command = "python bro_algo.py"
    bro_algo_process = subprocess.Popen(bro_algo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    
    # Capture the output (stdout and stderr) from bro_algo.py
    stdout, stderr = bro_algo_process.communicate()
    
    # Print the output from bro_algo.py
    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())
    
    bro_algo_process.wait()  # Wait for bro_algo.py to finish

    # Check if 5 minutes have passed
    if time.time() - start_time >= 10:
        # Write to the data.txt file
        with open('data.txt', 'w') as f:
            f.write("src_ip src_port dst_ip dst_port flags\n")
        print("All Blocked Hosts are Released after the time window of 10 seconds.")
        
        # Reset the start time for the next 10 seconds interval
        start_time = time.time()
    
    # Sleep for 5 seconds before the next iteration
    time.sleep(5)

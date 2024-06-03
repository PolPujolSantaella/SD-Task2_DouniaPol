import subprocess
import time
import os


data_storage_script = os.path.join('decentralized', 'dataDestorage.py')
node_slave0_script = os.path.join('decentralized', 'node0.py')
node_slave1_script = os.path.join('decentralized', 'node1.py')
node_slave2_script = os.path.join('decentralized', 'node2.py')

processes = []

def start_process(script_path):
    process = subprocess.Popen(['python3', script_path])
    processes.append(process)
    time.sleep(2)
    return process

try:
    server_process = start_process(data_storage_script)
    slave0_process = start_process(node_slave0_script)
    slave1_process = start_process(node_slave1_script)
    slave2_process = start_process(node_slave2_script)

    for process in processes:
        process.wait()
except KeyboardInterrupt:
    print("Terminating processes...")
    for process in processes:
        process.terminate()
        process.wait()
    print("All processes terminated")

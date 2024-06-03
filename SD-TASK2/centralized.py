import subprocess
import time
import os


data_storage_script = os.path.join('centralized', 'dataStorage.py')
node_master_script = os.path.join('centralized', 'node_master.py')
node_slave1_script = os.path.join('centralized', 'node_slave1.py')
node_slave2_script = os.path.join('centralized', 'node_slave2.py')

processes = []


def start_process(script_path):
    process = subprocess.Popen(['python3', script_path])
    processes.append(process)
    time.sleep(2)
    return process

try:
    server_process = start_process(data_storage_script)
    master_process = start_process(node_master_script)
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

import signal
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../proto')
sys.path.append(os.getcwd())

import unittest
import subprocess
import grpc
import time
from threading import Thread
import yaml
import logging
import random
import concurrent.futures
import store_pb2, store_pb2_grpc
from tabulate import tabulate


def perform_operations(args):
    
    operations_per_process = args[0]
    master_ip = args[1]
    master_port = args[2]
    slave_configs = args[3]
    
    master_channel = grpc.insecure_channel(
        f"{master_ip}:{master_port}",
        options=[
            ("grpc.max_send_message_length", -1),
            ("grpc.max_receive_message_length", -1),
            ("grpc.so_reuseport", 1),
            ("grpc.use_local_subchannel_pool", 1),
        ],
    )
    
    master_stub = store_pb2_grpc.KeyValueStoreStub(master_channel)
    slave_channels = [ ]
    slave_stubs = [ ]
    for slave_id, slave in enumerate(slave_configs):
        slave_ip = slave["ip"]
        slave_port = slave["port"]
        slave_channel = grpc.insecure_channel(
                                        f"{slave_ip}:{slave_port}",
                                        options=[
                                            ("grpc.max_send_message_length", -1),
                                            ("grpc.max_receive_message_length", -1),
                                            ("grpc.so_reuseport", 1),
                                            ("grpc.use_local_subchannel_pool", 1),
                                        ],
                                    )
        slave_channels.append(slave_channel)
        slave_stubs.append(store_pb2_grpc.KeyValueStoreStub(slave_channel))
    
    ops = 0
    for _ in range(operations_per_process):
        
        try:
            master_stub.put(store_pb2.PutRequest(key="perf_key", value="perf_value"))
            ops += 1
            random.choice(slave_stubs).get(store_pb2.GetRequest(key="perf_key"))
            ops += 1
            
        except Exception as e:
            print(e)
    
    return ops

class TestCentralizedSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures by starting the gRPC server and connecting to it."""
        self.logger = self.setup_logger()
        self.config = self.load_config()
        self.server_process = self.start_grpc_server()
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])
        self.channels_get, self.stubs_slaves = self.connect_to_grpc_servers(self.config['slaves'])
        self.stubs_get = self.stubs_slaves + [self.stub_put]

    def setup_logger(self):
        """Configure and return a logger for the test."""
        logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        return logger

    def load_config(self):
        """Load configuration from a YAML file."""
        config_path = os.path.join('centralized_config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def start_grpc_server(self):
        """Start the gRPC server as a subprocess."""
        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        server_script_path = os.path.join(project_dir, 'centralized.py')
        server_process = subprocess.Popen([sys.executable, server_script_path])
        time.sleep(2)
        return server_process

    def connect_to_grpc_server(self, ip, port):
        """Create and return a gRPC channel and stub for the specified node."""
        channel_address = f"{ip}:{port}"
        channel = grpc.insecure_channel(channel_address)
        if not self.wait_for_server(channel):
            self.logger.error(f"The gRPC server ({channel_address}) is not available after the timeout.")
            raise Exception(f"Failed to connect to the gRPC server ({channel_address}).")
        return channel, store_pb2_grpc.KeyValueStoreStub(channel)

    def connect_to_grpc_servers(self, slave_configs):
        """Create and return gRPC channels and stubs for the specified nodes."""
        channels = []
        stubs = []
        for slave in slave_configs:
            channel_address = f"{slave['ip']}:{slave['port']}"
            channel = grpc.insecure_channel(channel_address)
            if not self.wait_for_server(channel):
                self.logger.error(f"The gRPC server ({channel_address}) is not available after the timeout.")
                raise Exception(f"Failed to connect to the gRPC server ({channel_address}).")
            channels.append(channel)
            stubs.append(store_pb2_grpc.KeyValueStoreStub(channel)) 
        
        return channels, stubs
    

    def tearDown(self):
        """Tear down test fixtures by stopping the server and closing the channels."""
        self.close_grpc_channel(self.channel_put)
        self.close_grpc_channels(self.channels_get)
        self.stop_grpc_server()

    def close_grpc_channel(self, channel):
        """Close the gRPC channel."""
        channel.close()

    def close_grpc_channels(self, channels):
        """Close the gRPC channels."""
        for channel in channels:
            channel.close()

    def stop_grpc_server(self):
        """Stop the gRPC server process."""
        
        try:
            os.kill(self.server_process.pid, signal.SIGTERM)
        except OSError:
            print("OS error")
            pass
            
        self.server_process.wait()

    def wait_for_server(self, channel, timeout=15):
        """Wait until the server is available or the timeout is reached."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                grpc.channel_ready_future(channel).result(timeout=1)
                return True
            except grpc.FutureTimeoutError:
                continue
        return False

    def test_put_success(self):
        """Test that a successful put operation correctly updates the data."""
        self.logger.info("Testing put success...")
        args = store_pb2.PutRequest(key="test_key", value="test_value")
        response = self.stub_put.put(args)
        self.assertTrue(response.success)

    def test_get_correctness(self):
        """Ensure get retrieves the correct value for a given key."""
        self.logger.info("Testing get correctness...")
        self.stub_put.put(store_pb2.PutRequest(key="test_key", value="test_value"))
        response = random.choice(self.stubs_get).get(store_pb2.GetRequest(key="test_key"))
        self.assertEqual(response.value, "test_value")

    def test_concurrent_access(self):
        """Test handling of concurrent put and get requests."""
        self.logger.info("Testing concurrent access...")
        def worker(key, value, index):
            try:
                for _ in range(10):
                    self.stub_put.put(store_pb2.PutRequest(key=key, value=value))
                    time.sleep(0.1)  # Simulate time delay between operations
                    response = random.choice(self.stubs_get).get(store_pb2.GetRequest(key=key))
                    self.assertEqual(response.value, f'value{index}', f"Unexpected value for key '{key}': expected 'value{index}' but got '{response.value}'")
            except Exception as e:
                self.fail(f"Error occurred: {e}")

        threads = []
        for i in range(2):  # Two threads simulating different clients
            t = Thread(target=worker, args=(f'key{i}', f'value{i}', i))
            t.start()
            threads.append(t)

        for t in threads:
            t.join(timeout=30)

        for i in range(2):
            response = random.choice(self.stubs_get).get(store_pb2.GetRequest(key=f'key{i}'))
            self.assertEqual(response.value, f'value{i}', f"Unexpected value for key 'key{i}': expected 'value{i}' but got '{response.value}'")

    def test_system_scalability_and_performance(self):
        """Test the system's scalability and performance by simulating high concurrent access."""
        self.logger.info("Testing system scalability and performance...")

        start_time = time.time()
        process_count = 10
        operations_per_process = 20
        
        self.close_grpc_channel(self.channel_put)
        self.close_grpc_channels(self.channels_get)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(perform_operations, 
                                       (
                                           operations_per_process,
                                            self.config['master']['ip'],
                                            self.config['master']['port'],
                                            self.config['slaves']
                                       )
                                       )
                                       for _ in range(process_count)]
            
            concurrent.futures.wait(futures)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Performed {sum([ f.result() for f in futures])} operations in {duration:.2f} seconds.")
        
        assert duration < 10, "The system took too long to perform the operations."
        
    def test_system_scalability_and_performance_with_slowdown_slave(self):

        """Test the system's scalability and performance by simulating high concurrent access (with a partitioned slave)."""
        self.logger.info("Testing system scalability and performance with slowed slave...")
        
        
        self.channels_get, self.stubs_slaves = self.connect_to_grpc_servers(self.config['slaves'])
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])
        
        slowdown_request = store_pb2.SlowDownRequest(seconds=1)
        stub_slave_id = random.choice(range(len(self.stubs_slaves)))
        stub_slave = self.stubs_slaves[stub_slave_id]
        slowdown_resp = stub_slave.slowDown(slowdown_request)
        assert slowdown_resp.success, "Failed to slow down slave."
        
        start_time = time.time()
        process_count = 10
        operations_per_process = 20

        self.close_grpc_channel(self.channel_put)
        self.close_grpc_channels(self.channels_get)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(perform_operations, 
                                       (
                                           operations_per_process,
                                            self.config['master']['ip'],
                                            self.config['master']['port'],
                                            self.config['slaves']
                                       )
                                       )
                                       for _ in range(process_count)]
            
            concurrent.futures.wait(futures)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Performed {sum([f.result() for f in futures])} operations in {duration:.2f} seconds (slowing down master).")
        
        # Restore
        self.channels_get, self.stubs_slaves = self.connect_to_grpc_servers(self.config['slaves'])
        restore_request = store_pb2.RestoreRequest()
        stub_slave = self.stubs_slaves[stub_slave_id]
        restore_resp = stub_slave.restore(restore_request)
        assert restore_resp.success, "Failed to restore slave."

        assert duration < 10, "The system took too long to perform the operations."
        
    def test_system_scalability_and_performance_with_slowdown_master(self):

        """Test the system's scalability and performance by simulating high concurrent access (with a partitioned master)."""
        self.logger.info("Testing system scalability and performance with slowed master...")
        
        
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])
        
        # Slow down 
        slowdown_request = store_pb2.SlowDownRequest(seconds=1)
        slowdown_resp = self.stub_put.slowDown(slowdown_request)
        assert slowdown_resp.success, "Failed to slow down master."
        
        start_time = time.time()
        process_count = 10
        operations_per_process = 20

        self.close_grpc_channel(self.channel_put)
        self.close_grpc_channels(self.channels_get)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(perform_operations, 
                                       (
                                           operations_per_process,
                                            self.config['master']['ip'],
                                            self.config['master']['port'],
                                            self.config['slaves']
                                       )
                                       )
                                       for _ in range(process_count)]
            
            concurrent.futures.wait(futures)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Performed {process_count * operations_per_process * 2} operations in {duration:.2f} seconds (slowing down master).")
        
        # Restore
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])

        restore_request = store_pb2.RestoreRequest()
        restore_resp = self.stub_put.restore(restore_request)
        assert restore_resp.success, "Failed to restore master."

        assert duration < 10, "The system took too long to perform the operations."

    def test_state_recovery_after_critical_failure(self):
        """Test the system's ability to recover state after a critical failure."""

        self.logger.info("Testing state recovery after critical failure...")

        self.stub_put.put(store_pb2.PutRequest(key="stable_key", value="stable_value"))

        self.stop_grpc_server()
        time.sleep(5)
        self.server_process = self.start_grpc_server()
        time.sleep(5)
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])
        self.channels_get, self.stubs_get = self.connect_to_grpc_servers(self.config['slaves'])
        response = random.choice(self.stubs_get).get(store_pb2.GetRequest(key="stable_key"))
        self.assertEqual(response.value, "stable_value", "Data did not recover correctly after critical failure.")

    def test_node_failure_during_transaction(self):
        """Simulate node failure during a transaction and check for system consistency."""

        self.logger.info("Testing node failure during transaction...")

        
        response = self.stub_put.put(store_pb2.PutRequest(key="initial_key", value="initial_value"))
        self.assertTrue(response.success, "Initial put failed unexpectedly.")

        self.stop_grpc_server()
        time.sleep(1)
        self.server_process = self.start_grpc_server()
        self.channel_put, self.stub_put = self.connect_to_grpc_server(self.config['master']['ip'], self.config['master']['port'])
        self.channels_get, self.stubs_get = self.connect_to_grpc_servers(self.config['slaves'])

        try:
            recovery_response = self.stub_put.put(store_pb2.PutRequest(key="recovery_key", value="recovery_value"))
            self.assertTrue(recovery_response.success, "Recovery put failed after node failure.")
            response = random.choice(self.stubs_get).get(store_pb2.GetRequest(key="recovery_key"))
            self.assertEqual(response.value, "recovery_value", "Data was not correctly recovered.")
        except grpc.RpcError as e:
            self.fail(f"Operation failed after node recovery: {str(e)}")


if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult, verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCentralizedSystem)
    results = runner.run(suite)

    table = []
    for case, reason in results.failures + results.errors:
        status = 'FAIL' if (case, reason) in results.failures else 'ERROR'
        row = [case.id().split('.')[-1], status, reason]
        table.append(row)
    
    if results.testsRun:
        passed = results.testsRun - len(results.failures) - len(results.errors)
        table.append(["Total", "PASSED", f"{passed}/{results.testsRun}"])
    
    print("\nCentralized Test Results Summary:")
    print(tabulate(table, headers=["Test Case", "Result", "Details"], tablefmt="pretty"))

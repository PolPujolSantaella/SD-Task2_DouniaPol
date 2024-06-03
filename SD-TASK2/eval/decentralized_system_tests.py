import signal
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../proto')
sys.path.append(os.getcwd())

import random
import unittest
import subprocess
import grpc
import time
from threading import Thread
import yaml
import logging
import concurrent.futures
import store_pb2, store_pb2_grpc
from tabulate import tabulate

def perform_operations(args):
    
    operations_per_process = args[0]
    node_configs = args[1]
    
    channels = [ ]
    stubs = [ ]
    for node_id, node in enumerate(node_configs):
        node_ip = node["ip"]
        node_port = node["port"]
        node_channel = grpc.insecure_channel(
                                        f"{node_ip}:{node_port}",
                                        options=[
                                            ("grpc.max_send_message_length", -1),
                                            ("grpc.max_receive_message_length", -1),
                                            ("grpc.so_reuseport", 1),
                                            ("grpc.use_local_subchannel_pool", 1),
                                        ],
                                    )
        channels.append(node_channel)
        stubs.append(store_pb2_grpc.KeyValueStoreStub(node_channel))
    
    ops = 0
    for _ in range(operations_per_process):
        
        stub1 = random.choice(stubs)
        stub2 = random.choice(stubs)
        
        try:
            stub1.put(store_pb2.PutRequest(key="perf_key", value="perf_value"))
            ops += 1
            stub2.get(store_pb2.GetRequest(key="perf_key"))
            ops += 1
            
        except Exception as e:
            print(e)
    
    return ops

class TestDecentralizedSystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures by starting the gRPC server and connecting to it."""
        self.logger = self.setup_logger()
        self.config = self.load_config()
        self.server_process = self.start_grpc_server()
        self.channel, self.stub = self.connect_to_grpc_server()

    def setup_logger(self):
        """Configure and return a logger for the test."""
        logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def load_config(self):
        """Load configuration from a YAML file."""
        config_path = os.path.join('decentralized_config.yaml')
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def start_grpc_server(self):
        """Start the gRPC server as a subprocess."""
        server_script_path = os.path.join('decentralized.py')
        server_process = subprocess.Popen(
            [sys.executable, server_script_path]
        )
        return server_process

    def connect_to_grpc_server(self):
        """Create and return a gRPC channel and stub."""
        node = random.choice(self.config['nodes'])
        channel_address = f"{node['ip']}:{node['port']}"
        channel = grpc.insecure_channel(channel_address)
        if not self.wait_for_server(channel):
            self.logger.error("The gRPC server is not available after the timeout.")
            raise Exception("Failed to connect to the gRPC server.")
        return channel, store_pb2_grpc.KeyValueStoreStub(channel)

    def tearDown(self):
        """Tear down test fixtures by stopping the server and closing the channel."""
        self.close_grpc_channel()
        self.stop_grpc_server()
        
    def close_grpc_channel(self):
        """Close the gRPC channel."""
        self.channel.close()

    def stop_grpc_server(self):
        """"Stop the gRPC server process."""
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
        response = self.stub.put(store_pb2.PutRequest(key="test_key", value="test_value"))
        self.assertTrue(response.success)

    def test_get_correctness(self):
        """Ensure get retrieves the correct value for a given key."""
        self.logger.info("Testing get correctness...")
        self.stub.put(store_pb2.PutRequest(key="test_key", value="test_value"))
        response = self.stub.get(store_pb2.GetRequest(key="test_key"))
        self.assertEqual(response.value, "test_value")

    def test_concurrent_access(self):
        """Test handling of concurrent put and get requests."""
        self.logger.info("Testing concurrent access...")
        def worker(key, value):
            try:
                for _ in range(10):
                    self.stub.put(store_pb2.PutRequest(key=key, value=value))
                    time.sleep(0.2)  # Simulate time delay between operations
                    response = self.stub.get(store_pb2.GetRequest(key=key))
                    
            except Exception as e:
                self.fail(f"Error occurred: {e}")

        threads = []
        for i in range (2):
            t = Thread(target=worker, args=(f'key{i}', f'value{i}'))
            t.start()
            threads.append(t)

        for t in threads:
            t.join(timeout=30)

        for i in range(2):
            response = self.stub.get(store_pb2.GetRequest(key=f'key{i}'))
            self.assertEqual(response.value, f'value{i}')  

    def test_system_scalability_and_performance(self):
        """Test the system's scalability and performance by simulating high concurrent access."""
        self.logger.info("Testing system scalability and performance...")
        
        start_time = time.time()
        process_count = 10
        operations_per_process = 20

        self.close_grpc_channel()
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(perform_operations, 
                                       (
                                           operations_per_process,
                                            self.config['nodes']
                                       )
                                       )
                                       for _ in range(process_count)]
            
            concurrent.futures.wait(futures)
            
        end_time = time.time()
        duration = end_time - start_time
        print(f"Performed {process_count * operations_per_process * 2} operations in {duration:.2f} seconds.")

        self.assertLess(duration, 10, "The system took too long to perform the operations.")

    
    def test_system_scalability_and_performance_with_slowdown(self):
        
        """Test the system's scalability and performance by simulating high concurrent access (with a partitioned node)."""
        self.logger.info("Testing system scalability and performance with slowed node...")
        
        # Slow down 
        self.channel, self.stub = self.connect_to_grpc_server() 
        slowdown_request = store_pb2.SlowDownRequest(seconds=1)
        slowdown_resp = self.stub.slowDown(slowdown_request)
        assert slowdown_resp.success, "Failed to slow down node."
        
        start_time = time.time()
        process_count = 10
        operations_per_process = 20
        
        self.close_grpc_channel()
        
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(perform_operations, 
                                       (
                                           operations_per_process,
                                            self.config['nodes']
                                       )
                                       )
                                       for _ in range(process_count)]
            
            concurrent.futures.wait(futures)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Performed {process_count * operations_per_process * 2} operations in {duration:.2f} seconds (slowing down master).")
        
        # Restore
        self.channel, self.stub = self.connect_to_grpc_server() 
        restore_request = store_pb2.RestoreRequest()
        restore_resp = self.stub.restore(restore_request)
        assert restore_resp.success, "Failed to restore node."

        assert duration < 10, "The system took too long to perform the operations."


    def test_state_recovery_after_critical_failure(self):
        """Test the system's ability to recover state after a critical failure."""
        
        self.channel, self.stub = self.connect_to_grpc_server() 
        
        self.logger.info("Testing state recovery after critical failure...")
        try:
            response_put = self.stub.put(store_pb2.PutRequest(key="stable_key", value="stable_value"))
            if not response_put.success:
                self.fail("Error al realizar el put. La operación no se completó correctamente.")

            self.stop_grpc_server()
            time.sleep(5)
            self.server_process = self.start_grpc_server()
            time.sleep(10)
            self.channel, self.stub = self.connect_to_grpc_server()

            response_get = self.stub.get(store_pb2.GetRequest(key="stable_key"))
            self.assertEqual(response_get.value, "stable_value", "Data did not recover correctly after critical failure.")
        except Exception as e:
            self.logger.exception("Error during state recovery test: %s", str(e))
            self.fail("Error during state recovery test: %s" % str(e))
            
    def test_node_failure_during_transaction(self):
        """Simulate node failure during a transaction and check for system consistency."""
        self.logger.info("Testing node failure during transaction...")
        response = self.stub.put(store_pb2.PutRequest(key="initial_key", value="initial_value"))
        self.assertTrue(response.success, "Initial put failed unexpectedly.")

        self.stop_grpc_server()
        time.sleep(1)
        self.server_process = self.start_grpc_server()
        self.channel, self.stub = self.connect_to_grpc_server()

        try:
            recovery_response = self.stub.put(store_pb2.PutRequest(key="recovery_key", value="recovery_value"))
            self.assertTrue(recovery_response.success, "Recovery put failed after node failure.")
            get_response = self.stub.get(store_pb2.GetRequest(key="recovery_key"))
            self.assertEqual(get_response.value, "recovery_value", "Data was not correctly recovered.")
        except grpc.RpcError as e:
            self.fail(f"Operation failed after node recovery: {str(e)}")


if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=unittest.TestResult, verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecentralizedSystem)
    results = runner.run(suite)

    table = []
    for case, reason in results.failures + results.errors:
        status = 'FAIL' if (case, reason) in results.failures else 'ERROR'
        row = [case.id().split('.')[-1], status, reason]
        table.append(row)
    
    if results.testsRun:
        passed = results.testsRun - len(results.failures) - len(results.errors)
        table.append(["Total", "PASSED", f"{passed}/{results.testsRun}"])
    
    print("\nDecentralized Test Results Summary:")
    print(tabulate(table, headers=["Test Case", "Result", "Details"], tablefmt="pretty"))


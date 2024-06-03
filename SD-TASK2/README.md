# Distributed storage systems and the CAP theorem

```
Project/
│
├── proto/
│   ├── store.proto
│   ├── store_pb2.py
│   └── store_pb2_grpc.py
│
├── centralized_config.yaml
├── decentralized_config.yaml
├── centralized.py
├── decentralized.py
├── eval/
│   ├── test_centralized_system.py
│   └── test_decentralized_system.py
│
└── ...
```

## Directory Structure Explanation

- **proto/**: Contains Protocol Buffer files used for defining gRPC services and messages. Generated Python files (`store_pb2.py` and `store_pb2_grpc.py`) based on `store.proto` should be stored here.

- **centralized_config.yaml and decentralized_config.yaml**: YAML configuration files containing settings for the centralized and decentralized systems.

    - ***Centralized Format***: 

    ```yaml
    master:
      ip: <IP>
      port: <Port>

    slaves:
      - id: <slave_1_ID>
        ip: <slave_1_IP>
        port: <slave_1_Port>
      - id: <slave_2_ID>
        ip: <slave_2_IP>
        port: <slave_2_Port>
      ...
    ```

    - ***Decentralized Format***: 

    ```yaml
    nodes:
      - id: <node_1_ID>
        ip: <node_1_IP>
        port: <node_1_Port>
      - id: <node_2_ID>
        ip: <node_2_IP>
        port: <node_2_Port>
      ...
    ```

- **eval/**: Directory containing evaluation scripts and tests.

  - **test_centralized_system.py**: Script containing unit tests for the centralized system.
  
  - **test_decentralized_system.py**: Script containing unit tests for the decentralized system.

Each component of the project is organized into its respective directory, facilitating clear separation of concerns and ease of navigation. The `eval` directory specifically houses test scripts for evaluating the functionality and correctness of the implemented systems.

> **Note:** Students are required to define the necessary stubs for implementing the Two Phase Commit (2PC) protocol and for node registration in the system. These stubs must be manually added to the store.proto file by the students as part of their implementation.

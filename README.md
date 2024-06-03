# SD-Task2_DouniaPol
# Execució del .proto i Proves del Sistema

Aquest document proporciona instruccions sobre com executar el protocol definit a `store.proto` i les proves del sistema per a les implementacions centralitzades i descentralitzades.

## Execució del .proto

El protocol definit a `store.proto` proporciona una API de client per interactuar amb els sistemes d'emmagatzematge distribuït de clau-valor. Per utilitzar aquest protocol, segueix aquestes instruccions:

1. **Compilació del .proto**:
   
   Utilitza el compilador de protobuf per generar els fitxers Python a partir del fitxer `store.proto`. Executa aquesta comanda:

   ```bash
   python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. store.proto

## Execucio testos
python3 eval/centralized_system_test.py
python3 eval/decentralized_system_test.py
python eval/eval.py



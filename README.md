# Project: Understand Blockchain with BikeChain

## Introduction

This three days project is a collaborative effort by six individuals who completed the capped course on understanding blockchain. The project aims to apply the knowledge gained during the course and provide a practical demonstration of blockchain concepts with an example of a BikeChain. BikeChain is a blockchain designed for selling bikes and two-wheelers, maintaining the history of each bike and serving to check if a two-wheeler is stolen.

## Contributors

1. [@eloisebaril](https://github.com/eloisebaril)
2. [@ElisabethElMurr](https://github.com/ElisabethElMurr)
3. [@lucaorla20003](https://github.com/lucaorla20003)
4. [@Saakinaaa](https://github.com/Saakinaaa)
5. [@wwolfi](https://github.com/wwolfi)
6. [@edward-lucyszyn](https://github.com/edward-lucyszyn)

## Required Python Modules

Before running the project, make sure you have the following Python modules installed:

- cryptography
- ecdsa
- rich

You can install these modules using the following commands:

```bash
pip install cryptography
pip install ecdsa
pip install rich
```

## Project Files

### 1. `blockchain.py`

This file contains the core implementation of a simple blockchain. It includes classes and functions for creating blocks, validating transactions, and managing the blockchain.

### 2. `block.py`

The `block.py` file implements basic functionalities for handling blocks within the blockchain. It covers aspects such as block creation and validity.

### 3. `transaction.py`

The `transaction.py` file defines the structure and handling of transactions within the blockchain. It covers aspects such as transaction validation and input/output management.

### 4. `utils.py`

The `utils.py` file contains two useful functions to handle time in string format and conversely.

### 5. `main.py`

The `main.py` file serves as the entry point for the project. It orchestrates the interactions between different modules, creating a functional blockchain system.

### 6. `customer.py`, `companies.py`

These files are used to create classes that define customers and companies. Remark: `companies.py` is not used in the main because we didn't have time to manage companies in the chain.

### 7. `config.py`

This file serves as the configuration of the blockchain, providing default block size, depth, and difficulty of the proof of work.

### 8. `encryp_data.py`

The `encryp_data.py` file is used for handling keys. Keys are crucial in the blockchain, providing the opportunity to sign documents.

### 9. `README.md`

You are currently reading the project's README file, providing an overview of the project, its contributors, required modules, and file descriptions.

## How to Run the Project

1. Ensure you have Python installed on your system.
2. Install the required modules using the provided commands.
3. Run the `main.py` file to start the blockchain application.

Feel free to explore the code.

Happy coding! 🚀

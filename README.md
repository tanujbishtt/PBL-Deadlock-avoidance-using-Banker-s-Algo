# Deadlock Avoidance using Banker's Algorithm

![Language](https://img.shields.io/badge/Language-C-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A C-based command-line application that implements the Banker's Algorithm to simulate deadlock avoidance in an operating system. This project determines whether a system is in a "safe state" or an "unsafe state" based on resource allocation.

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Compilation](#compilation)
  - [Execution](#execution)
- [Example Walkthrough](#example-walkthrough)
- [Code Structure](#code-structure)

## Overview

In operating systems, a deadlock is a state in which each member of a group is waiting for another member, including itself, to release a resource. The Banker's Algorithm, developed by Edsger Dijkstra, is a resource allocation and deadlock avoidance algorithm. It tests for safety by simulating the allocation of predetermined maximum possible amounts of all resources, and then makes a "safe state" check to test for possible deadlock conditions.

This program allows a user to input the number of processes, the number of resource types, the available instances of each resource, and the maximum and currently allocated resources for each process. It then calculates the sequence of processes that can run to completion, thus determining if the system is in a safe state.

## How It Works

1.  **Input:** The program first prompts the user to enter:
    -   The total number of processes.
    -   The total number of resource types.
    -   The number of available instances for each resource type.
    -   The maximum resource needs for each process.
    -   The currently allocated resources for each process.

2.  **Need Calculation:** It calculates the `need` matrix for each process using the formula:
    ```
    Need[i][j] = Max[i][j] - Allocation[i][j]
    ```

3.  **Safety Check:** The core of the Banker's Algorithm checks if a safe sequence of processes exists.
    -   It finds a process `i` whose resource needs (`Need[i]`) are less than or equal to the currently available resources (`Work` array, initialized from `Available`).
    -   If such a process is found, it's assumed to execute and release its allocated resources. The `Work` array is updated: `Work = Work + Allocation[i]`.
    -   This step is repeated until all processes are marked as finished.

4.  **Output:**
    -   If a safe sequence is found, the program prints "System is in a SAFE STATE" and displays the safe sequence (e.g., `P1 -> P3 -> P4 -> P0 -> P2`).
    -   If no such sequence can be found, it prints "System is in an UNSAFE STATE" because a deadlock is possible.

## Features

-   **Dynamic Input:** Accepts any number of processes and resources.
-   **Clear State Indication:** Explicitly states whether the system is safe or unsafe.
-   **Safe Sequence Display:** Shows the order of execution if the state is safe.
-   **Step-by-Step Logic:** Follows the classic Banker's Algorithm logic for educational purposes.
-   **Written in C:** A lightweight and fast implementation.

## Getting Started

To get this project running on your local machine, follow these steps.

### Prerequisites

You need a C compiler installed on your system. The most common one is `gcc`.

-   **To install GCC on Debian/Ubuntu:**
    ```sh
    sudo apt update
    sudo apt install build-essential
    ```
-   **To install GCC on Fedora/CentOS:**
    ```sh
    sudo dnf install gcc
    ```

### Compilation

1.  Clone the repository:
    ```sh
    git clone https://github.com/tanujbishtt/PBL-Deadlock-avoidance-using-Banker-s-Algo.git
    cd PBL-Deadlock-avoidance-using-Banker-s-Algo
    ```

2.  Compile the C source file using `gcc`:
    ```sh
    gcc banker.c -o banker
    ```
    This command will create an executable file named `banker`.

### Execution

Run the compiled program from your terminal:
```sh
./banker

# SJT Permutation Algorithms - CT-208 (2026)

This repository contains the implementation and performance analysis of permutation generation algorithms based on the **Steinhaus-Johnson-Trotter (SJT)** logic. This project was developed as a requirement for the **CT-208** course in the Doctoral Program at the **Instituto Tecnológico de Aeronáutica (ITA)**, Brazil, taught by **Prof. Luiz Mirosola** in 2026.

## Authors
* **Flávio Souza** – Doctoral Student (ITA)
* **Nilson Sangy** – Doctoral Student (ITA)

## Overview

The primary goal of this project is to compare different strategies for generating all $n!$ permutations of a set using adjacent transpositions (Plain Changes). A system of computational analyses was developed to evaluate the efficiency of each approach.

## Implemented Algorithms

* **Algorithm P**: A standard real-time implementation of the SJT algorithm that finds the largest mobile element and performs a swap in each iteration.
* **Algorithm T (Online/Offline)**: 
    * **Online**: Generates permutations in real time, executing all search and logic reversal at each step, while recording them as "transactions" (swap indices).
    * **Offline**: Focuses on optimized execution through a pre-computed **Transition Table**. In this mode, permutation generation involves $O(1)$ complexity per step, eliminating searches and comparisons by only following previously recorded indices.

## Test & Analysis Methodology: 

To ensure the validity of the experimental data, the main script executes: 
1. **Cleanup:** Garbage collection (gc.collect()) between runs to avoid memory residue from previous tests. 
2. **Isolation:** Resetting the memory tracer (tracemalloc) for each value of $n$. 
3. **Standardization:** Using the same input vector (randomly shuffled) for all algorithms in a given $n$.

For rigorous analysis according to academic guidelines, assignments ($A$) are divided into:
* **$A$ (local vars)**: Assignments to control variables and search logic (e.g., `mobile`, `prox_idx`).
* **$A$ (to/from V)**: Assignments that directly manipulate the permutation and mechanics vectors (`a` and `d`).
* **Comparisons**: Logical tests to find moving elements and boundary limits.
* **Swaps**: Physical movements of elements in the vector.
* **Memory (KB)**: Peak amount of RAM allocated during execution.
* **Time (ms)**: Total execution time in milliseconds.

## Performance Analysis

![img1](results/T%20offline.png) ![img2](results/T%20online.png)

![img3](results/recursos.png)

The project evaluates the "viability range" for precomputing sequences:
* **Small $n$ ($n \le 11$)**: Precomputing the transition table is highly efficient as it eliminates the $O(n)$ search for the mobile element during execution.
* **Large $n$ ($n \ge 12$)**: Algorithm P is preferred due to memory constraints, as the transition table size grows factorially ($n!$).

## 📊 Algorithm: T Online

| n  | n!       | Comparações | Atribuições (local vars)  | Atribuições (to/from V)  | Trocas  | Memória (KB) | Tempo (ms)  |
|----|----------|-------------|---------------------------|--------------------------|---------|--------------|-------------|
| 3  | 6        | 88          | 47                        | 32                       | 5       | 2.76         | 0.0390      |   
| 4  | 24       | 494         | 229                       | 129                      | 23      | 3.90         | 0.1575      |   
| 5  | 120      | 3151        | 1317                      | 634                      | 119     | 10.04        | 1.2242      |   
| 6  | 720      | 22914       | 8887                      | 3755                     | 719     | 47.83        | 10.3490     |   
| 7  | 5040     | 188273      | 68669                     | 26076                    | 5039    | 319.01       | 76.6192     |   
| 8  | 40320    | 1728712     | 600595                    | 207517                   | 40319   | 2550.33      | 645.2183    |   
| 9  | 362880   | 17559351    | 5847583                   | 1860638                  | 362879  | 22705.70     | 6685.1744   |   
| 10 | 3628800  | 195592310   | 62887219                  | 18553119                 | 3628799 | 228595.02    | 73220.8081  |

---

## 📊 Algorithm: T Offline

| n  | n!       | Comparações | Atribuições (local vars) | Atribuições (to/from V) | Trocas | Memória (KB) | Setup (ms) | Tempo (ms) |
|----|----------|-------------|--------------------------|-------------------------|--------|--------------|------------|------------|
| 3  | 6        | 0           | 5                        | 13                      | 5      | 1.54         | 0.0529     | 0.0093     |      
| 4  | 24       | 0           | 23                       | 50                      | 23     | 1.66         | 0.0870     | 0.0141     |      
| 5  | 120      | 0           | 119                      | 243                     | 119    | 2.50         | 0.2223     | 0.0429     |      
| 6  | 720      | 0           | 719                      | 1444                    | 719    | 7.54         | 1.4238     | 0.5292     |      
| 7  | 5040     | 0           | 5039                     | 10085                   | 5039   | 208.66       | 10.5138    | 3.7106     |      
| 8  | 40320    | 0           | 40319                    | 80646                   | 40319  | 2439.97      | 92.4080    | 31.6959    |      
| 9  | 362880   | 0           | 362879                   | 725767                  | 362879 | 22595.33     | 927.9306   | 296.9058   |      
| 10 | 3628800  | 0           | 3628799                  | 7257608                 | 3628799| 228484.64    | 10425.2126 | 2917.7959  |   

## Project Structure

* `main.py`: Entry point for running experiments and generating graphs.
* `p.py`: Instrumented implementation of Algorithm P.
* `t.py`: Instrumented implementations of Algorithm T (Online and Offline).
* `tracker.py`: `AlgorithmTracker` class for monitoring metrics.

## Dependencies

The project is written in **Python 3.10+** and uses only the Python standard library.

The interactive charts shown in `index.html` are rendered in JavaScript (Canvas API), so no plotting package is required.

## Usage

1.  **Install dependencies**:
    ```bash
    # No external Python packages required
    ```

2.  **Run the analysis**:
    ```bash
    python src/main.py n
    python src/main.py report
    ```

The script will output a table in the terminal comparing **Comparisons**, **Attributions**, and **Exchanges** for both algorithms across values of $n$ ranging from 2 to 10. A logarithmic plot will also be generated to visualize the factorial growth of the operations.
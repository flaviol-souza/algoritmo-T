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

## Analysis Metrics

For rigorous analysis according to academic guidelines, assignments ($A$) are divided into:
* **$A$ (local vars)**: Assignments to control variables and search logic (e.g., `mobile`, `prox_idx`).
* **$A$ (to/from V)**: Assignments that directly manipulate the permutation and mechanics vectors (`a` and `d`).
* **Comparisons**: Logical tests to find moving elements and boundary limits.
* **Swaps**: Physical movements of elements in the vector.

## Performance Analysis

![img1](results/T%20offline.png) ![img2](results/T%20online.png)

The project evaluates the "viability range" for precomputing sequences:
* **Small $n$ ($n \le 11$)**: Precomputing the transition table is highly efficient as it eliminates the $O(n)$ search for the mobile element during execution.
* **Large $n$ ($n \ge 12$)**: Algorithm P is preferred due to memory constraints, as the transition table size grows factorially ($n!$).

                *** Algoritm: T online ***
-------------------------------------------------------------------------------------------------
n    | n!         | Comparacoes  | Atribuicoes (local vars)  | Atribuicoes (to/from  V) | Trocas  
-------------------------------------------------------------------------------------------------
3    | 6          | 90           | 52                        | 27                       | 5        
4    | 24         | 508          | 252                       | 106                      | 23       
5    | 120        | 3230         | 1436                      | 515                      | 119      
6    | 720        | 23388        | 9606                      | 3036                     | 719      
7    | 5040       | 191506       | 73708                     | 21037                    | 5039     
8    | 40320      | 1753904      | 640914                    | 167198                   | 40319    
9    | 362880     | 17781102     | 6210462                   | 1497759                  | 362879   
10   | 3628800    | 197769580    | 66516018                  | 14924320                 | 3628799  


                *** Algoritm: T offline ***
-------------------------------------------------------------------------------------------------
n    | n!         | Comparacoes  | Atribuicoes (local vars)  | Atribuicoes (to/from  V) | Trocas  
-------------------------------------------------------------------------------------------------
3    | 6          | 75           | 52                        | 41                       | 5        
4    | 24         | 416          | 252                       | 157                      | 23       
5    | 120        | 2635         | 1436                      | 759                      | 119      
6    | 720        | 19074        | 9606                      | 4481                     | 719      
7    | 5040       | 156233       | 73708                     | 31123                    | 5039     
8    | 40320      | 1431352      | 640914                    | 247845                   | 40319    
9    | 362880     | 14515191     | 6210462                   | 2223527                  | 362879   
10   | 3628800    | 161481590    | 66516018                  | 22181929                 | 3628799  

## Project Structure

* `main.py`: Entry point for running experiments and generating graphs.
* `p.py`: Instrumented implementation of Algorithm P.
* `t.py`: Instrumented implementations of Algorithm T (Online and Offline).
* `tracker.py`: `AlgorithmTracker` class for monitoring metrics.

## Dependencies

The project is written in **Python 3.10+** and requires the following libraries for data analysis and visualization:
* `matplotlib`: For plotting complexity curves.
* `pandas`: For organizing metric tables.
* `math`: For factorial calculations.

## Usage

1.  **Install dependencies**:
    ```bash
    pip install matplotlib pandas
    ```

2.  **Run the analysis**:
    ```bash
    python src/main.py
    ```

The script will output a table in the terminal comparing **Comparisons**, **Attributions**, and **Exchanges** for both algorithms across values of $n$ ranging from 2 to 10. A logarithmic plot will also be generated to visualize the factorial growth of the operations.
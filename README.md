# Complexity and Discrete Tomography Project

## Overview

This project tackles the discrete tomography problem: coloring a grid in black and white under constraints on consecutive blocks in each row and column.

The solution includes two main approaches:

1. **Incomplete Method (Section 1):**

   * Dynamic programming algorithm to check if a row can be colored according to a given sequence.
   * Generalization to partially colored rows.
   * Propagation to automatically color some cells.
   * Polynomial complexity but incomplete.

2. **Complete Method (Section 2):**

   * Recursive enumeration with backtracking.
   * Integration of propagation to prune the search tree.
   * Exponential complexity but complete.

## Code Structure

* `Grille.py` — main class implementing the logic and algorithms
* `util.py` — utility functions (some overlap with Grille.py)
* Clean and organized project structure with LICENSE file included

## Features

* Dynamic programming with memoization for row and column validation
* Propagation techniques to deduce cell colors automatically
* Backtracking with recursive enumeration for complete search
* Optimizations such as skipping already colored cells and early pruning

## Usage

1. Prepare your input file in the following format:

   * List the sequences of black block lengths for each row, one row per line
   * Insert a line containing only `#`
   * List the sequences of black block lengths for each column, one column per line

2. Run the solver script (e.g., `python main.py input.txt`) — adapt as per your project setup.

3. The output will provide the solved grid with black/white coloring satisfying the constraints.

4. You can customize or extend the code to test different instances or integrate visualization.

## Strengths

* Correct and clear implementation of core algorithms
* Efficient memoization and propagation
* Clean code with clear naming and structure
* Thoroughly tested on multiple instances


## License

This project is licensed under the MIT License — see LICENSE.txt for details.

---

If you want me to tailor the usage section for a specific script name or execution method, just let me know!

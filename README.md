

# TOPSIS – Multi-Criteria Decision-Making (MCDM) Project

## Overview
This project implements **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** to rank alternatives based on multiple criteria, considering their **weights** and **impacts** (benefit/cost). The project is divided into **three parts**:  

1. **Command-line Python program**  
2. **Python package for PyPI**  
3. **Web service for automated TOPSIS evaluation via email**  

---

## Part I – Command-Line Program
**Usage:**  
```bash
python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```
Example:

```bash
python topsis.py data.csv "1,1,1,1,2" "+,+,-,+,+" output-result.csv
```

**Features:**

* Validates **number of arguments**, **file existence**, and **numeric criteria**.
* Checks that **number of weights = number of impacts = number of criteria**.
* Supports **benefit (+)** and **cost (-)** criteria.
* Generates a CSV with **TOPSIS scores and ranks**.

---

## Part II – Python Package

* Install via PyPI:

```bash
pip install Topsis-Trishti-102313056
```

* Provides the same command-line functionality as Part I.
* Includes a **user manual** and example usage.

---

## Part III – Web Service

* Users provide **input CSV, weights, impacts, and email**.
* Validates inputs and sends the **result file via email**.
* Useful for remote TOPSIS evaluation without local Python installation.

---

## Input / Output

**Input:** CSV with alternatives and criteria.

**Output:** CSV containing:

| Alternative | TOPSIS Score | Rank |
| ----------- | ------------ | ---- |
| A1          | 0.78         | 1    |
| A2          | 0.42         | 2    |

---

## Technologies

* **Language:** Python
* **Libraries:** `numpy`, `pandas`, `flask`, `smtplib`
---

## Key Learnings

* Implementing **TOPSIS methodology** for multi-criteria decisions.
* Handling **file validation and command-line arguments**.
* Creating and uploading a **Python package**.
* Developing a **web service with email output**.

---


## Screenshot of Interface

<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/c5894a1a-9d86-49a8-a6af-ed5c7ffb140c" />







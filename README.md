<a name="readme-top"></a>

# 


CS 6840
Formal System Design
Summer Semester 2025
FINAL PROJECT PROPOSAL
DUE 7/29/2025
Please fill out and submit the following final project information:
(1) Indicate the type of project
(2) Provide a project title
(3) Describe the project concept in 100 words or less
Student Name: ___________________________
Project Type: ____ Research Paper ____ Programming Project
Project Title: _________________________________
Project Concept (100 words or less):


**Student Name:** Kevin Bell

**Project Type:** ☑ Programming Project ☐ Research Paper

**Project Title:** Developing a BDD‑Based CTL Model Checker

**Project Concept (100 words or less):**
We will design and implement a model checker for Computational Tree Logic (CTL) using Binary Decision Diagrams (BDDs) to represent state sets symbolically. Starting from a user‑specified transition system and CTL formula, the tool will construct BDDs for atomic propositions, compute predecessor and fixpoint operations, and evaluate temporal operators (EG, EU, AF, etc.) efficiently. We’ll compare its performance against an explicit‑state checker on benchmark examples, analyze memory and runtime trade‑offs, and document how BDD variable ordering impacts scalability. The final deliverable includes source code, test suite, and a performance report.


## Getting Started

The project requires **Python 3.10+**. The code lives in `src/` and the unit tests are in `tests/`. No compilation step is needed because everything is written in Python. Follow these steps to set up a development environment and run the model checker:

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd cs6840finalProject
   ```

2. **Create and activate a virtual environment** (recommended)

   On **Linux/macOS**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On **Windows (like in VS Code) (PowerShell)**:

   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   # If you get a policy error, run
   # Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the tests**

   ```bash
   pytest
   ```

5. **Run the example script**

   A minimal demonstration is provided in `example_usage.py`.
   Execute it from the repository root:

   ```bash
   python example_usage.py
   ```


   The script prints the following results, one per line:

   ```
   True
   False
   True
   False
   True
   False
   ```

   These correspond to the formulas `EF p`, `AG p`, `AF p`, `EG q`,
   `E[q U p]`, and `A[q U p]` in that order. They match the expectations in the
   unit tests.



## Test Suite Overview

The `tests/` directory contains six unit tests exercising key CTL operators on
small example transition systems. Each test instantiates a transition system and
checks whether a CTL formula holds starting from the initial state.

| Test name | Checked formula | Expected result |
|-----------|-----------------|-----------------|
| `test_ef_p` | `EF p` | **True** – a path exists where `p` eventually holds. |
| `test_ag_p_false` | `AG p` | **False** – not all paths maintain `p` globally. |
| `test_af_p_true` | `AF p` | **True** – on all paths `p` is eventually reached. |
| `test_eg_q_false` | `EG q` | **False** – no path stays in states labeled `q` forever. |
| `test_eu_q_until_p_true` | `E[q U p]` | **True** – a path exists where `q` holds until `p` becomes true. |
| `test_au_q_until_p_false` | `A[q U p]` | **False** – there exists a path that remains in `q` indefinitely without ever reaching `p`. |



--------------------------------------------------------------------------------------------------------------------------
== We're Using GitHub Under Protest ==

This project is currently hosted on GitHub.  This is not ideal; GitHub is a
proprietary, trade-secret system that is not Free and Open Souce Software
(FOSS).  We are deeply concerned about using a proprietary system like GitHub
to develop our FOSS project. I have a [website](https://bellKevin.me) where the
project contributors are actively discussing how we can move away from GitHub
in the long term.  We urge you to read about the [Give up GitHub](https://GiveUpGitHub.org) campaign 
from [the Software Freedom Conservancy](https://sfconservancy.org) to understand some of the reasons why GitHub is not 
a good place to host FOSS projects.

If you are a contributor who personally has already quit using GitHub, please
email me at **bellKevin@pm.me** for how to send us contributions without
using GitHub directly.

Any use of this project's code by GitHub Copilot, past or present, is done
without our permission.  We do not consent to GitHub's use of this project's
code in Copilot.

![Logo of the GiveUpGitHub campaign](https://sfconservancy.org/img/GiveUpGitHub.png)

<p align="right"><a href="#readme-top">back to top</a></p>

# Lab 5 - Static Analysis Reflection

These responses cover the reflection topics described in the lab handout. The available handout does not print the precise wording of four individual questions.

## 1. How did static analysis help identify problems in the original program?

Pylint revealed maintainability problems such as a mutable default argument, bare exception handlers, missing documentation and inconsistent naming. Bandit highlighted security risks such as unsafe SQL construction, arbitrary code execution and weak cryptographic practices. Flake8 reported formatting problems, including whitespace and line-length violations. Together, the tools helped identify issues that were easy to overlook when the program appeared to run.

## 2. Which findings were most important to fix, and why?

The SQL injection risks and use of `exec()` were especially important because they could let untrusted inputs influence database queries or execute code. The hard-coded administrator password, insecure receipt-file permissions, weak hash and predictable booking codes were also security concerns. I addressed the higher-risk issues before style-only changes.

## 3. Why are multiple analysis tools useful?

The tools focus on different dimensions of quality. Pylint checks potential code errors and maintainability, Bandit checks common security problems, and Flake8 checks style and syntax-related issues. Running all three produced a more useful review than relying on any one tool alone. I verified progress by comparing the saved before-and-after reports.

## 4. What did the final verification show, and what are its limitations?

The saved final results show a Pylint score of **10.00/10**, **zero Bandit findings**, and **no Flake8 violations**. That is strong evidence that the flagged issues were addressed. Static analysis cannot guarantee the program is functionally correct or secure in every situation; runtime tests and review of business rules are still necessary.

# Web-Security-Lab
Interactive learning platform demonstrating common web security vulnerabilities and their defenses.

## Features

- **SQL Injection**: Shows vulnerable vs secure query construction
- **Cross-Site Scripting (XSS)**: Demonstrates input sanitization
- **CSRF Protection**: Implements anti-CSRF tokens
- **Input Validation**: Shows proper validation techniques

## Labs Overview
### 1. SQL Injection Lab
- **Vulnerable**: String concatenation in SQL queries
- **Secure**: Parameterized queries with placeholders
- **Test payload**: admin' OR '1'='1

### 2. XSS Lab
- **Vulnerable**: Direct HTML injection
- **Secure**: HTML entity escaping
- **Test payload**: ```<script>alert('XSS')</script>```
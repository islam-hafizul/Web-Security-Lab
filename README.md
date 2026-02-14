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
<script>
3. CSRF Lab
Vulnerable: No CSRF protection

Secure: Flask-WTF CSRF tokens

Demonstration: Form submission protection

4. Input Validation Lab
Vulnerable: No validation

Secure: Regex validation and type checking

Tests: Email format, age range, input sanitization
</script>

## Tech Stack
- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: Flask-WTF, HTML escaping, parameterized queries

## Testing the Vulnerabilities
Each lab provides:

- ✅ Explanation of the vulnerability
- ❌ Vulnerable implementation
- ✅ Secure implementation
- 💡 Suggested attack payloads
- 🛡️ Defense mechanisms

## Learning Resources
- OWASP Top 10
- Web Security Academy (PortSwigger)
- MDN Web Security Guide

## ⚠️ Disclaimer
This project is for educational purposes only. Use only in controlled, isolated environments. Do not deploy vulnerable code to production.

## License
MIT License - See LICENSE file for details

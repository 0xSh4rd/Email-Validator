# 📧 Email Validator

A command-line tool for validating email addresses with format checking, MX record verification, and domain existence validation.

## ✨ Features

- ✅ Email format validation using regex
- 🌐 MX record verification to check if domain accepts email
- 📡 Domain existence checking 
- 📁 Batch validation from files
- 🔍 Extract emails from text files
- 📊 Export results to CSV or JSON
- ⚡ Concurrent processing for fast validation
- 📥 Read from stdin for pipeline integration

## 📋 Requirements

- Python 3.6 or higher
- dnspython library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xSh4rd/email-validator.git
cd email-validator
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage

```bash
python main.py <command> [options]
```

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

## ⚙️ Commands

- `validate`: Validate a single email address
- `file`: Validate emails from a file
- `extract`: Extract emails from a text file
- `stdin`: Validate emails from standard input

## 📋 Command Options

### Validate a single email:
```bash
python main.py validate <email> [options]
```

Options:

- `--no-mx`: Skip MX record check
- `--no-domain`: Skip domain existence check
- `-v, --verbose`: Show detailed information

### Validate from file:
```bash
python main.py file <input_file> [options]
```

Options:

- `-o, --output`: Output file for results
- `-f, --format`: Output format (csv, json)
- `--no-mx`: Skip MX record check
- `--no-domain`: Skip domain existence check
- `-w, --workers`: Number of concurrent workers

### Extract emails from text:
```bash
python main.py extract <input_file> [options]
```

Options:

- `-o, --output`: Output file for extracted emails

### Validate from stdin:
```bash
python main.py stdin [options]
```

Options:

- `--no-mx`: Skip MX record check
- `--no-domain`: Skip domain existence check

## 📝 Examples

### Validate a single email:
```bash
python main.py validate john.doe@example.com
```

### Validate a single email without MX check:
```bash
python main.py validate john.doe@example.com --no-mx
```

### Validate emails from a file:
```bash
python main.py file emails.txt
```

### Validate emails from a file and save results to CSV:
```bash
python main.py file emails.txt -o results.csv -f csv
```

### Extract emails from a document:
```bash
python main.py extract document.txt -o extracted_emails.txt
```

### Validate from stdin:
```bash
echo "test@example.com" | python main.py stdin
```

### Batch process with multiple workers:
```bash
python main.py file large_list.txt -w 20 -o results.json -f json
```

## 🔍 Validation Levels

The tool performs validation at multiple levels:

1. **Format Validation**
   - Checks if the email follows standard format (user@domain.tld)
   - Uses regex pattern for comprehensive format checking

2. **MX Record Check**
   - Verifies that the domain has mail exchange servers
   - Indicates the domain can receive emails

3. **Domain Existence**
   - Checks if the domain name resolves to an IP address
   - Confirms the domain is active

Results are categorized as:
- **VALID**: Format correct, MX records exist, domain resolves
- **DOUBTFUL**: Format correct, but MX or domain check failed
- **INVALID**: Format is incorrect

## 💡 Tips

- Use the `--no-mx` and `--no-domain` flags for faster validation when only format checking is needed
- For large lists, adjust the number of workers (-w) based on your system's capabilities
- The extract command is useful for cleaning up messy contact lists
- Results can be piped to other tools for further processing
- Consider rate limiting when validating very large lists to avoid potential IP blocks

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.




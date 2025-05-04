#!/usr/bin/env python3

import argparse
import re
import dns.resolver
import socket
import csv
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email regex pattern
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_format(email):
    """Validate email format using regex"""
    return bool(re.match(EMAIL_REGEX, email.strip()))

def check_mx_records(domain):
    """Check if domain has valid MX records"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return len(mx_records) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False
    except Exception as e:
        return False

def check_domain_exists(domain):
    """Check if domain exists using A record lookup"""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def validate_email(email, check_mx=True, check_domain=True):
    """Validate an email address with multiple checks"""
    email = email.strip()
    results = {
        'email': email,
        'valid_format': False,
        'has_mx': None,
        'domain_exists': None,
        'status': 'invalid'
    }
    
    # Check format
    if not validate_format(email):
        return results
    
    results['valid_format'] = True
    
    # Extract domain
    domain = email.split('@')[1]
    
    # Check MX records
    if check_mx:
        results['has_mx'] = check_mx_records(domain)
    
    # Check domain exists
    if check_domain:
        results['domain_exists'] = check_domain_exists(domain)
    
    # Determine overall status
    if results['valid_format']:
        if (check_mx and not results['has_mx']) or (check_domain and not results['domain_exists']):
            results['status'] = 'doubtful'
        else:
            results['status'] = 'valid'
    
    return results

def validate_single_email(email, check_mx=True, check_domain=True, verbose=False):
    """Validate a single email and display results"""
    results = validate_email(email, check_mx, check_domain)
    
    print(f"\nEmail: {email}")
    print("-" * 50)
    print(f"Format validation: {'✓' if results['valid_format'] else '✗'}")
    
    if results['valid_format']:
        if check_mx:
            print(f"MX records: {'✓' if results['has_mx'] else '✗'}")
        if check_domain:
            print(f"Domain exists: {'✓' if results['domain_exists'] else '✗'}")
        
        print(f"Overall status: {results['status'].upper()}")
    else:
        print("Overall status: INVALID")
    
    print("-" * 50)
    
    return results

def validate_file(file_path, check_mx=True, check_domain=True, output_file=None, format='csv', workers=10):
    """Validate emails from a file"""
    emails = []
    
    # Read emails from file
    try:
        with open(file_path, 'r') as f:
            emails = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not emails:
        print("No emails found in file")
        return
    
    print(f"Validating {len(emails)} emails...")
    
    # Validate emails concurrently
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_email = {executor.submit(validate_email, email, check_mx, check_domain): email 
                           for email in emails}
        
        processed = 0
        for future in as_completed(future_to_email):
            result = future.result()
            results.append(result)
            processed += 1
            
            # Show progress
            progress = (processed / len(emails)) * 100
            print(f"\rProgress: {progress:.1f}%", end='')
    
    print("\nValidation complete!")
    
    # Display summary
    valid_count = sum(1 for r in results if r['status'] == 'valid')
    doubtful_count = sum(1 for r in results if r['status'] == 'doubtful')
    invalid_count = sum(1 for r in results if r['status'] == 'invalid')
    
    print(f"\nSummary:")
    print(f"Valid: {valid_count}")
    print(f"Doubtful: {doubtful_count}")
    print(f"Invalid: {invalid_count}")
    
    # Save results if output file specified
    if output_file:
        save_results(results, output_file, format)

def save_results(results, output_file, format):
    """Save validation results to file"""
    try:
        if format == 'csv':
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Email', 'Format Valid', 'Has MX', 'Domain Exists', 'Status'])
                
                for r in results:
                    writer.writerow([
                        r['email'],
                        'Yes' if r['valid_format'] else 'No',
                        'Yes' if r['has_mx'] else 'No' if r['has_mx'] is not None else 'N/A',
                        'Yes' if r['domain_exists'] else 'No' if r['domain_exists'] is not None else 'N/A',
                        r['status']
                    ])
        
        elif format == 'json':
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        
        print(f"Results saved to {output_file}")
    
    except Exception as e:
        print(f"Error saving results: {e}")

def extract_emails_from_text(text):
    """Extract email addresses from text"""
    emails = re.findall(EMAIL_REGEX, text)
    return list(set(emails))  # Remove duplicates

def extract_from_file(file_path, output_file=None):
    """Extract email addresses from a text file"""
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        
        emails = extract_emails_from_text(text)
        
        if not emails:
            print("No email addresses found in file")
            return
        
        print(f"Found {len(emails)} unique email addresses:")
        for email in sorted(emails):
            print(f"  {email}")
        
        if output_file:
            with open(output_file, 'w') as f:
                for email in sorted(emails):
                    f.write(email + '\n')
            print(f"\nEmails saved to {output_file}")
    
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Email Validator - Validate and extract email addresses")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Validate single email
    validate_parser = subparsers.add_parser("validate", help="Validate a single email address")
    validate_parser.add_argument("email", help="Email address to validate")
    validate_parser.add_argument("--no-mx", action="store_true", help="Skip MX record check")
    validate_parser.add_argument("--no-domain", action="store_true", help="Skip domain existence check")
    validate_parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information")
    
    # Validate from file
    file_parser = subparsers.add_parser("file", help="Validate emails from a file")
    file_parser.add_argument("input", help="Input file containing emails (one per line)")
    file_parser.add_argument("-o", "--output", help="Output file for results")
    file_parser.add_argument("-f", "--format", choices=['csv', 'json'], default='csv', help="Output format")
    file_parser.add_argument("--no-mx", action="store_true", help="Skip MX record check")
    file_parser.add_argument("--no-domain", action="store_true", help="Skip domain existence check")
    file_parser.add_argument("-w", "--workers", type=int, default=10, help="Number of concurrent workers")
    
    # Extract emails from text
    extract_parser = subparsers.add_parser("extract", help="Extract emails from a text file")
    extract_parser.add_argument("input", help="Input file to extract emails from")
    extract_parser.add_argument("-o", "--output", help="Output file for extracted emails")
    
    # Validate from stdin
    stdin_parser = subparsers.add_parser("stdin", help="Validate emails from standard input")
    stdin_parser.add_argument("--no-mx", action="store_true", help="Skip MX record check")
    stdin_parser.add_argument("--no-domain", action="store_true", help="Skip domain existence check")
    
    args = parser.parse_args()
    
    if args.command == "validate":
        validate_single_email(
            args.email,
            check_mx=not args.no_mx,
            check_domain=not args.no_domain,
            verbose=args.verbose
        )
    
    elif args.command == "file":
        validate_file(
            args.input,
            check_mx=not args.no_mx,
            check_domain=not args.no_domain,
            output_file=args.output,
            format=args.format,
            workers=args.workers
        )
    
    elif args.command == "extract":
        extract_from_file(args.input, args.output)
    
    elif args.command == "stdin":
        print("Enter emails (one per line, Ctrl+C to finish):")
        emails = []
        try:
            while True:
                line = input().strip()
                if line:
                    emails.append(line)
        except KeyboardInterrupt:
            print("\n")
        
        for email in emails:
            validate_single_email(
                email,
                check_mx=not args.no_mx,
                check_domain=not args.no_domain
            )
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

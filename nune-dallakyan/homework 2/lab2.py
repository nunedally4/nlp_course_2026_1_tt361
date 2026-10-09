import re

# Problem 1
text = """Contact us at support@example.com or sales@company.org for assistance.
For personal inquiries, email john.doe123@university.edu."""

emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)

print("Email addresses:")
for email in emails:
    print(email)

print("\n" + "="*30 + "\n")

# Problem 2
text2 = """Valid: 123-456-7890, 987-654-3210
Invalid: 12-345-67890, 1234567890, 123-45-6789"""

phone_numbers = re.findall(r'\b\d{3}-\d{3}-\d{4}\b', text2)

print("Valid phone numbers:")
for phone in phone_numbers:
    print(phone)

print("\n" + "="*30 + "\n")

# Problem 3
text3 = """Important dates: 25/12/2023, 01-01-2024, 31/05/2023, and 15-10-2024."""
dates = re.findall(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', text3)

print("Dates:")
for date in dates:
    print(date)

print("\n" + "="*30 + "\n")

# Problem 4
text4 = "The the quick brown fox jumps over the the lazy dog."

repeated_words = re.finditer(r'\b(\w+)\s+\1\b', text4, re.IGNORECASE)

print("Repeated words:")
for match in repeated_words:
    print(match.group(0))

print("\n" + "="*30 + "\n")

# Problem 5
text5 = "Check out our new products: #Sale2024, #NewArrival, and #Discounts!"

hashtags = re.findall(r'#\w+', text5)
print("Hashtags:")
for hashtag in hashtags:
    print(hashtag)

print("\n" + "="*30 + "\n")

# Problem 6
text6 = """Sample Passwords:
Valid: Password123, Secure456
Invalid: weak, password, Password"""

valid_passwords = re.findall(r'Valid:\s*(.*)', text6)
invalid_passwords = re.findall(r'Invalid:\s*(.*)', text6)

print("Password results:")

for group in valid_passwords:
    passwords = re.findall(r'\b\w+\b', group)
    for password in passwords:
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
            print(password, "Valid")
        else:
            print(password, "Invalid")

for group in invalid_passwords:
    passwords = re.findall(r'\b\w+\b', group)
    for password in passwords:
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password):
            print(password, "Valid")
        else:
            print(password, "Invalid")

print("\n" + "="*30 + "\n")

# Problem 7
text7 = """Visit our website at https://www.example.com or check out
http://blog.example.org for updates."""

urls = re.findall(r'https?://\S+', text7)

print("URLs:")
for url in urls:
    print(url)

print("\n" + "="*30 + "\n")

# Problem 8
text8 = "This text has multiple spaces    between words."

result = re.sub(r'\s+', ' ', text8)
print("Cleaned text:")
print(result)

print("\n" + "="*30 + "\n")

# Problem 9
text9 = 'He said, "Hello, world!" and she replied, "Hi there!"'

quoted_text = re.findall(r'"(.*?)"', text9)
print("Quoted text:")
for text1 in quoted_text:
    print(text1)

print("\n" + "="*30 + "\n")

# Problem 10
text10 = """Valid: 192.168.1.1, 10.0.0.255
Invalid: 256.1.2.3, 192.168.01.1, 192.168.1"""

ip_addresses = re.findall(
    r'\b(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\b', 
    text10
)

print("Valid IP addresses:")
for ip in ip_addresses:
    print(ip)
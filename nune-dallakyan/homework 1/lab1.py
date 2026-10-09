import re


# Problem 1: extract email addresses.
text = """Contact us at support@example.com or sales@company.org for assistance.
For personal inquiries, email john.doe123@university.edu."""

emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}", text)

print("Problem 1: Extract Email Addresses")
for email in emails:
    print(email)


# Problem 2: validate phone numbers in the format XXX-XXX-XXXX.
text = """Valid: 123-456-7890, 987-654-3210
Invalid: 12-345-67890, 1234567890, 123-45-6789"""

candidates = re.findall(r"\d[\d-]*\d", text)
valid_phones = [c for c in candidates if re.fullmatch(r"\d{3}-\d{3}-\d{4}", c)]

print("\nProblem 2: Validate Phone Numbers")
print("Valid phone numbers:")
for phone in valid_phones:
    print(phone)


# Problem 3: extract dates in DD/MM/YYYY or DD-MM-YYYY format.
text = "Important dates: 25/12/2023, 01-01-2024, 31/05/2023, and 15-10-2024."

# \2 makes sure the same separator is used in both places.
dates = [m.group() for m in re.finditer(r"\b(\d{2})([/-])\d{2}\2\d{4}\b", text)]

print("\nProblem 3: Extract Dates")
for date in dates:
    print(date)


# Problem 4: find repeated words such as "the the".
text = "The the quick brown fox jumps over the the lazy dog."

repeated = [m.group().lower() for m in re.finditer(r"\b(\w+)\s+\1\b", text, re.IGNORECASE)]

print("\nProblem 4: Find Repeated Words")
print("Repeated words:")
for pair in repeated:
    print(pair)


# Problem 5: extract hashtags.
text = "Check out our new products: #Sale2024, #NewArrival, and #Discounts!"

hashtags = re.findall(r"#\w+", text)

print("\nProblem 5: Extract Hashtags")
for hashtag in hashtags:
    print(hashtag)


# Problem 6: validate password strength.
passwords = """Valid: Password123, Secure456
Invalid: weak, password, Password"""

candidates = re.findall(r"(?<=[:,] )\w+", passwords)
# Lookaheads check for a lowercase letter, an uppercase letter and a digit;
# .{8,} checks the length.
strong = r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}"
valid_passwords = [p for p in candidates if re.fullmatch(strong, p)]

print("\nProblem 6: Validate Password Strength")
print("Valid passwords:")
for password in valid_passwords:
    print(password)


# Problem 7: extract URLs.
text = "Visit our website at https://www.example.com or check out http://blog.example.org for updates."

urls = re.findall(r"https?://[\w.-]+(?:/[^\s]*)?(?<![.,!?])", text)

print("\nProblem 7: Extract URLs")
for url in urls:
    print(url)


# Problem 8: replace multiple spaces with a single space.
text = "This   text    has   multiple     spaces."

single_spaced = re.sub(r" {2,}", " ", text)

print("\nProblem 8: Replace Multiple Spaces with a Single Space")
print(single_spaced)


# Problem 9: extract text within double quotes.
text = 'He said, "Hello, world!" and she replied, "Hi there!"'

quotes = re.findall(r'"([^"]*)"', text)

print("\nProblem 9: Extract Quoted Text")
for quote in quotes:
    print(quote)


# Problem 10: validate IPv4 addresses.
text = """Valid: 192.168.1.1, 10.0.0.255
Invalid: 256.1.2.3, 192.168.01.1, 192.168.1"""

candidates = re.findall(r"\d+(?:\.\d+)*", text)
# Each octet is 0-255 with no leading zeros (so 01 is rejected).
octet = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
ip_pattern = rf"{octet}(?:\.{octet}){{3}}"
valid_ips = [ip for ip in candidates if re.fullmatch(ip_pattern, ip)]

print("\nProblem 10: Validate IP Addresses")
print("Valid IP addresses:")
for ip in valid_ips:
    print(ip)

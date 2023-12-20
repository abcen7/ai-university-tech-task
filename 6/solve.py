from os.path import abspath
import re

SOURCE_FILENAME = abspath('./6/data/emails.txt')
TARGET_FILENAME = abspath('./6/data/copied_emails.txt')

def email_generator(filename: str):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    with open(filename, 'r') as file:
        for line in file:
            for email in email_pattern.findall(line.strip()):
                yield email

def copy_emails_to_file(source_file, target_file):
    with open(target_file, 'w') as outfile:
        for email in email_generator(source_file):
            outfile.write(email + '\n')


copy_emails_to_file(SOURCE_FILENAME, TARGET_FILENAME)
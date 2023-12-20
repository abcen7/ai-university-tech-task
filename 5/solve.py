from os.path import abspath

def count_words_in_row(row: str) -> int:
    return len([word for word in row.split()])

with open(abspath('5/file.txt'), mode='r') as file:
    rows = [line.strip() for line in file.readlines()]

for index, row in enumerate(rows):
    print(f"В {index + 1} строке {count_words_in_row(row)} слов(а)")
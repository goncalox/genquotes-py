import csv

def read_quotes_from_file(filename):
    quotes_list = []

    # Open the file
    with open(filename, 'r', encoding='utf-8') as file:
        # Read the entire content of the file
        content = file.read().strip()
        
        # Split the content by ';' to get individual parts
        parts = content.split(';')

        # Iterate over the parts in groups of 3 (author, quote, description)
        for i in range(0, len(parts), 3):
            if i + 2 < len(parts):  # Ensure there are enough parts for a complete quote
                author = parts[i].strip()
                quote = parts[i + 1].strip()
                description = parts[i + 2].strip()
                
                # Append to the list as a dictionary
                quotes_list.append({
                    'author': author,
                    'quote': quote,
                    'description': description
                })

    return quotes_list

# Example usage
filename = 'quotes.txt'
quotes = read_quotes_from_file(filename)

# Print the quotes to verify
for q in quotes:
    print(f"Author: {q['author']}")
    print(f"Quote: {q['quote']}")
    print(f"Description: {q['description']}")
    print('---')

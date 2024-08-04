# Define the input and output file paths
input_file = 'quotes.txt'
output_file = 'quotes_output.txt'

# Function to process the input file and write to the output file
def process_quotes(input_path, output_path):
    try:
        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            content = infile.read()
            parts = content.split('. ')
            
            quotes = []
            for i in range(0, len(parts), 3):
                if i + 2 < len(parts):
                    author = parts[i].strip()
                    quote = parts[i+1].strip()
                    message = parts[i+2].strip()
                    # Write the formatted line to the output file
                    outfile.write(f"{quote};{author};{message}\n")
                else:
                    print(f"Skipping incomplete quote part starting with: {parts[i]}")
    except Exception as e:
        print(f"Error processing files: {e}")

# Call the function to process the quotes
process_quotes(input_file, output_file)

print("Quotes have been processed and written to the output file.")

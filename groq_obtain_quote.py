import os
import shutil
import textwrap
import get_wikimedia_image
from groq import Groq

def split_text_into_lines(text, width=40):
    return '\n'.join(textwrap.wrap(text, width))

def get_inspiring_quote(api_key):
    client = Groq(api_key=api_key)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """
Could you please provide me with a random philosophical quote not answered before, its author, and some advice based on the quote? The quote should have exactly two sentences. Please format your response as follows:

Quote: [The inspiring quote]
Author: [The author's name]
Advice: [Your advice based on the quote]
"""
            }
        ],
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    # Extracting the quote, author, and advice from the response
    quote = ""
    author = ""
    advice = ""

    lines = response.split('\n')
    for line in lines:
        if line.startswith("Quote: "):
            quote = line.replace("Quote: ", "").strip().strip('"')
        elif line.startswith("Author: "):
            author = line.replace("Author: ", "").strip()
        elif line.startswith("Advice: "):
            advice = line.replace("Advice: ", "").strip()

    return quote, author, advice

def write_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Create temp_text_files directory if it doesn't exist
folder = "temp_text_files"
if not os.path.exists(folder):
    os.makedirs(folder)

# Delete existing files in temp_text_files directory
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

    def process_quote(api_key, folder):
        # Get the quote, author, and advice
        quote, author, advice = get_inspiring_quote(api_key)

        # Split the quote into sentences
        quote_sentences = quote.split('. ')
        if len(quote_sentences) > 0:
            write_to_file(os.path.join(folder, 'quote1.txt'), split_text_into_lines(quote_sentences[0] + ('.' if not quote_sentences[0].endswith('.') else '')))
        if len(quote_sentences) > 1:
            write_to_file(os.path.join(folder, 'quote2.txt'), split_text_into_lines(quote_sentences[1] + ('.' if not quote_sentences[1].endswith('.') else '')))

        # Write author and advice to their respective files
        write_to_file(os.path.join(folder, 'author.txt'), author)
        write_to_file(os.path.join(folder, 'advice.txt'), advice)

        print(f"Quote: {quote}")
        print(f"Author: {author}")
        print(f"Advice: {advice}")

        return get_wikimedia_image.get_wikimedia_image(author, "assets/background.jpeg")

    # API key (You should store this securely, not in plain text)
    api_key = "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"
    folder = "temp_text_files"  # Replace with your actual folder path

    # Run the process until get_wikimedia_image does not return None
    while process_quote(api_key, folder) is None:
        pass
import os
# Define base path
base_path = r"C:\Users\Kaustubh_k\PycharmProjects\Marathi_RAG\pythonProject2"

# Define the directory path
markdown_directory = os.path.join(base_path, "New Folder")

# Create the directory if it doesn't exist
if not os.path.exists(markdown_directory):
    os.makedirs(markdown_directory)

# Define the Markdown file path
markdown_path = os.path.join(markdown_directory, "example.md")

# Save the Markdown file
with open(markdown_path, 'w', encoding='utf-8') as md_file:
    md_file.write(r"C:\Users\Kaustubh_k\PycharmProjects\Marathi_RAG\pythonProject2\content")






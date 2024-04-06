import os
from IPython.display import Markdown
from pdf2image import convert_from_path
import ipywidgets as widgets
from IPython.display import display as ipy_display
from ipywidgets import Output
import pytesseract
from PIL import Image

def pdf_to_markdown(pdf_path, markdown_path, save_file=True, language='mar'):
    """
    Convert a PDF file to Markdown using OCR.

    Args:
        pdf_path (str): Path to the input PDF file.
        markdown_path (str): Path to save the output Markdown file.
        save_file (bool): Flag to indicate whether to save the Markdown file.
        language (str): Language for OCR. Default is 'mar' (Marathi).

    Returns:
        str: Extracted text in Markdown format.
    """
    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Initialize a variable to store the accumulated text
    accumulated_text = ''

    # Check if the output directory exists, create it if it doesn't
    output_directory = os.path.dirname(markdown_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Perform OCR on each image
    for i, image in enumerate(images):
        # Save the image as a temporary file
        image_path = f'image_{i}.png'
        image.save(image_path, 'PNG')

        # Perform OCR on the image
        text = pytesseract.image_to_string(Image.open(image_path), lang=language)

        # Accumulate the extracted text
        accumulated_text += f'# Page {i+1}\n\n{text}\n\n'

        # Optionally, delete the temporary image file
        os.remove(image_path)

    # Save the accumulated text to the Markdown file if the flag is True
    if save_file:
        with open(markdown_path, 'w', encoding='utf-8') as md_file:
            md_file.write(accumulated_text)
        print('Text extraction complete. Markdown file saved as:', markdown_path)

    return accumulated_text


def display_text_and_markdown(pdf_path, output_folder, is_write=False):
    images = convert_from_path(pdf_path)
    markdown_content = pdf_to_markdown(pdf_path, output_folder, save_file=is_write)
    image_widgets = [widgets.Image(value=image._repr_png_(), format='png') for image in images]

    # Create Markdown widget
    markdown_widget = Markdown(markdown_content)

    # Create Output widget
    output_widget = Output()

    # Display Markdown widget inside the Output widget
    with output_widget:
        ipy_display(markdown_widget)
            # display()

    # Create HBox for side-by-side display
    hbox = widgets.HBox([widgets.VBox(image_widgets), output_widget])

    # Display side by side
    ipy_display(hbox)

# Define base path
base_path = r"C:\Users\Kaustubh_k\PycharmProjects\Marathi_RAG\pythonProject2"

display_text_and_markdown(
    pdf_path=os.path.join(base_path,"ToshieMaruki-FireOfHiroshima (1).pdf"),
    output_folder=os.path.join(base_path,"content"),
    is_write=True
)

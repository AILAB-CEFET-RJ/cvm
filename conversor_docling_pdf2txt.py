import sys
from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_path: str) -> str:
    # Convert PDF to Markdown
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    document_content = result.document.export_to_markdown()
    # document_content = remove_image_placeholder(document_content)
    # document_content = remove_extra_spaces(document_content)
    return document_content

if __name__ == "__main__":
    # Get file path from command line arguments
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "./data/resol175consolid.pdf"
    # For testing purposes, we can hardcode the path
    pdf_path = "./data/resol175consolid.pdf"

    # Convert PDF to Markdown
    markdown_content = convert_pdf_to_markdown(pdf_path)
    # print(markdown_content)
    # Get file name without extension
    file_name = pdf_path.split("/")[-1].split(".")[0]
    # Create a markdown file name
    markdown_file_name = f"{file_name}.md"
    # Save the markdown content to a file
    with open(markdown_file_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Markdown content saved to {markdown_file_name}")

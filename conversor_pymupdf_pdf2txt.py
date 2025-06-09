import sys
import pymupdf  # PyMuPDF

def convert_pdf_to_markdown(pdf_path: str) -> str:
    '''
    Convert PDF to Markdown with strikeout annotations.
    This function reads a PDF file, extracts text from each page. 
    The resulting Markdown content is returned as a string.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Markdown content with strikeout annotations.

    See: https://stackoverflow.com/questions/74533481/how-to-extract-text-with-strikethroughs-from-pdf-files-using-python
    '''
    doc = pymupdf.open(pdf_path)
    markdown_lines = []

    for page_number, page in enumerate(doc, start=1):
        text_instances = []
        strikeouts1 = []

        # Coletar os retângulos de anotações do tipo "strikeout"
        if page.annots():
            for annot in page.annots():
                if annot.type[0] == pymupdf.PDF_ANNOT_STRIKE_OUT:  # StrikeOut
                    print(f"Strikeout annotation found on page {page_number}: {annot.rect}")
                    # Adiciona o retângulo da anotação à lista de retângulos de strikeout
                    strikeouts1.append(annot.rect)

        # Coletar os retângulos de linhas horizontais e pseudo-linhas (retângulos com altura pequena)
        strikeouts2 = []  # to be filled with horizontal "lines": thin rectangles
        paths = page.get_drawings()  # list of drawing dictionary objects
        for path in paths:  # dictionary with single draw commands
            for item in path["items"]:  # check item types
                if item[0] in ("c", "qu"):  # skip curves and quads
                    continue
                if item[0] == "l":  # a true line
                    p1, p2 = item[1:]  # start / stop points
                    if p1.y != p2.y:  # skip non-horizontal lines
                        continue
                    # make a thin rectangle of height 2
                    rect = pymupdf.Rect(p1.x, p1.y - 1, p2.x, p2.y + 1)
                    strikeouts2.append(rect)
                    # print(f"Strikeout (line) annotation found on page {page_number}: {rect}")
                elif item[0] == "re":  # a rectangle, check if roughly a horizontal line
                    rect = item[1]  # the item's rectangle
                    if rect.width <= 2 * rect.height or rect.height > 4:
                        continue  # not a pseudo-line
                    strikeouts2.append(rect)
                    # print(f"Strikeout (rect) annotation found on page {page_number}: {rect}")

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        span_text = span["text"]
                        bbox = pymupdf.Rect(span["bbox"])
                        is_struck = any(bbox.intersects(strike_rect) for strike_rect in strikeouts1)
                        is_struck = any(bbox.intersects(strike_rect) for strike_rect in strikeouts2)
                        if is_struck:
                            span_text = f"~~{span_text}~~"
                            print(f"Strikeout annotation found on page {page_number}: {span_text}")
                        text_instances.append(span_text)

        page_text = " ".join(text_instances).strip()
        if page_text:
            markdown_lines.append(f"### Página {page_number}\n\n{page_text}\n")

    return "\n\n".join(markdown_lines)

if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "./data/resol175consolid.pdf"

    print(pymupdf.PDF_ANNOT_STRIKE_OUT)

    markdown_content = convert_pdf_to_markdown(pdf_path)

    file_name = pdf_path.split("/")[-1].split(".")[0]
    markdown_file_name = f"{file_name}.md"
    with open(markdown_file_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Markdown content saved to {markdown_file_name}")

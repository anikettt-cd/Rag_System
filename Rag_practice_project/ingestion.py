import pymupdf
import re
import psycopg2
from db import save_chunks

def extract_pages(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        pages.append({
            "page_number": page_number,
            "text": clean_text(text)
        })

    document.close()

    return pages


def clean_text(text):
    # 1. Remove zero-width and invisible Unicode characters
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)

    # 2. Replace non-breaking spaces with normal spaces
    text = text.replace('\xa0', ' ')

    # 3. Remove common PDF bullet artifacts at the beginning of lines
    text = re.sub(r'^[●•]\s*', '', text, flags=re.MULTILINE)

    # 4. Remove trailing spaces from every line
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)

    # 5. Replace multiple spaces/tabs with a single space
    text = re.sub(r'[ \t]+', ' ', text)

    # 6. Remove spaces directly before/after a newline
    text = re.sub(r' *\n *', '\n', text)

    # 7. Collapse 3+ consecutive newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 8. Remove spaces at the beginning/end of the whole text
    text = text.strip()

    return text


def is_heading(line):
    line = line.strip()

    if not line:
        return False

    # Very long lines are probably normal content
    if len(line) > 80:
        return False

    # Numbered headings/subsections
    if re.match(r'^\d+(\.\d+)*\.?\s+\S+', line):
        return True

    # Normal sentence punctuation means it is probably content
    if line.endswith((".", ",", ":", ";")):
        return False

    # Short title-like text
    words = line.split()

    if len(words) <= 8:
        return True

    return False


def detect_sections(text):
    lines = text.split("\n")

    sections = []
    current_section = "General"
    current_content = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if is_heading(line):

            # Save previous section
            if current_content:
                sections.append({
                    "section": current_section,
                    "text": " ".join(current_content)
                })

            # Start new section
            current_section = line
            current_content = []

        else:
            current_content.append(line)

    # Save final section
    if current_content:
        sections.append({
            "section": current_section,
            "text": " ".join(current_content)
        })

    return sections


def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):

        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def create_chunks(pages, document_id):
    chunks = []

    chunk_index = 0

    for page in pages:

        sections = detect_sections(page["text"])

        for section in sections:

            section_chunks = chunk_text(section["text"])

            for chunk in section_chunks:

                chunks.append({
                    "document_id": document_id,
                    "page_number": page["page_number"],
                    "section": section["section"],
                    "chunk_index": chunk_index,
                    "text": chunk
                })

                chunk_index += 1

    return chunks


from uuid import uuid4
from db import save_document, save_chunks
import os

pdf_path = "sample.pdf"

pages = extract_pages(pdf_path)

document_id = uuid4()

save_document(
    document_id=document_id,
    filename=os.path.basename(pdf_path),
    file_path=pdf_path,
    mime_type="application/pdf",
    file_size=os.path.getsize(pdf_path)
)

chunks = create_chunks(
    pages,
    document_id=document_id
)

save_chunks(chunks)
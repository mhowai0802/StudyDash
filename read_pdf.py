"""Extract text from PDFs in 000/ for summarization. Usage: python read_pdf.py [filename] (default: 01.pdf)"""
import sys
from pathlib import Path

# Support running from project root or backend
root = Path(__file__).resolve().parent
name = sys.argv[1] if len(sys.argv) > 1 else "01.pdf"
pdf_path = root / "000" / name
if not pdf_path.exists():
    pdf_path = root / name
if not pdf_path.exists():
    print(f"PDF not found: {name}", file=sys.stderr)
    sys.exit(1)

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 not installed. Run: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)

reader = PdfReader(str(pdf_path))
text_parts = []
for i, page in enumerate(reader.pages):
    t = page.extract_text()
    if t:
        text_parts.append(t)

full_text = "\n\n".join(text_parts)
# Write to file to avoid console encoding issues (UTF-8)
stem = Path(name).stem
out_path = root / "000" / f"{stem}_extracted.txt"
out_path.parent.mkdir(parents=True, exist_ok=True)
max_len = 80000
with open(out_path, "w", encoding="utf-8") as f:
    f.write(full_text[:max_len])
    if len(full_text) > max_len:
        f.write("\n\n[... truncated ...]")
print(f"Extracted {len(full_text)} chars to {out_path}")

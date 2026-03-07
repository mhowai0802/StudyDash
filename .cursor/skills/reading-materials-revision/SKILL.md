---
name: reading-materials-revision
description: Helps with reading materials for revision by first giving a concise summary, then offering or providing detailed explanations. Use when the user asks for a summary of a document, revision help, "read this" or "teach me" from PDFs or other reading materials.
---

# Reading Materials for Revision

## Workflow

When helping the user revise from reading materials (PDFs, docs, notes):

1. **Summary first** – Provide a short, structured overview before any deep detail.
2. **Details after** – Offer or give detailed explanations, either in the same response (if brief) or on request.

## Response Structure

### 1. Summary (always first)

- **One short paragraph** or **bullet list** of main points.
- Include: title/topic, 3–7 key ideas or sections, and main takeaway.
- Keep it scannable (headings, bullets, optional short table).

### 2. Details (then or on request)

For **each section**, follow this structure:

1. **Definition / concept** – What is it, in plain words.
2. **Why it matters** – Motivation or use case (one sentence is enough).
3. **Worked example** – A concrete, small example that shows how it works (numbers, images, or code snippets from the material). This is mandatory; never skip it.
4. **Key takeaway** – One-liner the student should remember.

- Use clear headings so the user can jump to a section (e.g. "Explain sampling" or "More on color models").
- End with a short recap or checklist covering all sections.

## Trigger Scenarios

Apply this skill when the user:

- Asks for a "summary" of a document or file.
- Says "read this", "help me revise", "teach me" from notes or slides.
- References a PDF or doc (e.g. `@000/02.pdf`) for study or revision.
- Asks to "explain in detail" after a summary has been given.

## PDF Content

If the material is a PDF:

- Prefer extracting text via project tooling (e.g. venv + `read_pdf.py` or PyPDF2) and working from extracted text.
- If extraction fails or is partial, say so and work from whatever text or structure is available; still follow summary-first then details.

## Example Flow

**User:** "Summary of 02.pdf?"

**Agent:**  
1. Extract/read content.  
2. Reply with **Summary** (short overview, key points).  
3. Then: "I can go into detail on any section (e.g. X, Y, Z). Say which part you want."

**User:** "Explain X in detail."

**Agent:**  
For section X, provide:
1. Definition / concept in plain words.
2. Why it matters (one sentence).
3. Worked example with concrete numbers or visuals from the material.
4. Key takeaway (one-liner to remember).

Repeat this pattern for every section covered.

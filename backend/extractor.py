import pdfplumber
import re
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_PATH = os.path.join(BASE_DIR, "skills.json")

def extract_text(pdf):
    with pdfplumber.open(pdf) as f:
        text = ""
        for page in f.pages:
            text += page.extract_text() or ""
    return text

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s-]{7,15}', text)
    return match.group(0) if match else None
with open(SKILL_PATH, "r") as f:

    SKILL_LIST = json.load(f)

def extract_skills(text):
    text = text.lower()

    found = []

    for skill in SKILL_LIST:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))

def extract_github_username(pdf):
    """Extract username from clickable links or text."""
    import pdfplumber
    import re

    username = None

    with pdfplumber.open(pdf) as pdf_file:
        for page in pdf_file.pages:

            # ---- 1. Extract hyperlink annotations ----
            if page.annots:
                for annot in page.annots:
                    uri = annot.get("uri", "")
                    if "github.com" in uri:
                        match = re.search(r"github\.com/([A-Za-z0-9\-_\.]+)", uri)
                        if match:
                            return match.group(1)

            # ---- 2. Extract text-based URLs ----
            text = page.extract_text() or ""
            match = re.search(r"github\.com/([A-Za-z0-9\-_\.]+)", text)
            if match:
                return match.group(1)

    return None


def extract_sections(text):
    lines = text.split("\n")
    current = None
    out = {"experience": "", "projects": "", "education": ""}

    for line in lines:
        l = line.lower()
        if "experience" in l: current = "experience"
        elif "project" in l: current = "projects"
        elif "education" in l: current = "education"
        elif current:
            out[current] += line + "\n"

    return out

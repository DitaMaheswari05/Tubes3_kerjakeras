import re

def extract_cv_summary(text: str) -> dict:
    """
    Ekstrak ringkasan CV dari teks hasil ekstraksi PDF.
    Return dict: skills, job, education.
    """
    skills = []
    m = re.search(r'Skills?\s*[:\-]?\s*(.+?)(\n\n|\Z)', text, re.IGNORECASE | re.DOTALL)
    if m:
        skills = [s.strip() for s in re.split(r',|\n', m.group(1)) if s.strip()]

    # Pengalaman kerja
    job = []
    for m in re.finditer(r'(\d{4})\s*-\s*(\d{4}|Present).*\n(.+)', text):
        job.append({
            "start": m.group(1),
            "end": m.group(2),
            "position": m.group(3).strip()
        })

    education = []
    for m in re.finditer(r'(\d{4})\s*-\s*(\d{4}|Present).*\n(.+),\s*(.+)', text):
        education.append({
            "start": m.group(1),
            "end": m.group(2),
            "university": m.group(3).strip(),
            "degree": m.group(4).strip()
        })

    return {
        "skills": skills,
        "job": job,
        "education": education
    }
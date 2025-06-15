import re

skill_sections = [
    "skills", "skill highlights", "summary of skills"
]

experience_sections = [
    "work history", "work experience", "experience",
    "professional experience", "professional history"
]

education_sections = [
    "education", "education and training", "educational background",
    "teaching experience", "corporate experience"
]

all_sections = skill_sections + experience_sections + education_sections + [
    "summary", "highlights", "professional summary", "core qualifications", "languages",
    "professional profile", "relevant experience", "affiliations", "certifications", "qualifications",
    "accomplishments", "additional information", "core accomplishments", "career overview", "core strengths",
    "interests", "professional affiliations", "online profile", "certifications and trainings", "credentials",
    "personal information", "career focus", "executive profile", "military experience", "community service",
    "presentations", "publications", "community leadership positions", "license", "computer skills",
    "volunteer work", "awards and publications", "activities and honors", "volunteer associations"
]

def extract_skills(text: str) -> list[str]:
    pattern = f"\n({'|'.join(map(re.escape, skill_sections))})\n(.*?)(\n({'|'.join(map(re.escape, all_sections))})\n|$)"
    m = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        body = m.group(2).strip()
        skills = [s.strip() for s in re.split(r',|\n|;', body) if s.strip()]
        return skills
    return []

    
def extract_education(text: str) -> list[str]:
    patterns = [
        r"university of [a-zA-Z ]+",
        r"[a-zA-Z ]+ university",
        r"[a-zA-Z ]+ college",
        r"college of [a-zA-Z ]+",
        r"[a-zA-Z ]* institute of [a-zA-Z ]+",
        r"[a-zA-Z ]+ institute",
        r"[a-zA-Z ]+ high school",
        r"[a-zA-Z ]+ seminary",
        r"[a-zA-Z ]+ center",
        r"[a-zA-Z ]+ training program"
    ]

    education_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        education_matches.extend(matches)

    cleaned = list({match.strip() for match in education_matches if match.strip()})
    return cleaned


def extract_job(text: str) -> list[str]:
    pattern = f"\n({'|'.join(map(re.escape, experience_sections))})\n(.*?)(\n({'|'.join(map(re.escape, all_sections))})\n|$)"
    m = re.search(pattern, flags=re.IGNORECASE | re.DOTALL, string=text)
    if not m:
        return []

    body = m.group(2)
    lines = body.splitlines()
    keywords = [
        "Director", "Manager", "Analyst", "Specialist", "Recruiter", "Representative",
        "Coordinator", "Lead", "Consultant", "Volunteer", "Assistant", "Technician",
        "Supervisor", "Associate", "Intern", "Counselor", "Advocate"
    ]
    results = []
    for line in lines:
        for kw in keywords:
            if kw.lower() in line.lower():
                found = re.findall(rf"[A-Z][a-zA-Z ]*{kw}[a-zA-Z ]*", line)
                results.extend(found)
                break
    return list(set(results))


def extract_cv_summary(text: str) -> dict:
    return {
        "skills": extract_skills(text),
        "job": extract_job(text),
        "education": extract_education(text)
    }
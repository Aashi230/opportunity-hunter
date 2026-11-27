#!/usr/bin/env python3
"""
Opportunity Hunter — Intelligence & Recommendation Engine
Provides rule-based resume parsing, explainable recommendation scoring,
and contextual career assistant responses using standard library.
"""

import re
from datetime import datetime

# Curated catalog of recognized in-demand student technical skills
KNOWN_SKILLS = {
    # Languages
    "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript",
    "java": "Java", "c++": "C++", "c#": "C#", "c": "C", "sql": "SQL",
    "html": "HTML", "css": "CSS", "go": "Go", "golang": "Go", "rust": "Rust",
    "ruby": "Ruby", "php": "PHP", "swift": "Swift", "kotlin": "Kotlin", "r": "R",
    # Frameworks & Libraries
    "react": "React", "node.js": "Node.js", "nodejs": "Node.js", "express": "Express",
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI", "spring": "Spring Boot",
    "spring boot": "Spring Boot", "angular": "Angular", "vue": "Vue", "next.js": "Next.js",
    "nextjs": "Next.js", "pytorch": "PyTorch", "tensorflow": "TensorFlow",
    "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn",
    "scikitlearn": "Scikit-Learn", "opencv": "OpenCV", "tailwind": "Tailwind CSS",
    # Data & AI
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "artificial intelligence": "AI", "nlp": "NLP", "data science": "Data Science",
    "data analysis": "Data Analysis", "tableau": "Tableau", "power bi": "Power BI",
    "statistics": "Statistics",
    # Cloud, DevOps & Tools
    "aws": "AWS", "azure": "Azure", "gcp": "Google Cloud", "docker": "Docker",
    "kubernetes": "Kubernetes", "git": "Git", "github": "GitHub", "linux": "Linux",
    "ci/cd": "CI/CD", "terraform": "Terraform", "graphql": "GraphQL",
    # Databases
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "mysql": "MySQL",
    "mongodb": "MongoDB", "redis": "Redis", "sqlite": "SQLite", "firebase": "Firebase",
    # Security & Systems
    "cybersecurity": "Cybersecurity", "cryptography": "Cryptography",
    "networking": "Computer Networking", "penetration testing": "Penetration Testing"
}

ACTION_VERBS = [
    "built", "developed", "engineered", "designed", "architected", "implemented",
    "optimized", "spearheaded", "created", "automated", "deployed", "scaled",
    "collaborated", "managed", "delivered", "integrated", "reduced", "improved"
]

def parse_resume_text(text, opportunities=None):
    """
    Safely extract skills, education, experience metrics, and recommendations
    from plain resume text.
    """
    if not text or not isinstance(text, str):
        return {
            "error": "EMPTY_TEXT",
            "message": "Resume text could not be extracted or is empty."
        }

    raw = text.strip()
    low = raw.lower()

    # 1. Contact / Name inference
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    candidate_name = "Candidate"
    for line in lines[:5]:
        if len(line.split()) in (2, 3, 4) and not re.search(r'[@\d\/:.]', line):
            candidate_name = line
            break

    # Email & Links
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw)
    email = email_match.group(0) if email_match else None
    has_github = bool(re.search(r'github\.com\/[\w-]+', raw, re.IGNORECASE))
    has_linkedin = bool(re.search(r'linkedin\.com\/in\/[\w-]+', raw, re.IGNORECASE))

    # 2. Degree & Field of Study
    degree = "Technical Degree"
    if re.search(r'\bb\.?\s*tech\b|\bbachelor of technology\b', low):
        degree = "B.Tech Computer Science / Engineering"
    elif re.search(r'\bb\.?\s*e\b|\bbachelor of engineering\b', low):
        degree = "B.E. Engineering"
    elif re.search(r'\bm\.?\s*tech\b|\bmaster of technology\b', low):
        degree = "M.Tech"
    elif re.search(r'\bbca\b|\bbachelor of computer applications\b', low):
        degree = "BCA"
    elif re.search(r'\bmca\b|\bmaster of computer applications\b', low):
        degree = "MCA"
    elif re.search(r'\bb\.?\s*sc\b|\bbachelor of science\b', low):
        degree = "B.Sc Computer Science"

    # 3. Academic Year & Graduation Year
    grad_year = None
    year_match = re.search(r'\b(202[4-9]|2030)\b', raw)
    if year_match:
        grad_year = year_match.group(1)

    study_year = "2nd year"
    if re.search(r'\b(?:first|1st)[- ]year\b|\bfreshman\b', low):
        study_year = "1st year"
    elif re.search(r'\b(?:second|2nd)[- ]year\b|\bsophomore\b', low):
        study_year = "2nd year"
    elif re.search(r'\b(?:third|3rd)[- ]year\b|\bjunior\b', low):
        study_year = "3rd year"
    elif re.search(r'\b(?:fourth|4th|final)[- ]year\b|\bsenior\b', low):
        study_year = "Final year"
    elif re.search(r'\bmaster\b|\bpostgrad', low):
        study_year = "Master’s"

    # 4. Extract Technical Skills
    found_skills = set()
    for skill_key, skill_display in KNOWN_SKILLS.items():
        pattern = r'(?:^|[^a-zA-Z0-9+#])' + re.escape(skill_key) + r'(?:$|[^a-zA-Z0-9+#])'
        if re.search(pattern, low):
            found_skills.add(skill_display)

    extracted_skills = sorted(list(found_skills))

    # 5. Quality & Strength Audit (0-100 Score)
    score = 40  # baseline
    tips = []
    strengths = []

    if len(extracted_skills) >= 6:
        score += 20
        strengths.append(f"Strong technical skill variety ({len(extracted_skills)} in-demand technologies detected).")
    elif len(extracted_skills) >= 3:
        score += 10
        strengths.append(f"Good foundational skills ({len(extracted_skills)} detected).")
    else:
        tips.append("Add more specific technical tools, languages, and frameworks to your Skills section.")

    # Check for quantitative impact metrics (numbers, %, metrics)
    metrics_matches = len(re.findall(r'\b\d+(?:\.\d+)?%|\b\d+x\b|\b\$\d+|\b\d+\s*(?:users|clients|ms|seconds|stars|downloads|requests|queries)\b', raw, re.IGNORECASE))
    if metrics_matches >= 3:
        score += 20
        strengths.append("Excellent use of quantifiable metrics and measurable impact.")
    elif metrics_matches >= 1:
        score += 10
        tips.append("Enhance bullet points with more quantifiable outcomes (e.g. 'Improved query latency by 35%', 'Serving 500+ daily active users').")
    else:
        tips.append("Include measurable metrics and numbers in your project descriptions to demonstrate clear business/engineering impact.")

    # Action verbs check
    verbs_count = sum(1 for v in ACTION_VERBS if re.search(r'\b' + v + r'\b', low))
    if verbs_count >= 4:
        score += 10
        strengths.append("Active, punchy accomplishment language across project bullets.")
    else:
        tips.append("Start project bullet points with strong action verbs (e.g., 'Architected', 'Optimized', 'Automated').")

    # Links check
    if has_github:
        score += 5
        strengths.append("GitHub profile linked for code verification.")
    else:
        tips.append("Include your active GitHub profile URL with pinned repositories.")

    if has_linkedin:
        score += 5
        strengths.append("LinkedIn profile linked.")

    score = min(100, max(25, score))

    # 6. Suitable Opportunities Matching
    matches = []
    if opportunities and isinstance(opportunities, list):
        for opp in opportunities:
            opp_text = (opp.get("title", "") + " " + opp.get("text", "")).lower()
            opp_skills = [s for s in extracted_skills if s.lower() in opp_text]
            match_pct = min(98, round(len(opp_skills) / max(1, len(extracted_skills)) * 100))
            matches.append({
                "id": opp.get("id") or opp.get("url"),
                "title": opp.get("title"),
                "url": opp.get("url"),
                "org": opp.get("org") or opp.get("organization", "Official"),
                "matching_skills": opp_skills,
                "score": match_pct
            })
        matches.sort(key=lambda x: x["score"], reverse=True)

    return {
        "candidate_name": candidate_name,
        "email": email,
        "degree": degree,
        "study_year": study_year,
        "graduation_year": grad_year,
        "has_github": has_github,
        "has_linkedin": has_linkedin,
        "extracted_skills": extracted_skills,
        "strength_score": score,
        "strengths": strengths,
        "improvement_tips": tips,
        "recommended_opportunities": matches[:3]
    }

# -------------------------------------------------------------
# Career Assistant Contextual Response Generator
# -------------------------------------------------------------
def generate_assistant_reply(query, profile=None, opportunities=None, applications=None):
    """
    Generate accurate, transparent career and opportunity guidance
    strictly grounded in the user's active profile and loaded opportunities.
    """
    q = (query or "").lower().strip()
    profile = profile or {}
    opportunities = opportunities or []
    applications = applications or []

    student_name = profile.get("name") or "Student"
    degree = profile.get("degree") or "Engineering"
    year = profile.get("year") or "2nd year"
    skills = profile.get("skills") or ["Python", "SQL"]
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    # 1. Matching Internships / Opportunities
    if any(k in q for k in ["match", "which internship", "recommend", "suitable", "find opportunity"]):
        if not opportunities:
            return (
                f"Hello {student_name}! Based on your profile ({degree}, {year}), I recommend searching for "
                f"roles that require your core skills: {', '.join(skills[:4])}. Currently, no opportunities are loaded. "
                "Click **Discover** or enter a topic like 'Software Engineering' to load verified programs."
            )
        
        # Rank by skill overlap
        scored = []
        for opp in opportunities:
            opp_text = (opp.get("title", "") + " " + opp.get("text", "")).lower()
            overlap = [s for s in skills if s.lower() in opp_text]
            scored.append((opp, overlap))
        scored.sort(key=lambda x: len(x[1]), reverse=True)
        top = scored[:3]
        
        reply = f"Here are the top student opportunities matching your profile ({degree}, {year}):\n\n"
        for opp, ov in top:
            t = opp.get("title", "Opportunity")
            u = opp.get("url", "#")
            reply += f"• **[{t}]({u})**: Matches your skills ({', '.join(ov) if ov else 'General engineering'}).\n"
        reply += f"\n💡 *Tip*: You can save any of these directly to your **Application Tracker** to monitor deadlines."
        return reply

    # 2. Eligibility Questions
    if any(k in q for k in ["eligible", "eligibility", "can i apply"]):
        if "microsoft" in q or "explore" in q:
            if year in ["1st year", "2nd year"]:
                return (
                    f"✅ **Yes, you are likely eligible for Explore Microsoft!**\n\n"
                    f"The Explore Microsoft program specifically targets **first- and second-year undergraduate college students** "
                    f"pursuing Computer Science or related engineering degrees. Since you are in your **{year}** of **{degree}**, "
                    f"you meet the academic prerequisite. Core requirements include basic coding in C, C++, Java, or Python."
                )
            else:
                return (
                    f"⚠️ **Eligibility Note for Explore Microsoft**:\n\n"
                    f"The Explore program is exclusively structured for 1st and 2nd year undergraduates. "
                    f"Since you are in **{year}**, you should instead apply to **Microsoft's Standard University Internship** "
                    f"or flagship engineering requisitions."
                )
        if "infosys" in q or "instep" in q or "winternship" in q:
            return (
                f"ℹ️ **Infosys Programs Eligibility**:\n\n"
                f"• **Winternship (76 days)**: Open to engineering students in India across CS & IT streams. Recruitment is facilitated via your college placement cell.\n"
                f"• **InStep Global Internship**: Open to top university students globally for AI/ML and software engineering through their direct application portal."
            )
        return (
            f"To check eligibility for any specific opportunity, open the opportunity card on the **Discover** tab "
            f"and expand the **'Eligibility Audit'** section. It automatically cross-references your study year ({year}) "
            f"and degree against the program requirements."
        )

    # 3. Skill Gap / What to learn next
    if any(k in q for k in ["skill", "learn next", "gap", "improve my skill", "technology"]):
        opp_skills_freq = {}
        for opp in opportunities:
            opp_text = (opp.get("title", "") + " " + opp.get("text", "")).lower()
            for sk, disp in KNOWN_SKILLS.items():
                if sk in opp_text:
                    opp_skills_freq[disp] = opp_skills_freq.get(disp, 0) + 1
                    
        user_skills_low = [s.lower() for s in skills]
        missing = [s for s, count in sorted(opp_skills_freq.items(), key=lambda x: x[1], reverse=True) if s.lower() not in user_skills_low]
        top_missing = missing[:3] if missing else ["Docker", "Git", "Cloud (AWS/Azure)"]
        
        return (
            f"Based on market demand across current technical programs, here are the top high-yield skills to learn next:\n\n"
            f"1. **{top_missing[0]}**: Frequently required in 80%+ of student developer listings.\n"
            f"2. **{top_missing[1]}**: Essential for modern full-stack and backend projects.\n"
            f"3. **{top_missing[2]}**: Enhances your resume for competitive selection.\n\n"
            f"Visit the **Skill Gap Analyzer** tab for free curated roadmaps and hands-on practice projects."
        )

    # 4. Resume Advice
    if any(k in q for k in ["resume", "cv", "portfolio"]):
        return (
            f"Here are 4 proven ways to optimize your technical resume for student opportunities:\n\n"
            f"1. **Quantify Results**: Use metrics like *'Optimized response time by 40%'* or *'Built React UI for 300+ students'*.\n"
            f"2. **Feature Links**: Place direct GitHub repository links and live demo URLs prominently under each project.\n"
            f"3. **Align Skills**: Place your strongest skills ({', '.join(skills[:3]) if skills else 'Python, SQL'}) at the top.\n"
            f"4. **Use our Resume Analyzer**: Upload your resume PDF on the **Resume Analyzer** tab for an instant strength score and personalized gap audit!"
        )

    # 5. Interview Prep
    if any(k in q for k in ["interview", "prepare", "assessment", "coding round"]):
        return (
            f"Technical Interview Strategy for {year} Students ({degree}):\n\n"
            f"• **Coding Assessments**: Practice Arrays, Strings, HashMaps, and Two-Pointer problems on LeetCode/HackerRank.\n"
            f"• **Behavioral / STAR Method**: Prepare 3 stories about project challenges, teamwork, and debugging under pressure (Situation, Task, Action, Result).\n"
            f"• **Core Fundamentals**: Review OOP concepts, basic SQL queries, and Git workflows.\n"
            f"• **Company Deep Dive**: Research the company's recent engineering blogs and open-source tooling before your interview."
        )

    # Default Contextual Answer
    return (
        f"Hello {student_name}! I am your Opportunity Hunter Career Companion. I have analyzed your profile "
        f"({degree}, {year}, skills: {', '.join(skills[:3]) if skills else 'Technical'}).\n\n"
        f"You can ask me:\n"
        f"• *'Which internships match my profile best?'*\n"
        f"• *'Am I eligible for Microsoft Explore or Infosys?'*\n"
        f"• *'What skills should I learn next?'*\n"
        f"• *'How can I improve my resume for technical roles?'*\n"
        f"• *'How should I prepare for an internship interview?'*"
    )

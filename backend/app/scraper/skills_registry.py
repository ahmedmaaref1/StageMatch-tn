"""
skills_registry.py — Specialized Tech & IT Skills Registry for Tunisia

Covers 6 Specialized Tech Tracks:
1. Web & Fullstack Development
2. Backend & Microservices Engineering
3. Artificial Intelligence & Data Science
4. DevOps, Cloud & Infrastructure
5. Mobile Application Development
6. Cybersecurity, Networks & Systems
"""

import re

# ── 6 SPECIALIZED TECH TRACKS ──────────────────────────────────────────────────

TECH_TRACKS = {
    "Web & Fullstack": {
        "keywords": [
            "fullstack", "full stack", "frontend", "front-end", "web developer",
            "développeur web", "react", "angular", "vue", "next.js", "nextjs", "javascript",
            "typescript", "html", "css", "tailwind", "node.js", "nodejs", "wordpress", "php",
            "laravel", "symfony", "web"
        ],
        "skills": [
            "React", "React.js", "Vue.js", "Angular", "Next.js", "Node.js", "Express.js",
            "TypeScript", "JavaScript", "HTML5", "CSS3", "TailwindCSS", "Bootstrap",
            "Sass", "Redux", "GraphQL", "REST API", "WordPress", "PHP", "Laravel"
        ]
    },

    "Backend & Microservices": {
        "keywords": [
            "backend", "back-end", "développeur python", "développeur java", "spring boot",
            "fastapi", "django", "microservices", "microservice", "api rest", "apis rest",
            "rest api", "golang", "c#", ".net", "java", "python", "spring", "flask",
            "postgresql", "mongodb", "sql", "c++", "logiciel"
        ],
        "skills": [
            "Python", "FastAPI", "Django", "Flask", "Java", "Spring Boot", "C#", ".NET",
            "Golang", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "SQLAlchemy", "Hibernate", "Kafka", "RabbitMQ", "Microservices", "REST API"
        ]
    },

    "IA, Data & Machine Learning": {
        "keywords": [
            "intelligence artificielle", "machine learning", "deep learning", "data science",
            "data engineer", "data analyst", "nlp", "computer vision", "llm", "transformers",
            "ia", "data", "big data", "etl", "pandas", "pytorch", "tensorflow", "power bi",
            "business intelligence", "bi", "analytics"
        ],
        "skills": [
            "Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "PyTorch", "TensorFlow", "Keras", "scikit-learn", "Pandas", "NumPy",
            "Hugging Face", "Transformers", "LLM", "LangChain", "OpenCV", "Power BI",
            "Spark", "Databricks", "Data Mining"
        ]
    },

    "DevOps & Cloud": {
        "keywords": [
            "devops", "cloud", "docker", "kubernetes", "k8s", "ci/cd", "ci-cd", "aws",
            "azure", "gcp", "terraform", "ansible", "linux", "sysadmin", "infrastructure",
            "gitlab", "jenkins", "systeme", "système", "serveur", "nginx", "grafana"
        ],
        "skills": [
            "Docker", "Kubernetes", "CI/CD", "GitHub Actions", "GitLab CI", "Jenkins",
            "AWS", "Microsoft Azure", "GCP", "Terraform", "Ansible", "Linux", "Bash",
            "Nginx", "Prometheus", "Grafana", "Git", "Helm"
        ]
    },

    "Mobile Development": {
        "keywords": [
            "mobile", "flutter", "dart", "react native", "android", "ios", "swift",
            "kotlin", "développeur mobile", "cross-platform", "ionic", "application mobile",
            "app mobile"
        ],
        "skills": [
            "Flutter", "Dart", "React Native", "Android", "Kotlin", "iOS", "Swift",
            "Java Android", "Firebase", "SQLite", "Mobile UI"
        ]
    },

    "Cybersécurité & Réseaux": {
        "keywords": [
            "sécurité", "cybersécurité", "cybersecurity", "pentest", "pentesting", "soc",
            "réseaux", "reseau", "network", "firewall", "siem", "ethical hacking", "infosec",
            "wireshark", "cisco", "audit securite", "télécom", "telecom", "iso 27001", "vpn"
        ],
        "skills": [
            "Cybersécurité", "Pentesting", "Ethical Hacking", "Wireshark", "Metasploit",
            "SIEM", "SOC", "Firewall", "Cisco", "TCP/IP", "VPN", "Linux Security",
            "ISO 27001", "Cryptographie"
        ]
    }
}

# ── TUNISIAN CITIES / TECH HUBS ───────────────────────────────────────────────

TUNISIAN_CITIES = [
    "Tunis", "Ariana", "Ben Arous", "Manouba", "Sousse", "Sfax", "Monastir",
    "Nabeul", "Bizerte", "Gabès", "Kairouan", "Gafsa", "Mahdia", "Médenine",
    "Béja", "Jendouba", "Kasserine", "Kébili", "Le Kef", "Sidi Bouzid",
    "Siliana", "Tataouine", "Tozeur", "Zaghouan",
    # Major Tech Parks in Tunisia
    "El Ghazala", "Les Berges du Lac", "Centre Urbain Nord", "Charguia"
]


def extract_skills_from_text(text: str) -> list[str]:
    """
    Extracts technical skills from text using strict regex boundaries.
    """
    found = []
    text_lower = text.lower()

    for track_data in TECH_TRACKS.values():
        for skill in track_data["skills"]:
            # Short acronyms (e.g. "R", "C#", "Go", "AWS", "GCP", "SQL")
            if len(skill) <= 3 or skill in ["C#", ".NET"]:
                pattern = r'(?i)\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text):
                    found.append(skill)
            else:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(skill)

    # Return unique skills preserving casing
    return list(set(found))


def detect_tech_track(title: str, description: str) -> str:
    """
    Detects which of the 6 Tech Tracks an offer belongs to.
    Title matches are weighted 4x compared to description.
    Falls back to extracted skill signatures before defaulting.
    """
    title_lower = title.lower()
    desc_lower = description.lower()

    best_track = None
    highest_score = 0

    for track_name, track_data in TECH_TRACKS.items():
        score = 0
        for keyword in track_data["keywords"]:
            if keyword in title_lower:
                score += 4
            elif keyword in desc_lower:
                score += 1

        if score > highest_score:
            highest_score = score
            best_track = track_name

    # If keywords matched with confidence
    if best_track and highest_score >= 1:
        return best_track

    # Fallback: check skills explicitly extracted
    extracted = extract_skills_from_text(f"{title} {description}")
    for skill in extracted:
        for track_name, track_data in TECH_TRACKS.items():
            if skill in track_data["skills"]:
                return track_name

    return "Web & Fullstack"


def normalize_city(city_text: str) -> str:
    if not city_text:
        return "Tunisie"

    city_lower = city_text.lower()
    for city in TUNISIAN_CITIES:
        pattern = r'\b' + re.escape(city.lower()) + r'\b'
        if re.search(pattern, city_lower):
            return city

    return "Tunisie"


def get_all_tracks() -> list[str]:
    return list(TECH_TRACKS.keys())

# ── COMPLETE DIRECTORY OF TUNISIAN TECH INSTITUTIONS ──────────────────────────

V, U, C = "verified", "unverified", "check"

INSTITUTIONS = [
    # ── Public engineering schools ─────────────────────────────────────────
    ("ENSI (École Nationale des Sciences de l'Informatique - Manouba)", "public_engineering", U),
    ("INSAT (Institut National des Sciences Appliquées et de Technologie)", "public_engineering", U),
    ("SUP'COM (École Supérieure des Communications de Tunis)", "public_engineering", U),
    ("ENIT (École Nationale d'Ingénieurs de Tunis)", "public_engineering", U),
    ("ENISo (École Nationale d'Ingénieurs de Sousse)", "public_engineering", V),
    ("ENIS (École Nationale d'Ingénieurs de Sfax)", "public_engineering", U),
    ("ENIM (École Nationale d'Ingénieurs de Monastir)", "public_engineering", V),
    ("ENIG (École Nationale d'Ingénieurs de Gabès)", "public_engineering", U),
    ("ENSIT (École Nationale Supérieure d'Ingénieurs de Tunis)", "public_engineering", U),
    ("EPT (École Polytechnique de Tunisie - La Marsa)", "public_engineering", U),
    ("ENIB (École Nationale d'Ingénieurs de Bizerte)", "public_engineering", U),
    ("ENICarthage (École Nationale d'Ingénieurs de Carthage)", "public_engineering", V),
    ("INTEK (Institut National des Technologies et des Sciences du Kef)", "public_engineering", V),

    # ── Public IT / multimedia institutes ──────────────────────────────────
    ("ISI (Institut Supérieur d'Informatique - Ariana / El Manar)", "public_it", U),
    ("ISITCom (Institut Supérieur d'Informatique et des Technologies de Communication - Hammam Sousse)", "public_it", U),
    ("ISIMM (Institut Supérieur d'Informatique et de Mathématiques de Monastir)", "public_it", V),
    ("ISIK (Institut Supérieur d'Informatique du Kef)", "public_it", V),
    ("ISLAIB (Institut Supérieur des Langues Appliquées et d'Informatique de Béja)", "public_it", V),
    ("ISIMS (Institut Supérieur d'Informatique et de Multimédia de Sfax)", "public_it", U),
    ("ISIMG (Institut Supérieur d'Informatique et de Multimédia de Gabès)", "public_it", U),
    ("ISAMM (Institut Supérieur des Arts Multimédia de la Manouba)", "public_it", V),
    ("ISIGK (Institut Supérieur d'Informatique et de Gestion de Kairouan)", "public_it", U),
    ("ISG Tunis (Informatique de Gestion & Business Analytics)", "public_it", U),
    ("ESSTHS (École Supérieure des Sciences et de la Technologie de Hammam Sousse)", "public_it", U),
    ("ESCT (École Supérieure de Commerce de Tunis - Business Computing)", "public_it", V),
    ("UVT (Université Virtuelle de Tunis)", "public_it", V),

    # ── ISSAT network ──────────────────────────────────────────────────────
    ("ISSAT Sousse", "public_issat", V),
    ("ISSAT Mahdia", "public_issat", U),
    ("ISSAT Kairouan", "public_issat", U),
    ("ISSAT Gafsa", "public_issat", U),
    ("ISSAT Kasserine", "public_issat", V),
    ("ISSAT Mateur", "public_issat", V),

    # ── Faculties of Science ───────────────────────────────────────────────
    ("FST (Faculté des Sciences de Tunis - El Manar)", "faculty", U),
    ("FSS (Faculté des Sciences de Sfax)", "faculty", V),
    ("FSM (Faculté des Sciences de Monastir)", "faculty", U),
    ("FSB (Faculté des Sciences de Bizerte)", "faculty", V),
    ("FSG (Faculté des Sciences de Gabès)", "faculty", U),
    ("FSGafsa (Faculté des Sciences de Gafsa)", "faculty", U),

    # ── ISET network ───────────────────────────────────────────────────────
    ("ISET'Com (Technopôle El Ghazala)", "iset", V),
    ("ISET Rades", "iset", U),
    ("ISET Sousse", "iset", U),
    ("ISET Sfax", "iset", U),
    ("ISET Nabeul", "iset", U),
    ("ISET Bizerte", "iset", U),
    ("ISET Kélibia", "iset", U),
    ("ISET Mahdia", "iset", U),
    ("ISET Djerba", "iset", U),
    ("ISET Gabès", "iset", U),
    ("ISET Kairouan", "iset", U),
    ("ISET Gafsa", "iset", U),
    ("ISET Kasserine", "iset", U),
    ("ISET Béja", "iset", U),
    ("ISET Jendouba", "iset", V),
    ("ISET Le Kef", "iset", U),
    ("ISET Siliana", "iset", U),
    ("ISET Sidi Bouzid", "iset", U),
    ("ISET Tozeur", "iset", U),
    ("ISET Médenine", "iset", U),
    ("ISET Tataouine", "iset", U),
    ("ISET Zaghouan", "iset", U),
    ("ISET Charguia", "iset", U),
    ("ISET Kébili", "iset", U),

    # ── Private engineering schools: OIT-accredited / recognized ───────────
    ("ESPRIT (École Supérieure Privée d'Ingénierie et de Technologies)", "private_engineering", V),
    ("TEK-UP (El Ghazala)", "private_engineering", V),
    ("SESAME (École Supérieure Privée des Sciences Appliquées et de Management)", "private_engineering", V),
    ("Polytechnique Intl (Lac Tunis)", "private_engineering", V),
    ("Iteam University (ESPRIT-IAA)", "private_engineering", V),
    ("ESIET - Université Arabe des Sciences (UAS, Tunis)", "private_engineering", V),
    ("UPES Mégrine", "private_engineering", V),
    ("ESPITA (École Supérieure Privée d'Ingénierie et Technologie Appliquée)", "private_engineering", V),
    ("IT Business School (Nabeul)", "private_engineering", V),
    ("ESAT (École Supérieure Privée de l'Aéronautique et des Technologies)", "private_engineering", V),
    ("IPSAS (Institut Privé Polytechnique des Sciences Avancées de Sfax)", "private_engineering", V),
    ("IIT (École Supérieure Internationale Privée de Technologie - Sfax)", "private_engineering", V),
    ("ULT (Université Libre de Tunis)", "private_engineering", V),
    ("POLYTECH Sousse (École Polytechnique Privée de Sousse)", "private_engineering", V),
    ("École Supérieure Privée d'Ingénieurs de Monastir", "private_engineering", V),
    ("MedTech / SMU (South Mediterranean University - Lac 2)", "private_engineering", C),
    ("Centrale School of IT & Telecom (Honoris)", "private_engineering", C),
    ("EPI (International Multidisciplinary School - Sousse)", "private_engineering", C),
    ("TIME Université (Tunis)", "private_engineering", C),

    ("Autre établissement IT en Tunisie", "other", U),
]

TUNISIAN_TECH_UNIVERSITIES = [name for name, _, _ in INSTITUTIONS]
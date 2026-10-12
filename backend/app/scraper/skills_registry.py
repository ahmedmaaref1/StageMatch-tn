"""
skills_registry.py — Tunisia-Specific Skills & Domain Registry
================================================================
Built specifically for the Tunisian university system (LMD + Grandes Écoles).

SOURCES USED TO BUILD THIS:
- ENIT / ENIM / ENIS / ENIB / ENIG / ENSIT (Écoles Nationales d'Ingénieurs)
- ISET network (Institut Supérieur des Études Technologiques)
- Faculties: Sciences, Droit, Médecine, Lettres, Économie, etc.
- ISG / ISC / IHEC (Instituts Supérieurs de Gestion / Commerce)
- Real Tunisian job offers from Tanitjobs, Optioncarriere, TunisieTravail

TUNISIAN UNIVERSITY TYPES:
  - Université (ex: Univ. Tunis El Manar, Carthage, Sfax, Sousse, Monastir...)
  - ENI / ENIT / ENIM / ENIS   → Engineering schools (cycle ingénieur, 5 ans)
  - ISET                        → Applied technology institutes (licence, 3 ans)
  - ISG / IHEC / ESC            → Management/Business schools
  - ISCAE / ISF                 → Finance & Accounting institutes
  - Faculté de Droit            → Law faculties
  - Faculté de Médecine         → Medical faculties
  - Faculté des Lettres         → Humanities & Languages
  - ISCS / IPSI / ISSHT         → Communication, Media, Tourism

DOMAINS COVERED (17 total):
  1.  Informatique & Développement
  2.  Réseaux & Télécommunications
  3.  Génie Civil & Architecture
  4.  Génie Mécanique & Industriel
  5.  Génie Électrique & Électronique
  6.  Génie Chimique & Procédés
  7.  Finance, Comptabilité & Audit
  8.  Management & Commerce
  9.  Marketing & Communication Digitale
  10. Ressources Humaines
  11. Droit & Sciences Politiques
  12. Médecine, Pharmacie & Santé
  13. Sciences (Biologie, Chimie, Physique, Maths)
  14. Agronomie & Agroalimentaire
  15. Lettres, Langues & Traduction
  16. Tourisme & Hôtellerie
  17. Design Graphique & Multimédia
"""

import re


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Tunisian cities for location normalization
# ─────────────────────────────────────────────────────────────────────────────

TUNISIAN_CITIES = [
    "Tunis", "Sfax", "Sousse", "Kairouan", "Bizerte", "Gabès", "Ariana",
    "Gafsa", "Monastir", "Ben Arous", "Nabeul", "Béja", "Kasserine",
    "Médenine", "Jendouba", "El Kef", "Sidi Bouzid", "Zaghouan", "Tozeur",
    "Kebili", "Tataouine", "Siliana", "Mahdia", "Manouba", "La Marsa",
    "Hammamet", "Djerba", "Zarzis", "Mateur", "Bou Salem",
    "Technopôle El Ghazala", "El Ghazala", "Lac", "Centre Urbain Nord",
    "El Menzah", "Cité El Khadra", "Charguia", "Riadh Andalous",
    "Ennasr", "Berges du Lac", "Les Berges du Lac",
]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN DOMAINS REGISTRY
# ─────────────────────────────────────────────────────────────────────────────

DOMAINS = {

    # ─── 1. INFORMATIQUE & DÉVELOPPEMENT ────────────────────────────────────
    # Covers: Licence Informatique, ISET-TI (DSI/MDW/SEM), Cycle Ingénieur
    # Informatique (ENIT/ESPRIT/INSAT/Polytechnique Tunis)
    "Informatique & Développement": {
        "keywords": [
            # French/Arabic job title keywords
            "informatique", "développeur", "developer", "développement",
            "programmeur", "programmation", "logiciel", "software",
            "génie logiciel", "systèmes d'information", "si ",
            "application web", "application mobile", "site web",
            "full stack", "frontend", "backend", "fullstack",
            # Domain names used in Tunisian universities
            "dsi", "mdw", "sem", "iset ti", "licence informatique",
            "master informatique", "ingénieur informatique",
            "esprit", "insat", "isg sfax", "polytechnique",
            # Tech keywords
            "python", "java", "php", "javascript", "react", "angular",
            "django", "spring", "flutter", "android", "ios",
            "intelligence artificielle", "ia ", " ai ", "machine learning",
            "data science", "big data", "devops", "cloud", "docker",
            "cybersécurité", "sécurité informatique", "base de données",
            "algorithme", "api", "microservices", "agile", "scrum",
        ],
        "skills": [
            # ── Langages de programmation ──
            "Python", "Java", "JavaScript", "TypeScript", "PHP", "C", "C++",
            "C#", "Ruby", "Go", "Kotlin", "Swift", "Dart", "Scala", "R",
            "MATLAB", "Bash", "Shell", "Perl", "Rust", "Lua",
            # ── Web Frontend ──
            "React.js", "Vue.js", "Angular", "Next.js", "Nuxt.js",
            "HTML5", "CSS3", "TailwindCSS", "Bootstrap", "SASS",
            "jQuery", "Redux", "Webpack", "Vite",
            # ── Web Backend ──
            "FastAPI", "Django", "Flask", "Node.js", "Express.js",
            "Spring Boot", "Laravel", "Symfony", "CodeIgniter",
            "ASP.NET", "Ruby on Rails", "Nest.js",
            # ── Mobile ──
            "Android", "iOS", "Flutter", "React Native", "Xamarin",
            "Ionic", "Kotlin", "Swift",
            # ── Data / IA / ML ──
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "TensorFlow", "PyTorch", "Keras", "scikit-learn",
            "Pandas", "NumPy", "Matplotlib", "Seaborn",
            "Data Science", "Big Data", "Hadoop", "Spark", "Kafka",
            "Power BI", "Tableau", "Jupyter Notebook",
            "LLM", "ChatGPT API", "LangChain",
            # ── Bases de données ──
            "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Oracle", "SQLite", "Elasticsearch", "Cassandra",
            "MariaDB", "Firebase",
            # ── DevOps / Cloud ──
            "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Heroku",
            "Linux", "Git", "GitHub", "GitLab", "CI/CD",
            "Jenkins", "Nginx", "Apache", "Terraform", "Ansible",
            "GitHub Actions", "GitLab CI",
            # ── Cybersécurité ──
            "Cybersécurité", "Sécurité réseau", "Pentest", "Ethical Hacking",
            "OWASP", "Wireshark", "Metasploit", "Kali Linux",
            # ── Méthodes & Outils ──
            "REST API", "GraphQL", "Microservices", "Agile", "Scrum",
            "UML", "Merise", "Figma", "Postman", "Swagger", "Jira",
            "SOLID", "Design Patterns", "TDD", "Clean Architecture",
        ],
    },

    # ─── 2. RÉSEAUX & TÉLÉCOMMUNICATIONS ────────────────────────────────────
    # Covers: ISET-Com, RSI (ISET), Télécoms (ENIT), INITELtunisie
    "Réseaux & Télécommunications": {
        "keywords": [
            "réseau", "réseaux", "télécommunications", "télécom",
            "administrateur réseau", "ingénieur réseau", "rsi",
            "iset'com", "isetcom", "el ghazala", "tic",
            "infrastructure", "sécurité réseau", "wifi", "fibre optique",
            "voip", "5g", "iot", "internet des objets", "rfid",
            "cisco", "ccna", "routeur", "switch", "pare-feu",
            "vpn", "lan", "wan", "dhcp", "dns", "tcp/ip",
            "administration système", "sysadmin",
        ],
        "skills": [
            "Cisco", "CCNA", "CCNP", "Routage", "Switching",
            "VPN", "Firewall", "Pare-feu", "TCP/IP", "DNS", "DHCP",
            "VLAN", "LAN", "WAN", "Wi-Fi", "Fibre optique",
            "Linux Administration", "Windows Server", "Active Directory",
            "VMware", "VirtualBox", "Virtualisation",
            "SNMP", "Wireshark", "Packet Tracer",
            "VoIP", "Asterisk", "5G", "4G/LTE",
            "IoT", "MQTT", "Zigbee", "LoRa", "RFID",
            "Sécurité réseau", "IDS/IPS", "SOC", "SIEM",
            "BGP", "OSPF", "MPLS", "SD-WAN",
            "Python", "Bash", "Ansible", "Nagios", "Zabbix",
        ],
    },

    # ─── 3. GÉNIE CIVIL & ARCHITECTURE ──────────────────────────────────────
    # Covers: ENIT-Génie Civil, ENIS, ENICARTHAGE, INBAT, ENAU, architecture
    "Génie Civil & Architecture": {
        "keywords": [
            "génie civil", "ingénieur civil", "bâtiment", "btp",
            "construction", "travaux publics", "architecture", "architecte",
            "urbanisme", "urbaniste", "topographie", "topographe",
            "structures", "hydraulique", "environnement",
            "béton armé", "fondations", "chaussée", "voirie",
            "assainissement", "terrassement", "maîtrise d'ouvrage",
            "maîtrise d'œuvre", "bureau d'étude", "bureau d'études",
            "aménagement", "rénovation", "réhabilitation",
            "enau", "inbat", "isteub",
        ],
        "skills": [
            # ── Logiciels BTP / Structure ──
            "AutoCAD", "Revit", "BIM", "ArchiCAD", "ETABS",
            "SAP2000", "ROBOT Structural", "CYPECAD", "STAAD.Pro",
            "SketchUp", "Tekla Structures", "Allplan",
            # ── Topographie / SIG ──
            "ArcGIS", "QGIS", "SIG", "Covadis", "Mensura",
            "Topographie", "GPS Topographique", "Nivellement",
            # ── Architecture ──
            "3ds Max", "V-Ray", "Lumion", "Enscape", "Rhino",
            "Adobe Photoshop", "Adobe Illustrator", "InDesign",
            "Rendu 3D", "Maquette numérique",
            # ── Calcul / Études ──
            "Béton armé", "Calcul structurel", "RDM",
            "Hydraulique", "Hydrologie", "Assainissement",
            "Étude de sol", "Géotechnique", "Fondations",
            # ── Gestion de chantier ──
            "MS Project", "Primavera P6", "Gestion de chantier",
            "Planification", "Suivi des travaux", "Métré",
            # ── Normes ──
            "Eurocode", "DTU", "ISO 9001", "Métrés", "CCTP",
            # ── Général ──
            "Excel", "Word", "PowerPoint", "AutoCAD 2D/3D",
        ],
    },

    # ─── 4. GÉNIE MÉCANIQUE & INDUSTRIEL ────────────────────────────────────
    # Covers: ENIT-Mécanique, ENIM (Monastir), ENIG, ENSIT-Mécanique,
    #         ISET-Mécanique, Génie Industriel
    "Génie Mécanique & Industriel": {
        "keywords": [
            "génie mécanique", "mécanique", "ingénieur mécanique",
            "génie industriel", "génie des procédés", "génie de production",
            "maintenance", "productique", "fabrication",
            "matériaux", "thermique", "fluides", "énergétique",
            "robotique", "automatisation", "lean", "qualité",
            "enim", "enig", "ensit",
            "conception mécanique", "bureau d'étude mécanique",
            "mécatronique", "industrie", "usine", "production",
        ],
        "skills": [
            # ── CAO / Simulation ──
            "SolidWorks", "CATIA", "Autodesk Inventor", "Fusion 360",
            "Pro/Engineer", "ANSYS", "ABAQUS", "Nastran",
            "MATLAB", "Simulink", "COMSOL",
            # ── Fabrication / Production ──
            "CNC", "Usinage", "Fraisage", "Tournage", "Soudage",
            "Impression 3D", "FAO", "CFAO", "Prototypage rapide",
            "Contrôle qualité", "Métrologie", "Cotation ISO",
            # ── Gestion industrielle ──
            "Lean Manufacturing", "Six Sigma", "Kaizen", "5S",
            "AMDEC", "FMEA", "TPM", "Kanban",
            "ERP", "SAP", "GPAO", "MRP",
            # ── Qualité / Normes ──
            "ISO 9001", "ISO 14001", "ISO 45001",
            "Contrôle non destructif", "CND",
            # ── Thermique / Fluides ──
            "Thermodynamique", "Mécanique des fluides",
            "Échangeurs thermiques", "Pneumatique", "Hydraulique",
            # ── Maintenance ──
            "GMAO", "Maintenance préventive", "Maintenance corrective",
            "Fiabilité", "Diagnostic",
            # ── Outils ──
            "MS Project", "AutoCAD", "Excel", "PowerPoint",
        ],
    },

    # ─── 5. GÉNIE ÉLECTRIQUE & ÉLECTRONIQUE ─────────────────────────────────
    # Covers: ENIT-Électrique, ENIS-Électronique, ISET-GE (AII/EI/ELnI)
    "Génie Électrique & Électronique": {
        "keywords": [
            "génie électrique", "électricité", "électronique",
            "électrotechnique", "automatique", "automatisme",
            "automatisation industrielle", "aii", "informatique industrielle",
            "systèmes embarqués", "microcontrôleur", "microprocesseur",
            "plc", "api", "scada", "supervision",
            "energie", "énergies renouvelables", "photovoltaïque",
            "éolien", "maintenance électrique", "haute tension",
            "basse tension", "onduleur", "variateur",
            "signal", "traitement du signal", "electronique de puissance",
        ],
        "skills": [
            # ── Programmation embarquée ──
            "Arduino", "Raspberry Pi", "STM32", "ESP32",
            "C embarqué", "Assembly", "VHDL", "Verilog",
            "FPGA", "DSP",
            # ── Automatismes / PLC ──
            "PLC", "API Siemens", "API Schneider", "TIA Portal",
            "Unity Pro", "Step 7", "SCADA", "WinCC", "Intouch",
            "Grafcet", "Ladder", "SFC", "IEC 61131",
            # ── Simulation / CAO ──
            "Proteus", "Multisim", "LTspice", "PSIM",
            "MATLAB/Simulink", "LabVIEW",
            "Altium Designer", "Eagle", "KiCad",
            # ── Puissance / Énergie ──
            "Électronique de puissance", "Onduleur", "Redresseur",
            "Variateur de vitesse", "Moteur électrique",
            "Énergie solaire", "Photovoltaïque", "Éolien",
            "Réseau électrique", "Haute tension",
            # ── Mesure / Instrumentation ──
            "Oscilloscope", "Multimètre", "Analyseur de spectre",
            "Capteurs", "Actionneurs", "CAN", "RS232", "I2C", "SPI",
            # ── Normes ──
            "NF C 15-100", "CEI 60364", "ISO 9001",
            # ── Outils généraux ──
            "AutoCAD Électrique", "Excel", "MATLAB",
        ],
    },

    # ─── 6. GÉNIE CHIMIQUE & PROCÉDÉS ───────────────────────────────────────
    # Covers: INSAT-Génie Chimique, ENIS-Chimie, Institut Supérieur
    #         des Sciences Appliquées et de Technologie
    "Génie Chimique & Procédés": {
        "keywords": [
            "génie chimique", "génie des procédés", "chimie industrielle",
            "procédés chimiques", "raffinage", "pétrochimie",
            "industrie chimique", "industrie pharmaceutique",
            "agroalimentaire procédés", "traitement des eaux",
            "environnement industriel", "qualité industrielle",
            "chimie analytique", "laboratoire chimie",
            "insat chimie", "enis chimie",
        ],
        "skills": [
            # ── Procédés ──
            "Simulation de procédés", "Aspen Plus", "HYSYS",
            "PRO/II", "ChemCAD", "COMSOL",
            "Distillation", "Extraction", "Réaction chimique",
            "Échangeurs thermiques", "Colonnes de distillation",
            # ── Qualité / HSE ──
            "HACCP", "ISO 22000", "BPF", "GMP",
            "HSE", "ATEX", "Sécurité industrielle",
            "ISO 9001", "ISO 14001",
            # ── Laboratoire ──
            "Chimie analytique", "Chromatographie", "HPLC",
            "GC", "Spectroscopie", "Titrimétrie",
            "Contrôle qualité", "Métrologie chimique",
            # ── Environnement ──
            "Traitement des eaux", "Épuration", "Dépollution",
            "Analyse environnementale", "ISO 14001",
            # ── Outils ──
            "MATLAB", "Excel", "AutoCAD", "MS Project",
        ],
    },

    # ─── 7. FINANCE, COMPTABILITÉ & AUDIT ───────────────────────────────────
    # Covers: IHEC, ISG, FSE (Faculté des Sciences Économiques),
    #         ISCAE, ISF (Institut Supérieur de Finance)
    "Finance, Comptabilité & Audit": {
        "keywords": [
            "finance", "comptabilité", "comptable", "audit",
            "contrôle de gestion", "contrôleur de gestion",
            "trésorerie", "trésorier", "fiscalité", "fiscaliste",
            "banque", "bancaire", "assurance", "bourse",
            "investissement", "analyse financière",
            "reporting financier", "budget", "budgétisation",
            "commissaire aux comptes", "expert comptable",
            "consolidation", "bilan", "liasse fiscale",
            "ihec", "isf", "iscae", "isg finance",
            "gestion financière", "comptabilité générale",
            "comptabilité analytique", "contrôle interne",
            "ifrs", "syscohada", "normes comptables",
            "credit management", "risque crédit", "risque financier",
            "monnaie banque", "marchés financiers",
        ],
        "skills": [
            # ── Logiciels comptables / ERP ──
            "Sage 100", "Sage Paie", "Ciel Compta", "Odoo",
            "SAP FI/CO", "SAP FICO", "Oracle Financials",
            "QuickBooks", "ERP", "CEGID",
            # ── Bureautique analytique ──
            "Microsoft Excel", "Excel avancé", "VBA Excel",
            "Tableaux croisés dynamiques", "Power Query",
            "Power BI", "Tableau", "SAP Analytics",
            # ── Normes & Référentiels ──
            "IFRS", "SYSCOHADA", "Plan comptable tunisien",
            "Normes comptables tunisiennes", "NCT",
            "COSO", "COBIT",
            # ── Audit & Contrôle ──
            "Audit interne", "Audit externe", "Audit financier",
            "Contrôle interne", "Contrôle de gestion",
            "Due diligence", "Commissariat aux comptes",
            "Révision comptable",
            # ── Finance d'entreprise ──
            "Analyse financière", "Tableau de bord",
            "Business Plan", "Cash flow", "Trésorerie",
            "Gestion budgétaire", "Budget prévisionnel",
            "Rentabilité", "Valorisation d'entreprise",
            # ── Fiscalité ──
            "TVA", "IS", "Fiscalité tunisienne", "Liasse fiscale",
            "Déclarations fiscales", "Droit fiscal",
            # ── Banque / Marchés ──
            "Analyse crédit", "Scoring bancaire", "Risque crédit",
            "Marchés financiers", "Bloomberg", "Reuters",
            "Options", "Produits dérivés",
        ],
    },

    # ─── 8. MANAGEMENT & COMMERCE ───────────────────────────────────────────
    # Covers: ISG (Institut Supérieur de Gestion), IHEC Commerce,
    #         Licence Management, MBA, ESC
    "Management & Commerce": {
        "keywords": [
            "management", "gestion", "commerce", "commercial",
            "administration des affaires", "mba", "master management",
            "business administration", "gestion d'entreprise",
            "chef de projet", "project manager", "responsable",
            "stratégie", "développement commercial", "business development",
            "key account manager", "account manager", "kam",
            "vente", "force de vente", "technico-commercial",
            "supply chain", "logistique", "achat", "approvisionnement",
            "isg", "ihec", "esc tunisie", "esec",
            "gestion pme", "gestion pmi", "entrepreneuriat",
            "export", "commerce international",
            "qualité", "qhse", "iso",
        ],
        "skills": [
            # ── Outils de gestion ──
            "ERP", "SAP", "Odoo", "Microsoft Dynamics",
            "CRM", "Salesforce", "HubSpot",
            "MS Project", "Primavera", "Gestion de projet",
            # ── Bureautique ──
            "Pack Office", "Microsoft Excel", "PowerPoint", "Word",
            "Power BI", "Tableau", "Google Workspace",
            # ── Commerce / Vente ──
            "Négociation commerciale", "Prospection",
            "Développement commercial", "B2B", "B2C",
            "Incoterms", "Commerce international", "Export",
            "Gestion des achats", "Appels d'offres",
            # ── Supply Chain / Logistique ──
            "Supply Chain Management", "Logistique",
            "Gestion des stocks", "ERP logistique",
            "Transport", "Douane", "Transit",
            "Lean Supply Chain", "S&OP",
            # ── Qualité ──
            "ISO 9001", "QHSE", "Management de la qualité",
            "Audit qualité", "Amélioration continue",
            # ── Management ──
            "Leadership", "Management d'équipe", "Gestion de projet",
            "Agile", "Scrum", "PMI", "PMP",
            "Balanced Scorecard", "KPI", "Tableau de bord",
            "Business Plan", "Stratégie d'entreprise",
        ],
    },

    # ─── 9. MARKETING & COMMUNICATION DIGITALE ──────────────────────────────
    # Covers: IPSI (Institut Presse et Sciences de l'Information),
    #         ISComE, ISCA, IHEC Marketing
    "Marketing & Communication Digitale": {
        "keywords": [
            "marketing", "communication", "digital marketing",
            "marketing digital", "webmarketing", "e-marketing",
            "community manager", "social media", "réseaux sociaux",
            "content marketing", "création de contenu", "copywriting",
            "seo", "sem", "sea", "google ads", "facebook ads",
            "publicité", "brand", "marque", "branding",
            "e-commerce", "commerce électronique",
            "relation client", "expérience client", "crm",
            "événementiel", "relations publiques", "rp",
            "communication institutionnelle",
            "ipsi", "iscome", "isca", "ihec marketing",
            "responsable marketing", "chargé de communication",
        ],
        "skills": [
            # ── Marketing Digital ──
            "Marketing digital", "SEO", "SEM", "SEA",
            "Google Ads", "Facebook Ads", "Instagram Ads",
            "LinkedIn Ads", "TikTok Ads",
            "Google Analytics", "Google Search Console",
            "Meta Business Suite", "Hootsuite", "Buffer",
            # ── Community Management ──
            "Community Management", "Social Media Management",
            "Instagram", "Facebook", "LinkedIn", "TikTok", "YouTube",
            "Content Marketing", "Création de contenu",
            # ── Design / Création ──
            "Adobe Photoshop", "Adobe Illustrator", "Canva",
            "InDesign", "Adobe Premiere", "CapCut",
            "Figma", "After Effects",
            # ── E-commerce ──
            "Shopify", "WooCommerce", "PrestaShop", "Magento",
            "Amazon", "Jumia", "E-commerce",
            # ── CRM / Emailing ──
            "CRM", "HubSpot", "Salesforce", "Mailchimp",
            "Emailing", "Newsletter", "Marketing automation",
            # ── Événementiel / RP ──
            "Organisation d'événements", "Relations presse",
            "Communiqué de presse", "Relations publiques",
            # ── Rédaction ──
            "Copywriting", "Rédaction web", "Storytelling",
            "Traduction FR/EN/AR", "WordPress", "CMS",
            # ── Analyse ──
            "Power BI", "Tableau", "Pack Office",
            "Excel", "PowerPoint",
        ],
    },

    # ─── 10. RESSOURCES HUMAINES ─────────────────────────────────────────────
    # Covers: ISG-RH, IHEC-RH, Licence Management option RH
    "Ressources Humaines": {
        "keywords": [
            "ressources humaines", "rh", "human resources", "hr",
            "recrutement", "talent acquisition", "sourcing",
            "paie", "gestionnaire de paie", "administration du personnel",
            "formation", "développement des compétences",
            "gpec", "gestion prévisionnelle", "mobility",
            "relations sociales", "droit social", "dialogue social",
            "marque employeur", "employer branding",
            "responsable rh", "drh", "chargé rh",
            "onboarding", "offboarding", "gestion des talents",
            "évaluation des performances", "people management",
        ],
        "skills": [
            # ── Recrutement ──
            "Recrutement", "Sourcing", "Entretien structuré",
            "Assessment center", "Tests psychométriques",
            "ATS", "LinkedIn Recruiter", "Jobboards",
            "Onboarding", "Intégration",
            # ── Administration du personnel ──
            "Gestion de la paie", "Sage Paie", "Paie tunisienne",
            "CNSS", "CNAM", "Contrat de travail",
            "Code du travail tunisien", "Administration RH",
            # ── Formation & Développement ──
            "Plan de formation", "GPEC", "Bilan de compétences",
            "Évaluation 360°", "KPIs RH", "Tableau de bord RH",
            # ── Relations sociales ──
            "Relations sociales", "Négociation collective",
            "Droit du travail", "Inspection du travail",
            # ── SIRH ──
            "SAP HCM", "Odoo RH", "People Soft",
            "SIRH", "Oracle HCM",
            # ── Outils ──
            "Pack Office", "Excel", "PowerPoint", "Word",
            "Google Workspace", "Power BI",
        ],
    },

    # ─── 11. DROIT & SCIENCES POLITIQUES ────────────────────────────────────
    # Covers: FDSPT (El Manar), FSJPST (Carthage), Faculté de Droit Sfax,
    #         Faculté de Droit Sousse, Droit des affaires, Droit numérique
    "Droit & Sciences Politiques": {
        "keywords": [
            "droit", "juridique", "juriste", "avocat", "notaire",
            "huissier", "magistrat", "juge", "procureur",
            "légal", "législation", "réglementation", "compliance",
            "conformité", "contrat", "contentieux", "arbitrage",
            "droit des affaires", "droit commercial", "droit des sociétés",
            "droit du travail", "droit civil", "droit pénal",
            "droit public", "droit privé", "droit fiscal",
            "droit administratif", "droit international",
            "propriété intellectuelle", "pi", "marques",
            "droit numérique", "rgpd", "protection des données",
            "sciences politiques", "relations internationales",
            "fdspt", "fsjpst", "licence droit",
            "droit des affaires tunisien", "csc tunisie",
        ],
        "skills": [
            # ── Compétences juridiques ──
            "Rédaction juridique", "Recherche juridique",
            "Analyse juridique", "Conseil juridique",
            "Veille juridique", "Veille réglementaire",
            # ── Domaines de droit ──
            "Droit des affaires", "Droit commercial",
            "Droit des sociétés", "Droit du travail",
            "Droit civil", "Droit pénal", "Droit public",
            "Droit fiscal", "Droit administratif",
            "Propriété intellectuelle", "Marques et brevets",
            "Droit numérique", "RGPD",
            "Droit des contrats", "Droit immobilier",
            "Droit de la concurrence", "Arbitrage",
            # ── Compliance ──
            "Compliance", "Conformité réglementaire",
            "KYC", "AML", "LCB-FT",
            "Contrôle interne juridique",
            # ── Tunisie spécifique ──
            "Code des sociétés commerciales tunisien",
            "Code du travail tunisien",
            "Code de l'IRPP et de l'IS",
            "BVMT", "CMF Tunisie",
            # ── Outils ──
            "Pack Office", "Word", "PowerPoint",
            "Légifrance", "Doctrine.fr", "Jurisite Tunisie",
        ],
    },

    # ─── 12. MÉDECINE, PHARMACIE & SANTÉ ────────────────────────────────────
    # Covers: Facultés de Médecine (Tunis, Sfax, Sousse, Monastir, Bizerte),
    #         Faculté de Pharmacie, ISSSTS (paramédical)
    "Médecine, Pharmacie & Santé": {
        "keywords": [
            "médecine", "médical", "santé", "médecin", "docteur",
            "pharmacie", "pharmacien", "pharmacologique",
            "infirmier", "infirmière", "soins", "paramédical",
            "clinique", "hôpital", "bloc opératoire", "urgences",
            "kinésithérapeute", "kiné", "physiothérapeute",
            "biologiste", "laborantin", "labo médical",
            "imagerie médicale", "radiologie", "radiologue",
            "chirurgie", "pédiatrie", "cardiologie", "dermatologie",
            "psychiatrie", "psychologie clinique", "nutrition",
            "sage-femme", "maternité", "stomatologie", "dentiste",
            "ophtalmologie", "oph", "oto-rhino-laryngologie", "orl",
            "recherche clinique", "essai clinique", "cro",
            "industrie pharmaceutique", "pharmacovigilance",
            "affaires médicales", "affaires réglementaires pharma",
        ],
        "skills": [
            # ── Clinique ──
            "Soins infirmiers", "Soins intensifs",
            "Gestes d'urgence", "Réanimation", "Suture",
            "Pharmacologie clinique", "Prescription médicale",
            # ── Laboratoire ──
            "Biologie médicale", "Hématologie", "Biochimie",
            "Microbiologie", "Immunologie", "PCR", "ELISA",
            "Culture cellulaire", "Sérologie", "Bactériologie",
            # ── Imagerie ──
            "Radiologie", "Échographie", "IRM", "Scanner",
            "Mammographie", "Imagerie médicale",
            # ── Industrie pharma ──
            "BPF", "GMP", "BPC", "ICH", "CTD",
            "Affaires réglementaires", "Pharmacovigilance",
            "Dossier d'AMM", "ISO 13485",
            "Contrôle qualité pharmaceutique",
            # ── Recherche clinique ──
            "Essais cliniques", "Protocole clinique",
            "Biostatistiques", "Épidémiologie",
            "SPSS", "R", "SAS",
            # ── Logiciels ──
            "Dossier patient informatisé", "HIS", "Mediware",
            "Pack Office", "Excel",
        ],
    },

    # ─── 13. SCIENCES FONDAMENTALES & APPLIQUÉES ─────────────────────────────
    # Covers: FST (Faculté des Sciences de Tunis), FSS (Sfax), etc.
    # Biology, Chemistry, Physics, Mathematics, Statistics
    "Sciences Fondamentales & Appliquées": {
        "keywords": [
            "biologie", "biologie moléculaire", "biotechnologie",
            "génétique", "microbiologie", "biochimie",
            "chimie", "chimie analytique", "chimie organique",
            "chimie des matériaux",
            "physique", "physique des matériaux", "nanomatériaux",
            "mathématiques", "maths", "mathématiques appliquées",
            "statistiques", "probabilités", "modélisation",
            "sciences de la terre", "géologie", "géophysique",
            "environnement", "écologie", "sciences environnementales",
            "fst", "fss sfax", "faculté des sciences",
            "ingénierie biologique", "nanotechnologie",
        ],
        "skills": [
            # ── Biologie ──
            "Biologie moléculaire", "Biochimie", "Microbiologie",
            "Génétique", "Biotechnologie", "PCR", "qPCR",
            "ELISA", "Western Blot", "Immunofluorescence",
            "Microscopie", "Culture cellulaire", "Flow cytometry",
            # ── Chimie ──
            "Chimie analytique", "HPLC", "GC-MS", "Spectroscopie",
            "RMN", "IR", "UV-Vis", "Titrimétrie",
            "Synthèse organique", "Chromatographie",
            # ── Physique / Matériaux ──
            "DRX", "MEB", "AFM", "Caractérisation des matériaux",
            "Optique", "Photovoltaïque",
            # ── Mathématiques / Statistiques ──
            "R", "Python", "MATLAB", "SPSS", "SAS", "Stata",
            "Statistiques descriptives", "Analyse de données",
            "Modélisation mathématique", "Machine Learning",
            "LaTeX",
            # ── Environnement ──
            "SIG", "QGIS", "ArcGIS", "Télédétection",
            "Analyse environnementale", "ISO 14001",
        ],
    },

    # ─── 14. AGRONOMIE & AGROALIMENTAIRE ─────────────────────────────────────
    # Covers: INAT (Institut National Agronomique de Tunisie),
    #         ESAK (Kef), ESSA (Sfax), IRESA
    "Agronomie & Agroalimentaire": {
        "keywords": [
            "agronomie", "agronome", "agriculture", "agricole",
            "agroalimentaire", "industrie alimentaire", "agro",
            "vétérinaire", "élevage", "zootechnie",
            "production végétale", "production animale",
            "horticulture", "sylviculture", "foresterie",
            "pêche", "aquaculture",
            "irrigation", "sol", "fertilisation",
            "phytosanitaire", "pesticides", "OPP",
            "inat", "esak", "essa sfax",
            "qualité alimentaire", "sécurité alimentaire",
            "agriculture biologique", "agriculture durable",
            "agroécologie", "terroir", "oléiculture", "viticulture",
        ],
        "skills": [
            # ── Agronomie terrain ──
            "Analyse de sol", "Fertilisation", "Phytosanitaire",
            "Irrigation", "Drainage", "Agriculture biologique",
            "OPP", "Désherbage", "Serre", "Culture sous abri",
            # ── Agroalimentaire ──
            "HACCP", "ISO 22000", "BRC", "IFS",
            "Contrôle qualité alimentaire", "Microbiologie alimentaire",
            "Analyse sensorielle", "Étiquetage alimentaire",
            "Traçabilité", "GMP agroalimentaire",
            # ── SIG & Télédétection ──
            "SIG", "ArcGIS", "QGIS", "GPS",
            "Télédétection", "Agriculture de précision",
            # ── Vétérinaire ──
            "Médecine vétérinaire", "Élevage bovin",
            "Aviculture", "Aquaculture",
            # ── Statistiques ──
            "R", "SPSS", "Excel", "STATISTICA",
            "Statistiques agricoles",
            # ── Outils ──
            "Pack Office", "Excel", "PowerPoint",
            "Rapport technique", "Rédaction scientifique",
        ],
    },

    # ─── 15. LETTRES, LANGUES & TRADUCTION ──────────────────────────────────
    # Covers: Faculté des Lettres (Manouba, Sfax, Sousse),
    #         ISLT (Institut Supérieur des Langues de Tunis)
    "Lettres, Langues & Traduction": {
        "keywords": [
            "lettres", "langue", "linguistique", "littérature",
            "traduction", "traducteur", "interprète", "interprétariat",
            "français", "anglais", "arabe", "allemand", "espagnol",
            "italien", "chinois", "langue étrangère",
            "langue arabe", "langue française", "langue anglaise",
            "sciences du langage", "fle", "français langue étrangère",
            "islt", "faculté des lettres manouba",
            "enseignement", "enseignant", "professeur de langue",
            "philologie", "sémiotique",
        ],
        "skills": [
            # ── Langues ──
            "Français", "Anglais", "Arabe", "Allemand",
            "Espagnol", "Italien", "Chinois", "Turc",
            "Traduction FR-EN", "Traduction AR-FR",
            "Traduction technique", "Traduction juridique",
            "Interprétation consécutive", "Interprétation simultanée",
            # ── Enseignement ──
            "FLE", "Enseignement du français",
            "Enseignement de l'anglais", "Pédagogie",
            "Didactique", "Conception pédagogique",
            # ── Rédaction ──
            "Rédaction professionnelle", "Correction orthographique",
            "Édition", "Relecture", "Copywriting",
            "Traduction assermentée",
            # ── Outils ──
            "SDL Trados", "memoQ", "Wordfast",
            "Pack Office", "Word", "LaTeX",
        ],
    },

    # ─── 16. TOURISME & HÔTELLERIE ──────────────────────────────────────────
    # Covers: ISSHT (Institut Supérieur des Sciences Humaines de Tunis),
    #         ISTHB (Djerba), ISTHSM (Monastir), ISCHT (Bizerte)
    "Tourisme & Hôtellerie": {
        "keywords": [
            "tourisme", "hôtellerie", "hôtel", "hébergement",
            "restaurant", "restauration", "culinaire", "cuisine",
            "réceptionniste", "front office", "back office",
            "guide touristique", "agence de voyage",
            "tour opérateur", "billetterie",
            "spa", "bien-être", "thalasso",
            "event manager", "événementiel hôtelier",
            "revenue management", "yield management",
            "isthb", "isthsm", "ischt", "issht tourisme",
        ],
        "skills": [
            # ── Hébergement ──
            "Accueil client", "Réception hôtelière",
            "Opera PMS", "Fidelio", "Protel",
            "Check-in/Check-out", "Réservation",
            "Revenue Management", "Yield Management",
            # ── Restauration ──
            "Service en salle", "Bar", "Sommellerie",
            "Cuisine", "HACCP restauration", "Hygiène alimentaire",
            "Gestion cuisine", "Food & Beverage",
            # ── Tourisme ──
            "Guide touristique", "Billetterie",
            "Gestion agence de voyage", "Tour operating",
            "Inbound tourism", "Outbound tourism",
            "Amadeus", "Galileo", "Sabre", "GDS",
            # ── Langues (cruciales dans ce secteur) ──
            "Français", "Anglais", "Arabe", "Allemand",
            "Espagnol", "Italien",
            # ── Événementiel ──
            "Organisation d'événements", "MICE",
            "Gestion de groupe", "Team building",
            # ── Outils ──
            "Pack Office", "Excel", "PowerPoint",
        ],
    },

    # ─── 17. DESIGN GRAPHIQUE & MULTIMÉDIA ──────────────────────────────────
    # Covers: ISET-MDW (Multimédia et Développement Web),
    #         ESSTED, Institut supérieur des Beaux-Arts (Tunis/Sousse/Nabeul)
    "Design Graphique & Multimédia": {
        "keywords": [
            "design graphique", "graphisme", "designer graphique",
            "multimédia", "motion design", "vidéo", "montage vidéo",
            "animation", "illustration", "identité visuelle",
            "ux design", "ui design", "ux/ui", "expérience utilisateur",
            "web design", "webdesign", "maquette", "prototype",
            "photographie", "retouche photo",
            "3d", "modélisation 3d", "animation 3d",
            "essted", "iset mdw", "beaux arts tunis",
            "direction artistique",
        ],
        "skills": [
            # ── Adobe Suite ──
            "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign",
            "Adobe After Effects", "Adobe Premiere Pro",
            "Adobe XD", "Adobe Lightroom",
            # ── UX/UI ──
            "Figma", "Sketch", "InVision", "Zeplin",
            "UX Design", "UI Design", "Wireframing",
            "Prototypage", "Design Thinking",
            "Tests utilisateurs", "User Research",
            # ── Motion / 3D ──
            "After Effects", "Cinema 4D", "Blender",
            "3ds Max", "Maya", "CapCut",
            # ── Web Design ──
            "HTML/CSS", "WordPress", "Elementor",
            "Webflow", "Squarespace",
            # ── Autres ──
            "Canva", "CorelDRAW", "GIMP",
            "Photographie", "Direction artistique",
            "Identité visuelle", "Charte graphique",
            "Impression offset", "PAO",
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def extract_skills_from_text(text: str) -> list[str]:
    """
    Scans job offer text and returns all recognized skills found,
    across ALL 17 Tunisian university domains.
    """
    found = []
    text_lower = text.lower()

    for domain_data in DOMAINS.values():
        for skill in domain_data["skills"]:
            # For short skills of 1-2 letters (like R, C, Go, CI), match strictly with word boundary and case
            if len(skill) <= 2:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text):  # case-sensitive for short acronyms
                    found.append(skill)
            else:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found.append(skill)

    return list(set(found))


def detect_domain(title: str, description: str) -> str:
    """
    Detects the most likely academic domain for a job offer.

    ALGORITHM:
    1. Combine title (weighted x3) + description into one text
    2. For each domain, count keyword matches
    3. Return the domain with the highest score
    4. Minimum 1 match required, otherwise return "General"

    WHY title x3: The job title is the most informative field.
    "Ingénieur Génie Civil" immediately tells us the domain
    even if the description is vague.
    """
    # Title weighted 3× more than description
    combined = f"{title} {title} {title} {description}".lower()

    scores = {}
    for domain_name, domain_data in DOMAINS.items():
        score = 0
        for keyword in domain_data["keywords"]:
            if keyword.lower() in combined:
                score += 1
        scores[domain_name] = score

    best_domain = max(scores, key=scores.get)
    best_score = scores[best_domain]

    return best_domain if best_score >= 1 else "General"


def get_all_domain_names() -> list[str]:
    """Returns sorted list of all domain names."""
    return sorted(DOMAINS.keys()) + ["General"]


def get_skills_for_domain(domain_name: str) -> list[str]:
    """Returns the skill list for a specific domain."""
    if domain_name in DOMAINS:
        return DOMAINS[domain_name]["skills"]
    return []


def normalize_city(city_text: str) -> str:
    """
    Normalizes a city string to a standard Tunisian city name.
    If no known Tunisian city is found, cleanly returns 'Tunisie'.
    """
    if not city_text:
        return "Tunisie"

    city_lower = city_text.lower()
    for city in TUNISIAN_CITIES:
        # Match city name as a distinct word
        pattern = r'\b' + re.escape(city.lower()) + r'\b'
        if re.search(pattern, city_lower):
            return city

    # Fallback to Tunisia if no specific city was mentioned
    return "Tunisie"

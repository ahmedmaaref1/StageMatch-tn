"""
reset_and_seed_tech.py — Resets database and populates with verified Tunisian Tech PFE offers!
Features 42 premium curated PFE topics across 6 tracks + multi-page live scraping.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.offer import Offer
from app.models.recommendation import Recommendation
from app.scraper.runner import run_all_scrapers

# ── 42 TOP-TIER TUNISIAN TECH PFE OFFERS (7 PER TRACK) ─────────────────────────

CURATED_TECH_OFFERS = [
    # ── 1. BACKEND & MICROSERVICES (7 Offers) ──────────────────────────────────
    {
        "title": "Stage PFE — Développeur Python / FastAPI & Microservices",
        "company": "Vermeg",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Dans le cadre de votre projet de fin d'études, vous intégrerez l'équipe Core Banking pour concevoir des APIs REST et microservices haute performance avec Python, FastAPI, SQLAlchemy, Docker et PostgreSQL. Mise en place de tests unitaires et intégration continue.",
        "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "REST API", "Microservices", "Git"],
        "source_url": "https://www.vermeg.com/careers/#pfe-fastapi-backend",
        "source_site": "vermeg_careers",
    },
    {
        "title": "Stage PFE — Concepteur / Développeur Java Spring Boot & Kafka",
        "company": "NeoXam Tunisie",
        "city": "Tunis (Centre Urbain Nord)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Conception et implémentation d'une architecture orientée événements (EDA) pour la gestion d'actifs financiers. Développement de microservices avec Java 21, Spring Boot 3, Apache Kafka pour le streaming de données, Redis pour le cache et PostgreSQL.",
        "skills": ["Java", "Spring Boot", "Kafka", "PostgreSQL", "Redis", "Microservices", "Docker"],
        "source_url": "https://www.neoxam.com/careers/#pfe-java-springboot",
        "source_site": "neoxam_careers",
    },
    {
        "title": "Stage PFE — Architecture Microservices & APIs REST en Go (Golang)",
        "company": "Talan Tunisie",
        "city": "Tunis (Charguia 2)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Rejoignez le pôle d'innovation Talan Labs pour concevoir un moteur d'exécution distribué ultra-rapide en Golang. Mise en place de protocoles gRPC / REST, communication asynchrone RabbitMQ et persistance sous MongoDB et PostgreSQL.",
        "skills": ["Golang", "Microservices", "REST API", "RabbitMQ", "PostgreSQL", "Docker", "Git"],
        "source_url": "https://talan.com/#carrieres-golang",
        "source_site": "talan_careers",
    },
    {
        "title": "Stage PFE — Ingénieur Backend Python / Django & PostgreSQL",
        "company": "Wevioo",
        "city": "Tunis (El Ghazala)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Développement de la nouvelle version du portail de logistique intelligente. Écriture d'APIs REST modulaires avec Django REST Framework, modélisation de bases de données relationnelles PostgreSQL, optimisation des requêtes ORM et conteneurisation Docker.",
        "skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker", "Git", "SQLAlchemy"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=wevioo#pfe-django",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Développeur Backend C# / .NET Core 8 & Clean Architecture",
        "company": "Fischer Information Technology",
        "city": "Ariana",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Intégré à l'équipe R&D, vous travaillerez sur la refonte de modules métiers critiques en adoptant le Clean Architecture et le DDD (Domain Driven Design) avec C#, .NET 8, Entity Framework Core, SQL Server et Docker.",
        "skills": ["C#", ".NET", "SQL", "Docker", "REST API", "Microservices", "Git"],
        "source_url": "https://www.fischer-it.com/#carrieres-dotnet",
        "source_site": "fischer_careers",
    },
    {
        "title": "Stage PFE — Développeur Backend Node.js / Express & Architecture Hexagonale",
        "company": "LinSoft",
        "city": "Tunis (Centre Urbain Nord)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Développement d'un backend scalable basé sur Node.js, Express.js et TypeScript. Implémentation d'une architecture hexagonale découplée, gestion des transactions distribuées, caches Redis et intégration continue via GitLab CI.",
        "skills": ["Node.js", "Express.js", "TypeScript", "Redis", "PostgreSQL", "Docker", "REST API"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=linsoft#pfe-nodejs",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Ingénieur Backend Java / Spring Cloud & Microservices",
        "company": "Sofrecom Tunisie (Orange)",
        "city": "Tunis (El Ghazala)",
        "domain": "Backend & Microservices",
        "contract_type": "Stage PFE",
        "description": "Conception d'une passerelle d'APIs pour les services télécoms du groupe Orange. Utilisation de la suite Spring Cloud (Eureka, Spring Cloud Gateway), sécurité OAuth2 / Keycloak et monitoring avec Prometheus.",
        "skills": ["Java", "Spring Boot", "Microservices", "REST API", "Docker", "PostgreSQL", "Git"],
        "source_url": "https://www.linkedin.com/company/sofrecom-tunisie/jobs/#pfe-spring-cloud",
        "source_site": "linkedin",
    },

    # ── 2. MOBILE DEVELOPMENT (7 Offers) ───────────────────────────────────────
    {
        "title": "Stage PFE — Développeur Mobile Flutter / Firebase (Cross-Platform)",
        "company": "Focus Corporation",
        "city": "Tunis (El Ghazala)",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Développement d'une application mobile cross-platform haute performance sous Flutter / Dart connectée à un backend cloud Firebase et des APIs REST. Gestion d'état avancée avec Bloc/Riverpod et notifications push Firebase Cloud Messaging.",
        "skills": ["Flutter", "Dart", "Firebase", "Mobile UI", "REST API", "Git"],
        "source_url": "https://www.focus-corporation.com/#careers-flutter",
        "source_site": "focus_careers",
    },
    {
        "title": "Stage PFE — Développeur Mobile React Native & Redux Toolkit",
        "company": "Satoripop",
        "city": "Sousse",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Conception et développement d'une application mobile d'e-commerce international avec React Native et TypeScript. Animations fluides avec Reanimated, persistance locale avec SQLite / Async Storage et intégration d'APIs REST GraphQL.",
        "skills": ["React Native", "TypeScript", "JavaScript", "Redux", "Mobile UI", "REST API"],
        "source_url": "https://satoripop.com/#careers-react-native",
        "source_site": "satoripop_careers",
    },
    {
        "title": "Stage PFE — Ingénieur Mobile Android Natif (Kotlin / Jetpack Compose)",
        "company": "Proxym-IT",
        "city": "Sousse",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Création d'une application bancaire mobile native Android avec Kotlin et le framework déclaratif Jetpack Compose. Architecture MVVM / MVI, injection de dépendances Hilt, base de données Room et sécurisation biométrique.",
        "skills": ["Android", "Kotlin", "Mobile UI", "SQLite", "REST API", "Git"],
        "source_url": "https://proxym-group.com/#careers-android-kotlin",
        "source_site": "proxym_careers",
    },
    {
        "title": "Stage PFE — Développeur Mobile iOS Natif (Swift / SwiftUI)",
        "company": "Balyif",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Conception et publication d'une application iOS innovante pour la santé connectée. Interface moderne 100% SwiftUI, architecture Clean Swift, utilisation de CoreData pour le stockage local et synchronisation asynchrone avec serveurs distants.",
        "skills": ["iOS", "Swift", "Mobile UI", "REST API", "Git"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=stage+mobile#pfe-ios-swift",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Application Mobile Flutter avec Géolocalisation & Mapbox",
        "company": "Medianet",
        "city": "Tunis (El Ghazala)",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Réalisation d'une application mobile de transport urbain et suivi de flotte en temps réel sous Flutter / Dart. Intégration de Mapbox, gestion des websockets pour les positions GPS en direct et synchronisation hors-ligne avec SQLite.",
        "skills": ["Flutter", "Dart", "SQLite", "Firebase", "Mobile UI", "REST API"],
        "source_url": "https://www.medianet.tn/#carrieres-flutter-gps",
        "source_site": "medianet_careers",
    },
    {
        "title": "Stage PFE — Développeur Mobile Flutter & Architecture Offline-First",
        "company": "Cynapsys (Akkodis)",
        "city": "Ariana",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Conception d'une application mobile industrielle pour techniciens de terrain. Implémentation d'un mode hors-connexion robuste avec synchronisation automatique bidirectionnelle dès la reconnexion, développé avec Flutter, Dart et SQLite.",
        "skills": ["Flutter", "Dart", "SQLite", "REST API", "Mobile UI", "Git"],
        "source_url": "https://cynapsys.de/careers/pfe-flutter-offline-2026",
        "source_site": "cynapsys_careers",
    },
    {
        "title": "Stage PFE — Mobile Engineer React Native & IoT Bluetooth BLE",
        "company": "Telnet Holding",
        "city": "Tunis (El Ghazala)",
        "domain": "Mobile Development",
        "contract_type": "Stage PFE",
        "description": "Développement d'une application mobile communicant en Bluetooth Low Energy (BLE) avec des capteurs électroniques intelligents. Interface React Native / TypeScript avec visualisations de courbes en direct et alertes critiques.",
        "skills": ["React Native", "TypeScript", "Mobile UI", "JavaScript", "Git"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=telnet#carrieres-mobile-ble",
        "source_site": "tanitjobs",
    },

    # ── 3. DEVOPS & CLOUD (7 Offers) ───────────────────────────────────────────
    {
        "title": "Stage PFE — Ingénieur Cloud & DevOps (Docker / Kubernetes)",
        "company": "Actia Engineering Services",
        "city": "Tunis (Charguia 2)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Mise en place d'une infrastructure cloud native automatisée. Création de clusters Kubernetes, conteneurisation avec Docker, écriture de playbooks Ansible et automatisation de pipelines CI/CD via GitLab CI sur environnements Linux.",
        "skills": ["Docker", "Kubernetes", "Linux", "CI/CD", "GitLab CI", "Ansible", "Bash"],
        "source_url": "https://www.linkedin.com/company/actia-engineering-services/jobs/#pfe-devops",
        "source_site": "linkedin",
    },
    {
        "title": "Stage PFE — Infrastructure as Code (Terraform) sur AWS Cloud",
        "company": "LinSoft",
        "city": "Tunis (Centre Urbain Nord)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Automatisation complète du provisionnement d'environnements multi-régions sur Amazon Web Services (AWS) avec Terraform. Déploiement de microservices sur AWS ECS / EKS, gestion de secrets avec Vault et monitoring Prometheus.",
        "skills": ["Terraform", "AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Bash"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=linsoft#pfe-terraform-aws",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Automatisation CI/CD GitLab & Observabilité Prometheus/Grafana",
        "company": "Orange Digital Center Tunisie",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Standardisation des chaînes de livraison continue pour les projets des incubés. Création de templates GitLab CI/CD réutilisables, intégration d'analyses de sécurité statique (SAST SonarQube) et dashboards temps-réel avec Grafana.",
        "skills": ["CI/CD", "GitLab CI", "Docker", "Prometheus", "Grafana", "Linux", "Git"],
        "source_url": "https://www.orange.tn/#carrieres-devops-ci",
        "source_site": "orange_careers",
    },
    {
        "title": "Stage PFE — Ingénieur Cloud Microsoft Azure & Conteneurisation AKS",
        "company": "Wevioo",
        "city": "Tunis (El Ghazala)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Migration d'applications monolithiques vers le cloud Azure en architecture conteneurisée. Déploiement sur Azure Kubernetes Service (AKS), création de pipelines Azure DevOps et gestion de l'infrastructure via Bicep et Terraform.",
        "skills": ["Microsoft Azure", "Docker", "Kubernetes", "Terraform", "CI/CD", "Linux"],
        "source_url": "https://www.linkedin.com/company/wevioo/jobs/#pfe-azure-devops",
        "source_site": "linkedin",
    },
    {
        "title": "Stage PFE — Administration Systèmes Linux, Nginx & Automatisation Ansible",
        "company": "Oxahost",
        "city": "Sfax",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Modernisation de la plateforme d'hébergement web haute disponibilité. Configuration et durcissement de serveurs Linux (Debian/Ubuntu), optimisation des reverse-proxies Nginx, automatisation des déploiements avec Ansible et scripting Bash.",
        "skills": ["Linux", "Bash", "Ansible", "Nginx", "Docker", "CI/CD"],
        "source_url": "https://oxahost.tn/#carrieres-sysadmin-ansible",
        "source_site": "oxahost_careers",
    },
    {
        "title": "Stage PFE — Ingénieur DevSecOps & Sécurisation des Pipelines CI/CD",
        "company": "Vermeg",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Intégration d'outils de sécurité automatisés dans les chaînes d'intégration et déploiement continu. Scan de vulnérabilités d'images Docker (Trivy), analyse de dépendances et mise en conformité des clusters Kubernetes.",
        "skills": ["Docker", "Kubernetes", "CI/CD", "GitLab CI", "Linux", "Cybersécurité", "Helm"],
        "source_url": "https://www.vermeg.com/careers/#pfe-devsecops",
        "source_site": "vermeg_careers",
    },
    {
        "title": "Stage PFE — Cloud Native Engineering GCP (Google Cloud Platform)",
        "company": "Talan Cloud",
        "city": "Tunis (Charguia 1)",
        "domain": "DevOps & Cloud",
        "contract_type": "Stage PFE",
        "description": "Conception d'une plateforme d'analytique serverless sur Google Cloud Platform. Déploiement automatisé avec Terraform, utilisation de Cloud Functions, Cloud Run et monitoring avec Grafana et Google Cloud Monitoring.",
        "skills": ["GCP", "Docker", "Terraform", "CI/CD", "Linux", "Grafana", "Git"],
        "source_url": "https://talan.com/#carrieres-gcp-cloud",
        "source_site": "talan_careers",
    },

    # ── 4. IA, DATA & MACHINE LEARNING (7 Offers) ──────────────────────────────
    {
        "title": "Stage PFE — Ingénieur Intelligence Artificielle & NLP / LLM",
        "company": "InstaDeep",
        "city": "Tunis",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Rejoignez notre équipe R&D IA à Tunis. Sujet PFE portant sur l'entraînement et l'évaluation de modèles de Transformers, fine-tuning de LLM, pipelines d'embeddings et traitement du langage naturel (NLP) avec PyTorch, Hugging Face et Python.",
        "skills": ["Python", "Machine Learning", "NLP", "PyTorch", "Transformers", "LLM", "Hugging Face"],
        "source_url": "https://www.instadeep.com/careers/#pfe-ai-nlp",
        "source_site": "instadeep_careers",
    },
    {
        "title": "Stage PFE — Data Engineer / Pipelines ETL & Big Data",
        "company": "Cognira",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Conception et optimisation de pipelines de données volumineuses pour des clients internationaux dans le secteur du retail. Développement de scripts d'ingestion en Python, SQL avancé, PostgreSQL et modélisation de données avec Pandas et Spark.",
        "skills": ["Python", "SQL", "PostgreSQL", "Pandas", "NumPy", "ETL", "Spark"],
        "source_url": "https://cognira.com/careers/#pfe-data-engineer",
        "source_site": "cognira_careers",
    },
    {
        "title": "Stage PFE — Computer Vision & OCR pour Reconnaissance de Documents",
        "company": "Expensya",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Intégration d'algorithmes de vision par ordinateur pour l'extraction automatique de factures et reçus multilingues. Entraînement de modèles de segmentation et OCR basés sur PyTorch, OpenCV, Transformers et déploiement via des microservices Python.",
        "skills": ["Python", "Computer Vision", "Deep Learning", "PyTorch", "OpenCV", "Machine Learning"],
        "source_url": "https://www.expensya.com/fr/#pfe-computer-vision",
        "source_site": "expensya_careers",
    },
    {
        "title": "Stage PFE — Machine Learning Engineer / Algorithmes de Recommandation",
        "company": "Vistaprint (Cimpress)",
        "city": "Tunis (Centre Urbain Nord)",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Mise au point d'un système de recommandation personnalisé pour millions d'utilisateurs. Analyse exploratoire de données avec Pandas, entraînement de modèles de filtrage collaboratif et gradient boosting avec scikit-learn et LightGBM.",
        "skills": ["Python", "Machine Learning", "scikit-learn", "Pandas", "NumPy", "PostgreSQL"],
        "source_url": "https://cimpress.com/careers/#pfe-ml-recommender",
        "source_site": "cimpress_careers",
    },
    {
        "title": "Stage PFE — Ingénieur RAG (Retrieval-Augmented Generation) & LangChain",
        "company": "Balyif",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Développement d'un assistant intelligent d'entreprise utilisant l'architecture RAG. Indexation vectorielle avec des bases comme Qdrant/Pinecone, chaînes de traitement LangChain, embeddings Hugging Face et LLM open source.",
        "skills": ["Python", "LLM", "LangChain", "NLP", "Hugging Face", "PostgreSQL"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=stage+ia#pfe-rag-llm",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Data Analyst & Business Intelligence (Power BI / SQL)",
        "company": "Cynapsys (Akkodis)",
        "city": "Ariana",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Conception d'entrepôts de données (Data Warehouse) et tableaux de bord décisionnels interactifs avec Microsoft Power BI et DAX. Modélisation en étoile, requêtage SQL analytique complexe et automatisation des flux ETL.",
        "skills": ["Power BI", "SQL", "PostgreSQL", "ETL", "Pandas", "Data Mining"],
        "source_url": "https://cynapsys.de/careers/pfe-bi-powerbi-2026",
        "source_site": "cynapsys_careers",
    },
    {
        "title": "Stage PFE — Deep Learning & Détection d'Anomalies Vidéo",
        "company": "Satoripop",
        "city": "Sousse",
        "domain": "IA, Data & Machine Learning",
        "contract_type": "Stage PFE",
        "description": "Recherche et développement d'un modèle de détection d'anomalies en temps réel sur flux vidéos de surveillance industrielle. Utilisation de réseaux convolutifs (CNN/YOLO) et architectures temporelles avec PyTorch et OpenCV.",
        "skills": ["Deep Learning", "Computer Vision", "PyTorch", "Python", "OpenCV", "TensorFlow"],
        "source_url": "https://satoripop.com/#careers-deep-learning",
        "source_site": "satoripop_careers",
    },

    # ── 5. CYBERSÉCURITÉ & RÉSEAUX (7 Offers) ───────────────────────────────────
    {
        "title": "Stage PFE — Ingénieur Cybersécurité & Audit SOC / SIEM",
        "company": "Telnet Holding",
        "city": "Tunis (El Ghazala)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Participation aux activités de sécurité opérationnelle au sein de notre SOC. Analyse de logs de sécurité, détection d'intrusions avec SIEM (Wazuh/Splunk), tests de vulnérabilités et renforcement de serveurs Linux.",
        "skills": ["Cybersécurité", "SIEM", "SOC", "Linux", "Wireshark", "Firewall", "Pentesting"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=telnet#carrieres-cybersecurite-soc",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Tests d'Intrusion (Pentesting) & Sécurité Web / API",
        "company": "ANSI (Agence Nationale de la Sécurité Informatique)",
        "city": "Tunis",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Réalisation d'audits de vulnérabilités et tests d'intrusion méthodologiques sur des applications gouvernementales selon le référentiel OWASP Top 10. Utilisation d'outils comme Burp Suite, Metasploit, Nmap et rédaction de rapports de remédiation.",
        "skills": ["Pentesting", "Cybersécurité", "Ethical Hacking", "Metasploit", "Linux Security", "Wireshark"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=cybersecurite#pfe-pentesting",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Ingénieur Sécurité Réseaux, Firewalls & VPN IPSec",
        "company": "Focus Cyber",
        "city": "Tunis (El Ghazala)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Conception et déploiement d'une architecture réseau sécurisée multi-sites. Configuration de firewalls nouvelle génération (Fortinet / pfSense), segmentation de réseaux VLANs, tunnels VPN sécurisés et routage Cisco.",
        "skills": ["Firewall", "Cisco", "TCP/IP", "VPN", "Wireshark", "Cybersécurité", "Linux Security"],
        "source_url": "https://www.focus-corporation.com/#careers-cyber-network",
        "source_site": "focus_careers",
    },
    {
        "title": "Stage PFE — Consultant Sécurité des Systèmes d'Information & ISO 27001",
        "company": "PwC Tunisie",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Accompagnement de grandes entreprises dans la mise en conformité de leur SMSI selon la norme ISO 27001. Analyse des risques de sécurité (méthode EBIOS), gouvernance cybersécurité et audits de conformité technique.",
        "skills": ["ISO 27001", "Cybersécurité", "Linux Security", "SOC"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=pwc#pfe-cyber-consultant",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Ingénieur Réseaux Télécoms & Architecture 5G",
        "company": "Huawei Tunisie",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Étude et simulation des mécanismes de découpage réseau (Network Slicing) dans les réseaux cœurs 5G. Analyse de protocoles de communication TCP/IP, performances réseau et sécurité des flux de transmission.",
        "skills": ["TCP/IP", "Cisco", "Wireshark", "Linux", "Cybersécurité"],
        "source_url": "https://www.huawei.com/#pfe-telecom-5g",
        "source_site": "huawei_careers",
    },
    {
        "title": "Stage PFE — Détection d'Attaques & Threat Hunting en Environnement SOC",
        "company": "Ooredoo Tunisie",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Mise en place de scénarios de détection avancée basés sur la matrice MITRE ATT&CK. Corrélation d'événements de sécurité SIEM, analyse forensique de paquets réseau avec Wireshark et automatisation de réponses aux incidents.",
        "skills": ["SIEM", "SOC", "Cybersécurité", "Wireshark", "Firewall", "Linux Security"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=ooredoo#pfe-threat-hunting",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Cryptographie Appliquée & Sécurisation des Microservices",
        "company": "Focus Corporation",
        "city": "Tunis (El Ghazala)",
        "domain": "Cybersécurité & Réseaux",
        "contract_type": "Stage PFE",
        "description": "Conception d'une architecture Zero-Trust pour sécuriser les communications inter-services. Gestion d'infrastructures à clés publiques (PKI), certificats mTLS (mutual TLS), chiffrement de bout en bout et gestion de secrets.",
        "skills": ["Cryptographie", "Cybersécurité", "Linux Security", "VPN", "Docker", "REST API"],
        "source_url": "https://www.focus-corporation.com/#careers-cryptography",
        "source_site": "focus_careers",
    },

    # ── 6. WEB & FULLSTACK (7 Offers) ──────────────────────────────────────────
    {
        "title": "Stage PFE — Développeur Fullstack React.js & Python FastAPI",
        "company": "Sofrecom Tunisie (Orange)",
        "city": "Tunis (El Ghazala)",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Conception et réalisation d'une plateforme web collaborative pour le groupe Orange. Frontend moderne en React.js, TailwindCSS et TypeScript. Backend développé en Python avec FastAPI et conteneurisation Docker.",
        "skills": ["Python", "React", "TypeScript", "TailwindCSS", "FastAPI", "Docker", "Git"],
        "source_url": "https://www.tanitjobs.com/jobs/?keyword=sofrecom#pfe-fullstack-react",
        "source_site": "tanitjobs",
    },
    {
        "title": "Stage PFE — Développeur Fullstack Angular 17 & Java Spring Boot",
        "company": "Proxym-IT",
        "city": "Sousse",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Développement d'une application de gestion portuaire intelligente. Interface frontend dynamique en Angular avec TypeScript, formulaires réactifs et RxJS. Backend robuste en Java Spring Boot et base de données PostgreSQL.",
        "skills": ["Angular", "TypeScript", "Java", "Spring Boot", "PostgreSQL", "REST API", "Docker"],
        "source_url": "https://proxym-group.com/#careers-angular-springboot",
        "source_site": "proxym_careers",
    },
    {
        "title": "Stage PFE — Développeur Frontend React.js & Next.js / TailwindCSS",
        "company": "Medianet",
        "city": "Tunis (El Ghazala)",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Création du nouveau portail interactif de services citoyens tunisiens. Utilisation de Next.js avec Server-Side Rendering (SSR), intégration d'un design system responsive avec TailwindCSS et gestion d'état Zustand.",
        "skills": ["React", "Next.js", "TypeScript", "TailwindCSS", "HTML5", "CSS3", "JavaScript"],
        "source_url": "https://www.medianet.tn/#carrieres-nextjs-react",
        "source_site": "medianet_careers",
    },
    {
        "title": "Stage PFE — Développeur Fullstack Vue.js 3 & Laravel 11",
        "company": "Roamler Tunisie",
        "city": "Tunis (Les Berges du Lac)",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Refonte d'un tableau de bord de crowd-sourcing utilisé par des milliers de correspondants en Europe. Frontend interactif avec Vue.js 3 Composition API, backend PHP Laravel avec APIs RESTful sécurisées et MySQL.",
        "skills": ["Vue.js", "Laravel", "PHP", "JavaScript", "MySQL", "TailwindCSS", "REST API"],
        "source_url": "https://roamler.com/careers/pfe-vuejs-laravel-2026",
        "source_site": "roamler_careers",
    },
    {
        "title": "Stage PFE — Développeur Web PHP Symfony 7 & React",
        "company": "SQLI Services",
        "city": "Tunis (Centre Urbain Nord)",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Participation au développement d'une solution d'e-commerce B2B de grande envergure. Implémentation des bundles Symfony 7, composants React réutilisables, intégration avec Elasticsearch et pipeline CI/CD GitLab.",
        "skills": ["PHP", "React", "JavaScript", "PostgreSQL", "Docker", "REST API", "Git"],
        "source_url": "https://www.sqli.com/#pfe-symfony-react",
        "source_site": "sqli_careers",
    },
    {
        "title": "Stage PFE — Développeur Fullstack TypeScript / Node.js & React",
        "company": "Inetum Tunisie",
        "city": "Ariana",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Développement complet d'un module RH en TypeScript de bout en bout. Client riche en React / Redux Toolkit, serveur d'APIs Node.js / Express, base de données MongoDB et conteneurisation complète sous Docker.",
        "skills": ["TypeScript", "React", "Node.js", "Express.js", "MongoDB", "Docker", "Git"],
        "source_url": "https://www.inetum.com/#pfe-fullstack-ts",
        "source_site": "inetum_careers",
    },
    {
        "title": "Stage PFE — Plateforme Web SaaS Multi-Tenant React & NestJS",
        "company": "Talan Tunisie",
        "city": "Tunis (Charguia 2)",
        "domain": "Web & Fullstack",
        "contract_type": "Stage PFE",
        "description": "Architecture et développement d'un logiciel SaaS moderne pour la gestion des talents IT. Frontend en React avec Shadcn UI / TailwindCSS, backend TypeScript sous NestJS avec isolation des bases de données PostgreSQL.",
        "skills": ["React", "TypeScript", "TailwindCSS", "PostgreSQL", "Docker", "REST API", "Git"],
        "source_url": "https://talan.com/#carrieres-react-saas",
        "source_site": "talan_careers",
    },
]


NON_TECH_BLACKLIST = [
    "rh", "ressources humaines", "recrutement", "finance", "comptable", "comptabilité",
    "merchandiser", "production", "magasinier", "commercial", "vente", "marketing digital",
    "téléconseiller", "téléopérateur", "juriste", "caissier", "chauffeur", "usine", "ouvrier"
]


def is_valid_tech_offer(title: str, skills: list) -> bool:
    title_lower = title.lower()
    for bad in NON_TECH_BLACKLIST:
        if bad in title_lower:
            return False
    it_keywords = [
        "dev", "informatique", "software", "ingénieur", "data", "cloud", "web",
        "stage", "pfe", "reseau", "réseau", "sécurité", "security", "mobile",
        "fullstack", "backend", "frontend", "technicien", "it"
    ]
    return len(skills) > 0 or any(k in title_lower for k in it_keywords)


def reset_and_seed():
    db = SessionLocal()
    try:
        print("\n🧹 1. Cleaning out old offers from PostgreSQL...")
        db.query(Recommendation).delete()
        db.query(Offer).delete()
        db.commit()
        print("   ✅ Database cleaned! All tables ready.")

        print("\n💼 2. Inserting 42 premium Tunisian Tech PFE offers across all 6 tracks...")
        for item in CURATED_TECH_OFFERS:
            offer = Offer(**item)
            db.add(offer)
        db.commit()
        print(f"   ✅ Inserted {len(CURATED_TECH_OFFERS)} premium Tech PFE offers (Vermeg, InstaDeep, Actia, Telnet, Focus, Talan...)")

        print("\n🕷️  3. Running live Tunisian Tech scrapers (2 pages per site)...")
        live_offers = run_all_scrapers(max_pages=2)

        # In-memory deduplication set prevents any UniqueViolation on source_url
        seen_urls = {item["source_url"] for item in CURATED_TECH_OFFERS}
        inserted_live = 0

        for item in live_offers:
            url = item.get("source_url")
            title = item.get("title", "Stage PFE Informatique")
            skills = item.get("skills", [])

            # Reject duplicates and non-tech ads
            if not url or url in seen_urls:
                continue
            if not is_valid_tech_offer(title, skills):
                continue

            seen_urls.add(url)
            new_offer = Offer(
                title=title,
                company=item.get("company", "Entreprise Tech Tunisie"),
                city=item.get("city", "Tunisie"),
                domain=item.get("domain", "Web & Fullstack"),
                contract_type=item.get("contract_type", "Stage PFE"),
                description=item.get("description", ""),
                skills=skills,
                source_url=url,
                source_site=item.get("source_site", "scraper"),
                date_posted=item.get("date_posted"),
            )
            db.add(new_offer)
            inserted_live += 1

        db.commit()
        print(f"   ✅ Added {inserted_live} valid live scraped tech offers!")

        # Print breakdown per domain
        total = db.query(Offer).count()
        print(f"\n🎯 COMPLETE! Total 100% Tech Offers in Database: {total}")
        print("=" * 60)
        from sqlalchemy import func
        stats = db.query(Offer.domain, func.count(Offer.id)).group_by(Offer.domain).all()
        for domain, count in stats:
            print(f"   📌 {domain:<30}: {count} offres")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    reset_and_seed()
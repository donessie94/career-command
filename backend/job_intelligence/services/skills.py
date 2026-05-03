"""Utilities for normalizing and categorizing job-posting skills."""

import re

from job_intelligence.models import Skill


# Preserving "+", "#", and "." because skills like C++, C#, F#, .NET,
# Node.js, and Next.js need those symbols before alias matching.
_SEPARATOR_RE = re.compile(r"[/|,;:_\-()\[\]{}]+")
_EXTRA_SYMBOL_RE = re.compile(r"[^a-z0-9+#.\s]")


SKILL_ALIASES = {
    # Programming languages
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "c plus plus": "c++",
    "cpp": "c++",
    "c++": "c++",
    "c sharp": "c#",
    "csharp": "c#",
    "c#": "c#",
    "golang": "go",
    "go lang": "go",
    "f sharp": "f#",
    "f#": "f#",

    # SQL / databases
    "postgres": "postgresql",
    "postgres sql": "postgresql",
    "postgresql": "postgresql",
    "mysql": "mysql",
    "maria db": "mariadb",
    "mariadb": "mariadb",
    "ms sql": "sql server",
    "mssql": "sql server",
    "microsoft sql server": "sql server",
    "sql server": "sql server",
    "mongo": "mongodb",
    "mongo db": "mongodb",
    "mongodb": "mongodb",
    "redis": "redis",
    "sqlite": "sqlite",
    "oracle db": "oracle database",
    "oracle database": "oracle database",
    "dynamo db": "dynamodb",
    "dynamodb": "dynamodb",
    "elastic search": "elasticsearch",
    "elasticsearch": "elasticsearch",

    # Frontend
    "reactjs": "react",
    "react.js": "react",
    "react": "react",
    "nextjs": "next.js",
    "next": "next.js",
    "next.js": "next.js",
    "vuejs": "vue",
    "vue.js": "vue",
    "vue": "vue",
    "angularjs": "angular",
    "angular": "angular",
    "html5": "html",
    "html": "html",
    "css3": "css",
    "css": "css",
    "tailwindcss": "tailwind css",
    "tailwind": "tailwind css",
    "tailwind css": "tailwind css",
    "bootstrap": "bootstrap",

    # Backend / frameworks
    "nodejs": "node.js",
    "node": "node.js",
    "node.js": "node.js",
    "expressjs": "express",
    "express.js": "express",
    "express": "express",
    "django rest framework": "django rest framework",
    "drf": "django rest framework",
    "django": "django",
    "flask": "flask",
    "fast api": "fastapi",
    "fastapi": "fastapi",
    "spring boot": "spring boot",
    "springboot": "spring boot",
    "spring": "spring",
    "asp.net": "asp.net",
    "asp net": "asp.net",
    "dotnet": ".net",
    ".net": ".net",
    "rest": "rest api",
    "rest api": "rest api",
    "graphql": "graphql",
    "microservice": "microservices",
    "microservices": "microservices",
    "api design": "api design",
    "backend development": "backend development",

    # Cloud
    "amazon web services": "aws",
    "aws": "aws",
    "azure": "azure",
    "microsoft azure": "azure",
    "google cloud": "gcp",
    "google cloud platform": "gcp",
    "gcp": "gcp",
    "aws s3": "s3",
    "s3": "s3",
    "aws ec2": "ec2",
    "ec2": "ec2",
    "aws lambda": "lambda",
    "lambda": "lambda",
    "cloud formation": "cloudformation",
    "cloudformation": "cloudformation",

    # DevOps / tools
    "docker": "docker",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "github actions": "github actions",
    "git hub actions": "github actions",
    "gitlab ci": "gitlab ci/cd",
    "gitlab cicd": "gitlab ci/cd",
    "gitlab ci cd": "gitlab ci/cd",
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
    "ci/cd": "ci/cd",
    "terraform": "terraform",
    "jenkins": "jenkins",
    "linux": "linux",
    "bash": "bash",
    "git": "git",

    # Data / analytics
    "excel": "excel",
    "microsoft excel": "excel",
    "powerbi": "power bi",
    "power bi": "power bi",
    "tableau": "tableau",
    "looker": "looker",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "spark": "apache spark",
    "apache spark": "apache spark",
    "pyspark": "pyspark",
    "airflow": "apache airflow",
    "apache airflow": "apache airflow",
    "snowflake": "snowflake",
    "databricks": "databricks",
    "data analytics": "data analysis",
    "data analysis": "data analysis",
    "data visualization": "data visualization",
    "etl": "etl",
    "data modeling": "data modeling",

    # Machine learning / AI
    "machine learning": "machine learning",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "scikit-learn": "scikit-learn",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",

    # Product / collaboration tools
    "jira": "jira",
    "confluence": "confluence",
    "postman": "postman",
    "figma": "figma",
    "notion": "notion",
    "slack": "slack",

    # Soft skills
    "communication skills": "communication",
    "communication": "communication",
    "leadership": "leadership",
    "teamwork": "teamwork",
    "collaboration": "collaboration",
    "problem solving": "problem solving",
    "critical thinking": "critical thinking",
    "attention to detail": "attention to detail",
    "detail oriented": "attention to detail",
    "stakeholder communication": "stakeholder communication",
}


SKILL_DISPLAY_NAMES = {
    # Programming languages
    "python": "Python",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "java": "Java",
    "c": "C",
    "c++": "C++",
    "c#": "C#",
    "f#": "F#",
    "go": "Go",
    "rust": "Rust",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "php": "PHP",
    "ruby": "Ruby",
    "r": "R",
    "scala": "Scala",
    "bash": "Bash",
    "sql": "SQL",

    # Databases
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mariadb": "MariaDB",
    "sql server": "SQL Server",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "oracle database": "Oracle Database",
    "dynamodb": "DynamoDB",
    "elasticsearch": "Elasticsearch",

    # Frontend
    "react": "React",
    "next.js": "Next.js",
    "vue": "Vue",
    "angular": "Angular",
    "html": "HTML",
    "css": "CSS",
    "tailwind css": "Tailwind CSS",
    "bootstrap": "Bootstrap",

    # Backend / frameworks
    "node.js": "Node.js",
    "express": "Express",
    "django": "Django",
    "django rest framework": "Django REST Framework",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    ".net": ".NET",
    "asp.net": "ASP.NET",
    "rest api": "REST API",
    "graphql": "GraphQL",
    "microservices": "Microservices",
    "api design": "API Design",
    "backend development": "Backend Development",

    # Cloud
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "s3": "Amazon S3",
    "ec2": "Amazon EC2",
    "lambda": "AWS Lambda",
    "cloudformation": "AWS CloudFormation",

    # DevOps
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "github actions": "GitHub Actions",
    "gitlab ci/cd": "GitLab CI/CD",
    "ci/cd": "CI/CD",
    "terraform": "Terraform",
    "jenkins": "Jenkins",
    "linux": "Linux",
    "git": "Git",

    # Data
    "excel": "Excel",
    "power bi": "Power BI",
    "tableau": "Tableau",
    "looker": "Looker",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "apache spark": "Apache Spark",
    "pyspark": "PySpark",
    "apache airflow": "Apache Airflow",
    "snowflake": "Snowflake",
    "databricks": "Databricks",
    "data analysis": "Data Analysis",
    "data visualization": "Data Visualization",
    "etl": "ETL",
    "data modeling": "Data Modeling",

    # Machine learning
    "machine learning": "Machine Learning",
    "artificial intelligence": "Artificial Intelligence",
    "scikit-learn": "scikit-learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",
    "natural language processing": "Natural Language Processing",

    # Tools
    "jira": "Jira",
    "confluence": "Confluence",
    "postman": "Postman",
    "figma": "Figma",
    "notion": "Notion",
    "slack": "Slack",

    # Soft skills
    "communication": "Communication",
    "leadership": "Leadership",
    "teamwork": "Teamwork",
    "collaboration": "Collaboration",
    "problem solving": "Problem Solving",
    "critical thinking": "Critical Thinking",
    "attention to detail": "Attention to Detail",
    "stakeholder communication": "Stakeholder Communication",
}


SKILL_CATEGORY_MAP = {
    # Programming languages
    "python": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "javascript": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "typescript": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "java": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "c": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "c++": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "c#": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "f#": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "go": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "rust": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "kotlin": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "swift": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "php": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "ruby": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "r": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "scala": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "bash": Skill.SkillCategory.PROGRAMMING_LANGUAGE,
    "sql": Skill.SkillCategory.PROGRAMMING_LANGUAGE,

    # Frameworks
    "django": Skill.SkillCategory.FRAMEWORK,
    "django rest framework": Skill.SkillCategory.FRAMEWORK,
    "flask": Skill.SkillCategory.FRAMEWORK,
    "fastapi": Skill.SkillCategory.FRAMEWORK,
    "spring": Skill.SkillCategory.FRAMEWORK,
    "spring boot": Skill.SkillCategory.FRAMEWORK,
    "express": Skill.SkillCategory.FRAMEWORK,
    "node.js": Skill.SkillCategory.FRAMEWORK,
    ".net": Skill.SkillCategory.FRAMEWORK,
    "asp.net": Skill.SkillCategory.FRAMEWORK,

    # Frontend
    "react": Skill.SkillCategory.FRONTEND,
    "next.js": Skill.SkillCategory.FRONTEND,
    "vue": Skill.SkillCategory.FRONTEND,
    "angular": Skill.SkillCategory.FRONTEND,
    "html": Skill.SkillCategory.FRONTEND,
    "css": Skill.SkillCategory.FRONTEND,
    "tailwind css": Skill.SkillCategory.FRONTEND,
    "bootstrap": Skill.SkillCategory.FRONTEND,

    # Backend
    "rest api": Skill.SkillCategory.BACKEND,
    "graphql": Skill.SkillCategory.BACKEND,
    "microservices": Skill.SkillCategory.BACKEND,
    "api design": Skill.SkillCategory.BACKEND,
    "backend development": Skill.SkillCategory.BACKEND,

    # Databases
    "postgresql": Skill.SkillCategory.DATABASE,
    "mysql": Skill.SkillCategory.DATABASE,
    "mariadb": Skill.SkillCategory.DATABASE,
    "sql server": Skill.SkillCategory.DATABASE,
    "mongodb": Skill.SkillCategory.DATABASE,
    "redis": Skill.SkillCategory.DATABASE,
    "sqlite": Skill.SkillCategory.DATABASE,
    "oracle database": Skill.SkillCategory.DATABASE,
    "dynamodb": Skill.SkillCategory.DATABASE,
    "elasticsearch": Skill.SkillCategory.DATABASE,

    # Cloud
    "aws": Skill.SkillCategory.CLOUD,
    "azure": Skill.SkillCategory.CLOUD,
    "gcp": Skill.SkillCategory.CLOUD,
    "s3": Skill.SkillCategory.CLOUD,
    "ec2": Skill.SkillCategory.CLOUD,
    "lambda": Skill.SkillCategory.CLOUD,
    "cloudformation": Skill.SkillCategory.CLOUD,

    # DevOps
    "docker": Skill.SkillCategory.DEVOPS,
    "kubernetes": Skill.SkillCategory.DEVOPS,
    "github actions": Skill.SkillCategory.DEVOPS,
    "gitlab ci/cd": Skill.SkillCategory.DEVOPS,
    "ci/cd": Skill.SkillCategory.DEVOPS,
    "terraform": Skill.SkillCategory.DEVOPS,
    "jenkins": Skill.SkillCategory.DEVOPS,
    "linux": Skill.SkillCategory.DEVOPS,

    # Data
    "excel": Skill.SkillCategory.DATA,
    "power bi": Skill.SkillCategory.DATA,
    "tableau": Skill.SkillCategory.DATA,
    "looker": Skill.SkillCategory.DATA,
    "pandas": Skill.SkillCategory.DATA,
    "numpy": Skill.SkillCategory.DATA,
    "matplotlib": Skill.SkillCategory.DATA,
    "seaborn": Skill.SkillCategory.DATA,
    "apache spark": Skill.SkillCategory.DATA,
    "pyspark": Skill.SkillCategory.DATA,
    "apache airflow": Skill.SkillCategory.DATA,
    "snowflake": Skill.SkillCategory.DATA,
    "databricks": Skill.SkillCategory.DATA,
    "data analysis": Skill.SkillCategory.DATA,
    "data visualization": Skill.SkillCategory.DATA,
    "etl": Skill.SkillCategory.DATA,
    "data modeling": Skill.SkillCategory.DATA,

    # Machine learning
    "machine learning": Skill.SkillCategory.MACHINE_LEARNING,
    "artificial intelligence": Skill.SkillCategory.MACHINE_LEARNING,
    "scikit-learn": Skill.SkillCategory.MACHINE_LEARNING,
    "tensorflow": Skill.SkillCategory.MACHINE_LEARNING,
    "pytorch": Skill.SkillCategory.MACHINE_LEARNING,
    "keras": Skill.SkillCategory.MACHINE_LEARNING,
    "natural language processing": Skill.SkillCategory.MACHINE_LEARNING,

    # Tools
    "git": Skill.SkillCategory.TOOL,
    "jira": Skill.SkillCategory.TOOL,
    "confluence": Skill.SkillCategory.TOOL,
    "postman": Skill.SkillCategory.TOOL,
    "figma": Skill.SkillCategory.TOOL,
    "notion": Skill.SkillCategory.TOOL,
    "slack": Skill.SkillCategory.TOOL,

    # Soft skills
    "communication": Skill.SkillCategory.SOFT_SKILL,
    "leadership": Skill.SkillCategory.SOFT_SKILL,
    "teamwork": Skill.SkillCategory.SOFT_SKILL,
    "collaboration": Skill.SkillCategory.SOFT_SKILL,
    "problem solving": Skill.SkillCategory.SOFT_SKILL,
    "critical thinking": Skill.SkillCategory.SOFT_SKILL,
    "attention to detail": Skill.SkillCategory.SOFT_SKILL,
    "stakeholder communication": Skill.SkillCategory.SOFT_SKILL,
}


def normalize_skill_name(name: str) -> str:
    """Normalize a skill name for consistent matching and storage."""

    cleaned = name.strip().lower()
    cleaned = _SEPARATOR_RE.sub(" ", cleaned)
    cleaned = _EXTRA_SYMBOL_RE.sub("", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return SKILL_ALIASES.get(cleaned, cleaned)


def prettify_skill_name(normalized_name: str) -> str:
    """Return a clean display name for a normalized skill name."""

    return SKILL_DISPLAY_NAMES.get(
        normalized_name,
        normalized_name.title(),
    )


def guess_skill_category(normalized_name: str) -> str:
    """Return the best known category for a normalized skill name."""

    return SKILL_CATEGORY_MAP.get(
        normalized_name,
        Skill.SkillCategory.OTHER,
    )


def get_or_create_skill(name: str) -> Skill:
    """Return an existing skill or create one with a guessed category."""

    normalized_name = normalize_skill_name(name)
    category = guess_skill_category(normalized_name)

    skill, _created = Skill.objects.get_or_create(
        normalized_name=normalized_name,
        defaults={
            "name": prettify_skill_name(normalized_name),
            "category": category,
        },
    )

    return skill



def _contains_skill_alias(search_text: str, alias: str) -> bool:
    """Return True if a skill alias appears as a standalone phrase."""

    pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
    return re.search(pattern, search_text, flags=re.IGNORECASE) is not None



def extract_skills_from_text(raw_text: str) -> list[dict[str, str]]:
    """Extract known skills from raw job posting text."""

    search_text = raw_text.lower()
    search_terms = set(SKILL_ALIASES) | set(SKILL_CATEGORY_MAP)
    found_skills = {}

    for term in search_terms:
        if _contains_skill_alias(search_text, term):
            normalized_name = normalize_skill_name(term)

            found_skills[normalized_name] = {
                "name": prettify_skill_name(normalized_name),
                "normalized_name": normalized_name,
                "category": guess_skill_category(normalized_name),
                "source_text": term,
            }

    return sorted(
        found_skills.values(),
        key=lambda skill: skill["name"].lower(), # sorting key
    )
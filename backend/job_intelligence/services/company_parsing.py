"""Utilities for guessing company names from job posting text and URLs."""

from urllib.parse import urlparse
import re



KNOWN_COMPANIES = {
    # Las Vegas / Nevada employers
    "caesars": "Caesars Entertainment",
    "caesars entertainment": "Caesars Entertainment",
    "mgm": "MGM Resorts International",
    "mgm grand": "MGM Resorts International",
    "mgm resorts": "MGM Resorts International",
    "mgm resorts international": "MGM Resorts International",
    "wynn": "Wynn Resorts",
    "wynn resorts": "Wynn Resorts",
    "encore": "Wynn Resorts",
    "venetian": "The Venetian Resort Las Vegas",
    "the venetian": "The Venetian Resort Las Vegas",
    "venetian resort": "The Venetian Resort Las Vegas",
    "palazzo": "The Venetian Resort Las Vegas",
    "station casinos": "Station Casinos",
    "red rock resorts": "Red Rock Resorts",
    "boyd gaming": "Boyd Gaming",
    "golden entertainment": "Golden Entertainment",
    "resorts world": "Resorts World Las Vegas",
    "resorts world las vegas": "Resorts World Las Vegas",
    "fontainebleau": "Fontainebleau Las Vegas",
    "fontainebleau las vegas": "Fontainebleau Las Vegas",
    "circa": "Circa Resort & Casino",
    "circa resort": "Circa Resort & Casino",
    "circa resort casino": "Circa Resort & Casino",
    "south point": "South Point Hotel Casino & Spa",
    "south point casino": "South Point Hotel Casino & Spa",
    "treasure island": "Treasure Island Las Vegas",
    "ti las vegas": "Treasure Island Las Vegas",
    "the strat": "The STRAT Hotel, Casino & Tower",
    "strat": "The STRAT Hotel, Casino & Tower",
    "sphere": "Sphere Entertainment",
    "sphere entertainment": "Sphere Entertainment",
    "las vegas sands": "Las Vegas Sands",
    "sands": "Las Vegas Sands",
    "allegiant": "Allegiant Air",
    "allegiant air": "Allegiant Air",
    "allegiantair": "Allegiant Air",
    "switch": "Switch",
    "zappos": "Zappos",
    "credit one": "Credit One Bank",
    "credit one bank": "Credit One Bank",
    "aristocrat": "Aristocrat Gaming",
    "aristocrat gaming": "Aristocrat Gaming",
    "light & wonder": "Light & Wonder",
    "light and wonder": "Light & Wonder",
    "igt": "International Game Technology",
    "international game technology": "International Game Technology",

    # Major big tech / platforms
    "google": "Google",
    "alphabet": "Alphabet",
    "microsoft": "Microsoft",
    "amazon": "Amazon",
    "aws": "Amazon Web Services",
    "apple": "Apple",
    "meta": "Meta",
    "facebook": "Meta",
    "instagram": "Meta",
    "netflix": "Netflix",
    "nvidia": "NVIDIA",
    "tesla": "Tesla",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "xai": "xAI",
    "deepmind": "Google DeepMind",

    # Enterprise software / cloud / SaaS
    "oracle": "Oracle",
    "salesforce": "Salesforce",
    "adobe": "Adobe",
    "servicenow": "ServiceNow",
    "workday": "Workday",
    "sap": "SAP",
    "snowflake": "Snowflake",
    "databricks": "Databricks",
    "mongodb": "MongoDB",
    "elastic": "Elastic",
    "elasticsearch": "Elastic",
    "atlassian": "Atlassian",
    "confluent": "Confluent",
    "hashicorp": "HashiCorp",
    "cloudflare": "Cloudflare",
    "twilio": "Twilio",
    "okta": "Okta",
    "docusign": "DocuSign",
    "dropbox": "Dropbox",
    "box": "Box",
    "zoom": "Zoom",
    "slack": "Slack",
    "notion": "Notion",
    "airtable": "Airtable",
    "asana": "Asana",
    "monday": "monday.com",
    "hubspot": "HubSpot",
    "zendesk": "Zendesk",

    # Developer tools / infra / cybersecurity
    "github": "GitHub",
    "gitlab": "GitLab",
    "docker": "Docker",
    "jetbrains": "JetBrains",
    "vercel": "Vercel",
    "netlify": "Netlify",
    "digitalocean": "DigitalOcean",
    "heroku": "Heroku",
    "datadog": "Datadog",
    "new relic": "New Relic",
    "sentry": "Sentry",
    "splunk": "Splunk",
    "palo alto networks": "Palo Alto Networks",
    "crowdstrike": "CrowdStrike",
    "zscaler": "Zscaler",
    "cloudstrike": "CrowdStrike",
    "sentinelone": "SentinelOne",
    "fortinet": "Fortinet",
    "rapid7": "Rapid7",
    "check point": "Check Point",
    "wiz": "Wiz",

    # Semiconductors / hardware / systems
    "intel": "Intel",
    "amd": "AMD",
    "qualcomm": "Qualcomm",
    "broadcom": "Broadcom",
    "arm": "Arm",
    "micron": "Micron",
    "texas instruments": "Texas Instruments",
    "ti": "Texas Instruments",
    "analog devices": "Analog Devices",
    "marvell": "Marvell",
    "supermicro": "Supermicro",
    "dell": "Dell",
    "dell technologies": "Dell Technologies",
    "hp": "HP",
    "hewlett packard": "Hewlett Packard Enterprise",
    "hpe": "Hewlett Packard Enterprise",
    "lenovo": "Lenovo",
    "cisco": "Cisco",
    "juniper": "Juniper Networks",
    "juniper networks": "Juniper Networks",
    "arista": "Arista Networks",
    "arista networks": "Arista Networks",

    # Fintech / payments / crypto-ish tech
    "stripe": "Stripe",
    "paypal": "PayPal",
    "block": "Block",
    "square": "Block",
    "adyen": "Adyen",
    "affirm": "Affirm",
    "coinbase": "Coinbase",
    "robinhood": "Robinhood",
    "plaid": "Plaid",
    "chime": "Chime",
    "sofi": "SoFi",
    "intuit": "Intuit",
    "fidelity": "Fidelity",
    "fiserv": "Fiserv",
    "fis": "FIS",
    "mastercard": "Mastercard",
    "visa": "Visa",

    # Consumer internet / marketplaces / apps
    "uber": "Uber",
    "lyft": "Lyft",
    "airbnb": "Airbnb",
    "doordash": "DoorDash",
    "instacart": "Instacart",
    "pinterest": "Pinterest",
    "reddit": "Reddit",
    "snap": "Snap",
    "snapchat": "Snap",
    "tiktok": "TikTok",
    "bytedance": "ByteDance",
    "spotify": "Spotify",
    "shopify": "Shopify",
    "etsy": "Etsy",
    "ebay": "eBay",
    "wayfair": "Wayfair",
    "zillow": "Zillow",
    "opendoor": "Opendoor",
    "yelp": "Yelp",
    "booking": "Booking Holdings",
    "booking.com": "Booking.com",
    "expedia": "Expedia Group",

    # Gaming / entertainment tech
    "roblox": "Roblox",
    "unity": "Unity",
    "epic games": "Epic Games",
    "activision": "Activision Blizzard",
    "blizzard": "Activision Blizzard",
    "electronic arts": "Electronic Arts",
    "ea": "Electronic Arts",
    "take-two": "Take-Two Interactive",
    "riot games": "Riot Games",
    "riot": "Riot Games",
    "nintendo": "Nintendo",
    "sony": "Sony",
    "playstation": "Sony Interactive Entertainment",
    "microsoft gaming": "Microsoft Gaming",

    # Consulting / IT services / digital engineering
    "accenture": "Accenture",
    "deloitte": "Deloitte",
    "cognizant": "Cognizant",
    "infosys": "Infosys",
    "tcs": "Tata Consultancy Services",
    "tata consultancy services": "Tata Consultancy Services",
    "wipro": "Wipro",
    "capgemini": "Capgemini",
    "epam": "EPAM Systems",
    "epam systems": "EPAM Systems",
    "globant": "Globant",
    "thoughtworks": "Thoughtworks",
    "slalom": "Slalom",
    "brillio": "Brillio",
    "ust": "UST",
    "ltimindtree": "LTIMindtree",
    "mindtree": "LTIMindtree",
    "hcltech": "HCLTech",
    "hcl": "HCLTech",

    # Job boards / recruiting platforms / HR tech
    "linkedin": "LinkedIn",
    "indeed": "Indeed",
    "glassdoor": "Glassdoor",
    "ziprecruiter": "ZipRecruiter",
    "greenhouse": "Greenhouse",
    "lever": "Lever",
    "workable": "Workable",
    "smartrecruiters": "SmartRecruiters",

    # Local / transportation / aerospace / engineering tech examples
    "allegiant": "Allegiant",
    "allegiant air": "Allegiant Air",
    "the boring company": "The Boring Company",
    "boring company": "The Boring Company",
    "spacex": "SpaceX",
    "blue origin": "Blue Origin",
    "boeing": "Boeing",
    "lockheed martin": "Lockheed Martin",
    "northrop grumman": "Northrop Grumman",
    "raytheon": "RTX",
    "rtx": "RTX",
}

def _normalize_search_text(text: str) -> str:
    """Normalize text before matching known company names."""

    return text.lower().strip()



def _get_first_words(text: str, word_limit: int = 50) -> str:
    """Return the first N words from text as lowercase searchable text."""

    normalized_text = _normalize_search_text(text)
    words = normalized_text.split()
    return " ".join(words[:word_limit])



def _get_searchable_url_text(source_url: str) -> str:
    """Return URL domain and path as lowercase searchable text."""

    parsed_url = urlparse(source_url)
    return _normalize_search_text(
        f"{parsed_url.netloc} {parsed_url.path}"
    )



def _contains_company_alias(search_text: str, alias: str) -> bool:
    """Return True if alias appears as a standalone phrase."""

    pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
    return re.search(pattern, search_text, flags=re.IGNORECASE) is not None



def _find_known_company(search_text: str) -> str:
    """Return a known company display name found in search text."""

    for alias, display_name in KNOWN_COMPANIES.items():
        if _contains_company_alias(search_text, alias):
            return display_name
    return ""



def guess_company_name(
    raw_text: str = "",
    source_url: str = "",
    provided_company_name: str = "",
) -> str:
    """Guess a company name from user input, URL, or job posting text."""

    cleaned_company_name = provided_company_name.strip()

    if cleaned_company_name:
        return cleaned_company_name

    if source_url:
        company_name = _find_known_company(
            _get_searchable_url_text(source_url)
        )

        if company_name:
            return company_name

    if raw_text:
        company_name = _find_known_company(
            _get_first_words(raw_text, word_limit=50)
        )

        if company_name:
            return company_name

    return ""
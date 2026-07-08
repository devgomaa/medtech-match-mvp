"""
Synthetic data generator — MedTech Global Connect
All data below is fictional/synthetic (Synthetic Data), for demo/testing purposes only.
"""
import random

SECTORS = [
    "Pharmaceuticals",
    "Nutraceuticals",
    "Consumer Health Products",
    "Medical Supplies",
    "Medical Devices",
    "MedTech",
]

CHINA_CITIES = ["Shenzhen", "Shanghai", "Suzhou", "Guangzhou", "Hangzhou", "Beijing", "Nanjing", "Chengdu"]

MANUFACTURERS = [
    {
        "name": "Sinopharm BioGen Labs",
        "country": "China", "city": "Shanghai",
        "sector": "Pharmaceuticals",
        "sub_specialty": "Generic oncology drugs, biosimilars",
        "description": "Manufacturer of biosimilar oncology therapeutics and generic injectables, GMP-certified, exporting to Southeast Asia and Africa.",
        "tags": "biosimilars,oncology,injectables,GMP,generics",
        "certifications": "GMP,ISO 13485,CFDA",
        "target_markets": "Africa,Southeast Asia,Middle East",
        "company_size": "large", "stage": "established", "annual_revenue_usd_m": 85,
    },
    {
        "name": "Guangzhou VitaWell Nutraceuticals",
        "country": "China", "city": "Guangzhou",
        "sector": "Nutraceuticals",
        "sub_specialty": "Plant-based supplements, immunity boosters",
        "description": "Producer of plant-derived dietary supplements and functional foods focused on immunity and gut health, OEM/ODM capable.",
        "tags": "supplements,plant-based,immunity,OEM,functional-food",
        "certifications": "ISO 22000,HACCP",
        "target_markets": "Middle East,Europe",
        "company_size": "medium", "stage": "growth", "annual_revenue_usd_m": 22,
    },
    {
        "name": "Shenzhen NovaDerm Consumer Health",
        "country": "China", "city": "Shenzhen",
        "sector": "Consumer Health Products",
        "sub_specialty": "Skincare devices, personal hygiene products",
        "description": "Consumer health brand producing at-home dermatological devices and personal hygiene products with e-commerce distribution experience.",
        "tags": "skincare,consumer-devices,hygiene,e-commerce,D2C",
        "certifications": "CE,RoHS",
        "target_markets": "GCC,Europe,North America",
        "company_size": "medium", "stage": "growth", "annual_revenue_usd_m": 15,
    },
    {
        "name": "Suzhou MedSupply Group",
        "country": "China", "city": "Suzhou",
        "sector": "Medical Supplies",
        "sub_specialty": "Disposable PPE, wound care consumables",
        "description": "Large-scale manufacturer of disposable medical consumables including PPE, gloves, and wound care products for hospital procurement.",
        "tags": "PPE,disposables,wound-care,hospital-procurement,bulk-export",
        "certifications": "ISO 13485,FDA 510k,CE",
        "target_markets": "Global,Africa,Middle East",
        "company_size": "large", "stage": "established", "annual_revenue_usd_m": 120,
    },
    {
        "name": "Hangzhou PrecisionOrtho Devices",
        "country": "China", "city": "Hangzhou",
        "sector": "Medical Devices",
        "sub_specialty": "Orthopedic implants, surgical instruments",
        "description": "Designer and manufacturer of orthopedic implants and precision surgical instruments, seeking distribution partners in emerging markets.",
        "tags": "orthopedic,implants,surgical-instruments,precision-manufacturing",
        "certifications": "ISO 13485,CE,NMPA",
        "target_markets": "Middle East,Latin America,Southeast Asia",
        "company_size": "medium", "stage": "growth", "annual_revenue_usd_m": 30,
    },
    {
        "name": "Beijing NeuroLink MedTech",
        "country": "China", "city": "Beijing",
        "sector": "MedTech",
        "sub_specialty": "AI diagnostic imaging, remote patient monitoring",
        "description": "Developer of AI-powered diagnostic imaging software and wearable remote patient monitoring devices for chronic disease management.",
        "tags": "AI-diagnostics,imaging,remote-monitoring,wearables,chronic-disease",
        "certifications": "NMPA,CE,ISO 27001",
        "target_markets": "GCC,Europe,North America",
        "company_size": "startup", "stage": "early", "annual_revenue_usd_m": 4,
    },
    {
        "name": "Nanjing GreenLeaf Pharma",
        "country": "China", "city": "Nanjing",
        "sector": "Pharmaceuticals",
        "sub_specialty": "Traditional Chinese Medicine (TCM) extracts, herbal formulations",
        "description": "Manufacturer of standardized TCM extracts and herbal pharmaceutical formulations with modern extraction and quality-control facilities.",
        "tags": "TCM,herbal,extracts,pharmaceuticals,quality-control",
        "certifications": "GMP,ISO 9001",
        "target_markets": "Southeast Asia,Middle East",
        "company_size": "medium", "stage": "established", "annual_revenue_usd_m": 40,
    },
    {
        "name": "Chengdu SmartCare Devices",
        "country": "China", "city": "Chengdu",
        "sector": "Medical Devices",
        "sub_specialty": "Home healthcare devices, glucose/BP monitors",
        "description": "Manufacturer of connected home healthcare monitoring devices (glucose meters, blood pressure monitors) with companion mobile apps.",
        "tags": "home-healthcare,connected-devices,glucose-monitor,BP-monitor,mobile-app",
        "certifications": "CE,FDA 510k,ISO 13485",
        "target_markets": "GCC,Africa,Europe",
        "company_size": "medium", "stage": "growth", "annual_revenue_usd_m": 18,
    },
]

INVESTORS = [
    {
        "name": "Gulf Horizon Capital Partners",
        "type": "Investor", "country": "UAE",
        "sectors_of_interest": "Medical Devices,MedTech",
        "description": "Growth-stage investment fund focused on connected health devices and AI-enabled diagnostics, ticket size $2M-$10M, active in GCC expansion.",
        "geographic_focus": "GCC,Middle East",
        "stage_focus": "growth,early",
        "ticket_size_usd_m": "2-10",
    },
    {
        "name": "MENA Health Distribution Partners",
        "type": "Strategic Partner / Distributor", "country": "Egypt",
        "sectors_of_interest": "Medical Supplies,Pharmaceuticals",
        "description": "Regional distributor with hospital procurement network across Egypt and North Africa, seeking bulk-supply manufacturing partners for PPE and generics.",
        "geographic_focus": "Africa,Middle East",
        "stage_focus": "established",
        "ticket_size_usd_m": "N/A",
    },
    {
        "name": "VitalWell Ventures",
        "type": "Investor", "country": "Saudi Arabia",
        "sectors_of_interest": "Nutraceuticals,Consumer Health Products",
        "description": "Consumer wellness-focused VC investing in D2C nutraceutical and consumer health brands expanding into the GCC market, ticket size $500K-$3M.",
        "geographic_focus": "GCC",
        "stage_focus": "growth,early",
        "ticket_size_usd_m": "0.5-3",
    },
    {
        "name": "OrthoBridge Distribution",
        "type": "Strategic Partner / Distributor", "country": "UAE",
        "sectors_of_interest": "Medical Devices",
        "description": "Specialized distributor of orthopedic and surgical instruments across the Middle East, looking for precision manufacturing partners.",
        "geographic_focus": "Middle East,Latin America",
        "stage_focus": "growth,established",
        "ticket_size_usd_m": "N/A",
    },
    {
        "name": "DeepHealth AI Fund",
        "type": "Investor", "country": "Singapore",
        "sectors_of_interest": "MedTech",
        "description": "Early-stage fund dedicated to AI-driven diagnostics and remote patient monitoring startups scaling into emerging markets, ticket size $1M-$5M.",
        "geographic_focus": "Global,GCC,Europe",
        "stage_focus": "early,growth",
        "ticket_size_usd_m": "1-5",
    },
    {
        "name": "Levant Pharma Trading",
        "type": "Strategic Partner / Distributor", "country": "Jordan",
        "sectors_of_interest": "Pharmaceuticals",
        "description": "Pharmaceutical trading house with regulatory registration expertise across the Levant, seeking generics and TCM manufacturing partnerships.",
        "geographic_focus": "Middle East",
        "stage_focus": "established",
        "ticket_size_usd_m": "N/A",
    },
]


def get_manufacturers():
    return MANUFACTURERS


def get_investors():
    return INVESTORS

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

# Enhanced hobbies data with detailed information
hobbies_list = [
    {
        "name": "Soccer",
        "class": "soccer",
        "icon": "⚽",
        "image": "static/img/soccer.JPG",
        "description": "Passionate about the beautiful game! I love the teamwork, strategy, and athleticism that soccer demands. Whether it's pickup games or organized leagues, soccer keeps me active and competitive.",
        "details": {
            "experience": "10+ years",
            "favorite_team": "FC Barcelona",
            "position": "Attacker",
        },
    },
    {
        "name": "Skiing",
        "class": "skiing",
        "icon": "🎿",
        "image": "static/img/skiing.jpeg",
        "description": "There's nothing like carving down fresh powder! Skiing combines my love for adventure, nature, and adrenaline. The mountains provide the perfect escape from the digital world.",
        "details": {
            "experience": "10+ years",
            "skill_level": "Advanced",
            "favorite_resort": "Palisades",
        },
    },
    {
        "name": "Fitness",
        "class": "gym",
        "icon": "💪",
        "image": "static/img/gym.jpg",
        "description": "Staying strong and healthy is a priority. The gym helps me maintain physical fitness, mental clarity, and provides a great way to challenge myself and set new personal records.",
        "details": {
            "experience": "4 years",
        },
    },
]


@app.route("/")
def index():
    # Work Experience Data
    work_experiences = [
        {
            "title": "Software Engineer",
            "company": "Garde",
            "location": "Davis, CA",
            "date": "October 2023 – Present",
            "status": "current",
            "description": [
                "Created sports analytics platform that provided AI match analysis & feedback for 30+ users.",
                "Integrated video processing pipeline with FFmpeg transcoding, Cloudflare R2 storage, & HTTPS live streaming, capable of processing 30 minute videos in 2 minutes.",
                "Produced Next.js frontend for video streaming with seamless user experience.",
                "Implemented Next.js full-stack user auth from scratch, using JWT tokens for sessions & Cloudflare D1 for storage.",
            ],
            "tech_stack": ["Next.js", "FFmpeg", "Cloudflare R2", "JWT", "AI Analytics"],
        },
        {
            "title": "Software Engineer",
            "company": "Institute for Complex Adaptive Matter",
            "location": "Davis, CA",
            "date": "January 2024 – Present",
            "status": "current",
            "description": [
                "Architected a searchable materials science paper database with AI vector search, sorting, filters, & pagination.",
                "Created AI-powered data processing pipeline capable of handling 1,000 docs/min, using Python to query papers from ArXiv, MatbertNer to add NLP analysis, & Elasticsearch to store documents.",
                "Modeled Flask backend using AI vector search with sentence transformer embeddings. Capable of searching 50,000+ documents in <3 seconds, improved to <1 second for cached documents in Redis.",
                "Utilized Docker Compose to orchestrate containers, enabling seamless deployment across environments.",
            ],
            "tech_stack": [
                "Python",
                "Flask",
                "Elasticsearch",
                "Redis",
                "Docker",
                "React.js",
                "AI/ML",
            ],
        },
        {
            "title": "R&D Intern",
            "company": "Fiery LLC",
            "location": "Fremont, CA",
            "date": "June 2024 – September 2024",
            "status": "past",
            "description": [
                "Developed ETL pipelines on AWS to ingest, normalize, & visualize data.",
                "Used Terraform to setup S3 Buckets, Quicksight, Glue, Cloudwatch, Lambda Functions, & API Gateways.",
                "Designed API Gateway with Python Lambda functions to upload files & verify their existence on S3.",
                "Built PySpark script in AWS Glue to validate JSON schemas & normalize multi-client data in <1 minute, a 66% runtime improvement.",
                "Utilized Python testing scripts, boasting 100% test coverage on Pyspark scripts & Lambda functions.",
            ],
            "tech_stack": [
                "AWS",
                "Terraform",
                "PySpark",
                "Lambda",
                "S3",
                "API Gateway",
                "Python",
            ],
        },
    ]

    # Education Data
    education_list = [
        {
            "school_name": "University of California, Davis",
            "degree": "Bachelor's of Science in Computer Science",
            "location": "Davis, CA",
            "date": "September 2022 – June 2026",
            "status": "current",
            "icon": "🎓",
            "gpa": {"overall": "3.50", "engineering": "3.63"},
            "coursework": [
                {"name": "Machine Learning", "category": "ai-ml"},
                {"name": "Artificial Intelligence", "category": "ai-ml"},
                {"name": "Deep Learning", "category": "ai-ml"},
                {"name": "Algorithm Design & Analysis", "category": "theory"},
                {"name": "Data Structures & Algorithms", "category": "theory"},
                {"name": "Software Dev & OOP", "category": "software"},
                {"name": "Operating Systems", "category": "systems"},
                {"name": "Programming Languages", "category": "theory"},
                {"name": "Distributed Ledgers", "category": "systems"},
                {"name": "Computer Architecture", "category": "systems"},
            ],
            "achievements": [
                {"icon": "🧠", "text": "AI/ML Specialization"},
                {"icon": "💻", "text": "Software Engineering Focus"},
                {"icon": "🔬", "text": "Research Experience"},
            ],
        },
        {
            "school_name": "Homestead High School",
            "degree": "High School Diploma",
            "location": "Cupertino, CA",
            "date": "2022",
            "status": "past",
            "icon": "🏫",
            "achievements": [
                {"icon": "🏆", "text": "Valedictorian"},
                {"icon": "📐", "text": "Math Team Captain"},
            ],
        },
    ]

    # Travel Data
    travel_places = [
        {"name": "Melbourne, Australia", "coords": [-37.8136, 144.9631]},
        {"name": "Hyderabad, India", "coords": [17.3850, 78.4867]},
        {"name": "Rome, Italy", "coords": [41.9028, 12.4964]},
        {"name": "Paris, France", "coords": [48.8566, 2.3522]},
        {"name": "Sunnyvale, CA, USA", "coords": [37.3688, -122.0363]},
        {"name": "Mexico City, Mexico", "coords": [19.4326, -99.1332]},
    ]

    travel_stats = {"countries": 6, "continents": 4, "memories": "∞"}

    return render_template(
        "index.html",
        work_experiences=work_experiences,
        education_list=education_list,
        hobbies_list=hobbies_list,
        travel_places=travel_places,
        travel_stats=travel_stats,
    )


@app.route("/hobbies")
def hobbies():
    """Dedicated hobbies page with detailed information"""
    return render_template("hobbies.html", hobbies_list=hobbies_list)


@app.route("/hobbies/<hobby_name>")
def hobby_detail(hobby_name):
    """Individual hobby detail page"""
    # Find the specific hobby
    hobby = next(
        (h for h in hobbies_list if h["name"].lower() == hobby_name.lower()), None
    )
    if not hobby:
        return "Hobby not found", 404

    return render_template("hobby_detail.html", hobby=hobby)


if __name__ == "__main__":
    app.run(debug=True)

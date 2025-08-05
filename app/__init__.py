import datetime
import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from peewee import (CharField, DateTimeField, Model, MySQLDatabase,
                    SqliteDatabase)
from playhouse.shortcuts import model_to_dict

load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


def init_db():
    mydb.connect()
    mydb.create_tables([TimelinePost])

def connect_with_retry(max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            init_db()
            print(f"Database initialized successfully on attempt {attempt + 1}")
            return
        except Exception as e:
            print(f"Database init attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise e

connect_with_retry()

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
            "position": "Winger",
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
            "skill_level": "◆◆",
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
            "favorite_lift": "Bench Press",
        },
    },
]

# Work Experience Data
work_experiences = [
    {
        "title": "Software Engineer Intern",
        "company": "ScoreData Corporation",
        "location": "Remote",
        "date": "June 2025 – Present",
        "status": "current",
        "description": [
            # Add your description here when available
        ],
        "tech_stack": ["Flask", "LLMs", "Deep Learning"],
        "impact": "TBD",
        "highlight": "Machine Learning platform",
    },
    {
        "title": "Production Engineer",
        "company": "Meta & Major League Hacking",
        "location": "Remote",
        "date": "June 2025 – Present",
        "status": "current",
        "description": [
            # Add your description here when available
        ],
        "tech_stack": ["Docker", "Nginx", "AWS", "Flask", "HTML", "CSS"],
        "impact": "TBD",
        "highlight": "Production systems optimization",
    },
    {
        "title": "ML Intern",
        "company": "HealtheTile",
        "location": "Davis, CA",
        "date": "April 2025 – Present",
        "status": "current",
        "description": [
            "Implemented AutoML pipelines using Google Vertex and Datarobot.",
            "Built React Native app for health monitoring app",
            "Created development dashboards using React.js for lab members.",
        ],
        "tech_stack": ["Machine Learning", "Python", "React Native", "React", "Flask"],
        "impact": "TBD",
        "highlight": "Healthcare ML solutions",
    },
    {
        "title": "Co-Founder",
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
        "impact": "30+ active users",
        "highlight": "AI-powered sports analytics",
    },
    {
        "title": "Software Engineer",
        "company": "Institute for Complex Adaptive Matter (ICAM-I2CAM)",
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
        "impact": "50,000+ documents searchable",
        "highlight": "AI vector search engine",
    },
    {
        "title": "R&D Intern",
        "company": "Fiery",
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
        "impact": "66% runtime improvement",
        "highlight": "AWS cloud infrastructure",
    },
    {
        "title": "IT Infrastructure Assistant",
        "company": "UC Davis School of Veterinary Medicine",
        "location": "Davis, CA",
        "date": "October 2023 – June 2024",
        "status": "past",
        "description": [
            "Setup HPC Cluster with Slurm for PhD candidates to analyze DNA sequencing data.",
            "Implemented SSH access to cluster so users can access data & submit jobs from anywhere.",
            "Developed Python script to query user data from LDAP database & create posix users locally.",
            "Created shared directories with NFS4 to provide HPC cluster with centralized storage.",
            "Organized data across HDDs using Rsync, Python scripts, & Bash scripts.",
        ],
        "tech_stack": [
            "HPC",
            "Slurm",
            "SSH",
            "Python",
            "LDAP",
            "NFS4",
            "Rsync",
            "Bash",
        ],
        "impact": "Improved lab operations",
        "highlight": "Microlab infrastructure support",
    },
    {
        "title": "Frontend Developer",
        "company": "University of California, Davis",
        "location": "Davis, CA",
        "date": "February 2024 – May 2024",
        "status": "past",
        "description": ["Built webpages for the UC Davis Physics Page"],
        "tech_stack": ["Frontend Development", "HTML/CSS", "Concrete5"],
        "impact": "Created and improved current UC Davis Physics page interface",
        "highlight": "Improved information on program donations",
    },
    {
        "title": "Recreation Assistant",
        "company": "City of Sunnyvale",
        "location": "Sunnyvale, CA",
        "date": "April 2022 – April 2024",
        "status": "past",
        "description": ["Collaborated with local members of community and coworkers"],
        "impact": "Community engagement",
        "highlight": "Community involvement",
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
            {"icon": "💻", "text": "Software Engineering Focus"},
            {"icon": "🔬", "text": "Research Experience"},
        ],
        "description": "Pursuing a comprehensive computer science education with focus on software engineering. Actively engaged in research and practical application of cutting-edge technologies.",
    },
    {
        "school_name": "Homestead High School",
        "degree": "High School Diploma",
        "location": "Cupertino, CA",
        "date": "2022",
        "status": "past",
        "icon": "🏫",
        "description": "Graduated with a strong foundation in mathematics and science. Maintained academic excellence throughout high school.",
    },
]

# Travel Data
travel_places = [
    {
        "name": "Melbourne, Australia",
        "coords": [-37.8136, 144.9631],
        "country": "Australia",
        "continent": "Oceania",
        "description": "Explored the cultural capital of Australia",
        "highlights": [],
    },
    {
        "name": "Hyderabad, India",
        "coords": [17.3850, 78.4867],
        "country": "India",
        "continent": "Asia",
        "description": "Visited family and experienced rich Indian culture",
        "highlights": ["Extended Family"],
    },
    {
        "name": "Rome, Italy",
        "coords": [41.9028, 12.4964],
        "country": "Italy",
        "continent": "Europe",
        "description": "Immersed in ancient history and Italian cuisine",
        "highlights": ["Colosseum", "Vatican City", "Food Food 🫶"],
    },
    {
        "name": "Paris, France",
        "coords": [48.8566, 2.3522],
        "country": "France",
        "continent": "Europe",
        "description": "City of lights and romantic architecture",
        "highlights": ["Eiffel Tower", "Louvre Museum"],
    },
    {
        "name": "Sunnyvale, CA, USA",
        "coords": [37.3688, -122.0363],
        "country": "USA",
        "continent": "North America",
        "description": "My hometown in the heart of Silicon Valley",
        "highlights": ["Tech Hub", "Family Home", "Where it all began"],
    },
    {
        "name": "Mexico City, Mexico",
        "coords": [19.4326, -99.1332],
        "country": "Mexico",
        "continent": "North America",
        "description": "Vibrant culture and amazing street food",
        "highlights": [],
    },
]

travel_stats = {
    "countries": len(set(place["country"] for place in travel_places)),
    "continents": len(set(place["continent"] for place in travel_places)),
    "memories": "∞",
    "years_traveling": 5,
}


@app.route("/")
def index():
    """Main portfolio page with overview of all sections"""
    return render_template("index.html")


@app.route("/hobbies")
def hobbies():
    """Dedicated hobbies and interests page"""
    return render_template("hobbies.html", hobbies_list=hobbies_list)


@app.route("/experience")
def experience():
    """Dedicated work experience page"""
    return render_template("experience.html", work_experiences=work_experiences)


@app.route("/education")
def education():
    """Dedicated education page"""
    return render_template("education.html", education_list=education_list)


@app.route("/travel")
def travel():
    """Dedicated travel and places visited page"""
    return render_template(
        "travel.html", travel_places=travel_places, travel_stats=travel_stats
    )


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")


@app.route("/hobbies/<hobby_name>")
def hobby_detail(hobby_name):
    """Individual hobby detail page"""
    hobby = next(
        (h for h in hobbies_list if h["name"].lower() == hobby_name.lower()), None
    )
    if not hobby:
        return "Hobby not found", 404
    return render_template("hobby_detail.html", hobby=hobby)


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")

    if not all([name, email, content]):
        return jsonify({"error": "missing name, email, or content"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email"}), 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return (
        jsonify(
            {
                "timeline_posts": [
                    model_to_dict(p)
                    for p in TimelinePost.select().order_by(
                        TimelinePost.created_at.desc()
                    )
                ]
            }
        ),
        200,
    )


@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_timeline_post_by_id(post_id):
    try:
        deleted_count = TimelinePost.delete_by_id(post_id)

        if deleted_count:
            return (
                jsonify({"message": f"Timeline post {post_id} deleted successfully"}),
                200,
            )
        else:
            return jsonify({"error": "Timeline post not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to delete timeline post: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
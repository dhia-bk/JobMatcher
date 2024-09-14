from profile import ProfileInfo, Experience, Education, Project, Organization
from resume_builder import  ResumeBuilder
import pdfkit

profile_data = ProfileInfo(
    name="Dhia Braiek",
    title="Data Analyst",
    email="dhia.braiek@proton.me",
    phone="+216 90731814",
    linkedin="https://linkedin.com/in/mohamed-dhia-braiek",
    github="https://github.com/dhia-bk",
    profile_summary="Passionate Data Analyst with experience in machine learning, data visualization, and ETL pipelines. Enthusiastic about Web3 and decentralized technologies.",
    experiences=[
        Experience(
            title="Data Analyst",
            company="Sopra HR Software",
            date_range="June 2024 - August 2024",
            description=[
                "Developed a robust ETL pipeline in Python to retrieve, preprocess, and clean data from an Oracle database.",
                "Trained a machine learning model to predict employee churn, achieving 93% accuracy, and deployed it in a web application with a visualization dashboard.",
                "Collaborated closely with international clients to deliver key statistics and insights, driving better decision making."
            ]
        )
    ],
    education=[
        Education(
            degree="Bachelor of Science in Business Administration",
            school="Tunis Business School",
            graduation_year="2024",
            details="Focus on Business Analytics and International Business Economics."
        )
    ],
    skills=["Python", "SQL", "Power BI"],
    certifications=["Google Data Analytics Specialization"],
    projects=[
        Project(
            title="Job Hunter AI Application",
            description="AI application to scrape and recommend jobs using a RAG model."
        )
    ],
    languages=["Arabic", "English", "French"],
    organizations=[
        Organization(name="Google Developer Student Club - TBS", role="Member")
    ]
)

resume_builder = ResumeBuilder(profile_data)
html_content = resume_builder.generate_html()
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
pdfkit.from_string(html_content, 'resume.pdf', configuration=config)
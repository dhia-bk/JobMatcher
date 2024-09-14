# AI-Job-Hunter

AI-Job-Hunter is an automated job-hunting application that scrapes job listings from multiple platforms (LinkedIn, Glassdoor, Indeed), processes and cleans the data, and stores it in a PostgreSQL database. The system utilizes an NLP-based recommendation engine, which combines vector embeddings, BM25 search, and reciprocal rank fusion to provide personalized job recommendations based on user profiles.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [Technologies Used](#technologies-used)

## Features
- **Daily Job Scraping**: Automatically scrapes job listings from LinkedIn, Glassdoor, and Indeed.
- **Data Cleaning & Processing**: Cleans and processes the scraped data, removing unnecessary elements like emojis and formatting irregularities.
- **Database Management**: Stores processed job listings in PostgreSQL for structured analysis and retrieval.
- **Job Recommendation System**: Utilizes an NLP-based recommendation system combining vector embeddings, BM25 search, and reciprocal rank fusion to deliver personalized job suggestions.
- **Dashboard Integration**: Supports creating a job tracking dashboard for visualization and monitoring job applications.

## Project Structure

```bash
AI-Job-Hunter/
├── Final - Resume.pdf                 # PDF file (optional, used for demo)
├── data/                              # Folder for storing scraped JSON data
│   └── 2024-09-09.json                # Example of scraped job data
├── main.py                            # Main script to run the job scraping and recommendation system
├── requirements.txt                   # Python dependencies
└── src/                               # Source code folder
    ├── Job_Matcher.py                 # Job recommendation and matching logic
    ├── data_manager/                  # Data handling scripts
    │   ├── DataProcessor.py           # Data cleaning and preprocessing
    │   ├── MongoManager.py            # MongoDB interaction for intermediate storage
    │   ├── PostgresManager.py         # PostgreSQL interaction for storing structured job data
    │   └── utils.py                   # Utility functions for data processing
    └── job_scraper/                   # Job scraper scripts
        ├── GlassDoor_Scraper.py       # Glassdoor scraping logic
        ├── Indeed_Scraper.py          # Indeed scraping logic
        ├── Scrape.py                  # Orchestrates the scraping process
        ├── config.py                  # Configuration settings
        ├── linkedin_scraper.py        # LinkedIn scraping logic
        └── utils.py                   # Helper functions for the scraping process

```
Installation
Prerequisites
Python 3.11+
PostgreSQL
MongoDB (optional for intermediate storage)


```markdown
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

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL
- MongoDB (optional for intermediate storage)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/AI-Job-Hunter.git
   cd AI-Job-Hunter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL:
   - Create a database and tables for storing scraped jobs, recommended jobs, and applied jobs.

4. (Optional) Configure MongoDB if you plan to use it for storing raw job data before cleaning.

## Usage

1. **Scrape Jobs**: 
   Run the main script to scrape job listings from LinkedIn, Glassdoor, and Indeed:
   ```bash
   python main.py
   ```

2. **Process Data**: 
   The data cleaning and processing will automatically run after scraping. The cleaned data will be stored in the PostgreSQL database.

3. **Job Recommendation**:
   The job recommendation system combines vector embeddings, BM25 search, and reciprocal rank fusion to deliver personalized job suggestions based on user profiles.

## Data Flow

1. **Scraping**: Jobs are scraped from multiple sources using the scrapers in the `job_scraper/` folder.
2. **Cleaning & Processing**: The `DataProcessor.py` script cleans and preprocesses the scraped data, removing unwanted characters and standardizing the format.
3. **Database**: Cleaned data is stored in the PostgreSQL database. You can interact with the data using the `PostgresManager.py`.
4. **Recommendation**: The `Job_Matcher.py` script provides AI-driven job recommendations based on user input, leveraging vector embeddings, BM25, and reciprocal rank fusion to ensure personalized results.

## Technologies Used
- **Python**: Core programming language.
- **Selenium**: For web scraping.
- **PostgreSQL**: For storing cleaned job data in a structured format.
- **MongoDB**: (Optional) Intermediate storage of raw scraped data.
- **NLP-Based Recommendation**: Uses vector embeddings, BM25 search, and reciprocal rank fusion to deliver personalized job recommendations.
- **Kafka** (Optional): For real-time data streaming.
- **Power BI**: For dashboard visualization of job data.
```


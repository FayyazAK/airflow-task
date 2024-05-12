# Data Extraction, Transformation and Storage Pipeline
## Overview
This document describes the implementation of an Apache Airflow Directed Acyclic Graph (DAG) named data_extraction_pipeline. This DAG is designed to automate the process of extracting data of articles from the landing pages of news websites www.bbc.com and www.dawn.com, transforming the data, and storing it in a structured format. The main goal is to streamline the data handling process for websites using DVC and Airflow.

## Tasks
The DAG comprises three main tasks:

Extract Data
Transform Data
Store Data

### 1. Extract Data
This task is responsible for downloading the content from specified URLs (https://www.dawn.com and https://www.bbc.com). It utilizes the Python requests library to make HTTP requests and BeautifulSoup from bs4 for parsing HTML content. The data extracted includes the titles, descriptions, and links from articles.

### 2. Transform Data
The extracted data is transformed in this task. The transformation involves text preprocessing, including converting text to lowercase and tokenizing while removing stopwords. This process is meant to standardize the data and prepare it for analysis or storage.

### 3. Store Data
After transformation, this task stores the data in a CSV file named articles-data.csv. The file will contain columns for titles, descriptions, and links, making the data easier to access and analyze in the future.

### Python Functions
preprocess_text(text): This function preprocesses the text by lowering the case, tokenizing, and removing non-alphabetic characters and stopwords, enhancing the quality of text data for future processing.
Execution Flow
The DAG's execution flow is linear:

extract_data → transform_data → store_data
extract_data gathers data from the web.
transform_data processes this data.
store_data saves the processed data to a CSV file.
Task Dependencies
Task dependencies are set up to ensure that:

Data extraction must complete before the transformation begins.
Data transformation must complete before storing the data.
This sequence ensures data integrity and the successful execution of dependent tasks.

## Challenges Encountered
#### Web Scraping Limitations: 
Adaptations required due to changes in source website structures. So, I had to inspect the website and find the element structure for effeciently scrape the title and description of news articles.
#### DVC Integration: 
Challenges in automating DVC operations within Airflow tasks.
#### Dependency Management: 
Ensuring that all dependencies were correctly managed in the Airflow environment.
#### Installation of Apache Airflow:
It was very hard to install and setup the Apache Airflow on Windows using WSL.

## Conclusion
This Airflow DAG is designed to automate crucial data handling tasks, reducing manual effort and minimizing errors. By extracting, transforming, and storing web data daily, this pipeline ensures up-to-date data availability for analysis, reporting, or any other downstream use cases.

# Data Extraction Pipeline
## Overview
This document describes the implementation of an Apache Airflow Directed Acyclic Graph (DAG) named data_extraction_pipeline. This DAG is designed to automate the process of extracting data from websites, transforming the data, and storing it in a structured format. The main goal is to streamline the data handling process for websites such as dawn.com and bbc.com.

## DAG Configuration
Default Arguments
The DAG is configured with the following default parameters:

Owner: 'airflow' — Identifies the owner of the DAG, useful in a multi-user setup.
Depends on Past: False — Indicates that the DAG's runs do not depend on the success of previous runs.
Start Date: May 10, 2024 — The date from which the DAG is considered to have started.
Email on Failure: False — If set to true, Airflow will send an email to the owner if the DAG fails.
Email on Retry: False — If set to true, Airflow will send an email to the owner if a task in the DAG retries.
Retries: 1 — Number of retries that should be attempted on failure.
Retry Delay: 5 minutes — The delay between retry attempts.
Schedule
The DAG is scheduled to run once every day (@daily), which is controlled by the schedule_interval argument.

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

## Conclusion
This Airflow DAG is designed to automate crucial data handling tasks, reducing manual effort and minimizing errors. By extracting, transforming, and storing web data daily, this pipeline ensures up-to-date data availability for analysis, reporting, or any other downstream use cases.

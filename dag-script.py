from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 12),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def dvc_add_commit_push():
    """Function to add, commit, and push changes to DVC."""
    import os
    os.system('dvc add articles-data.csv')
    os.system('dvc commit articles-data.csv')
    os.system('dvc push')
    os.system('git add .')
    os.system('git commit -m "new-updated data"')
    os.system('git push')


def extract_data():
    nltk.download('punkt')
    nltk.download('stopwords')
    
    urls = ['https://www.dawn.com', 'https://www.bbc.com']
    extracted_data = []
    
    for url in urls:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        if "dawn.com" in url:
            articles = soup.find_all('article', {'class': 'story'})
            for article in articles:
                title = article.find('a', {'class': 'story__link'}).get_text(strip=True) if article.find('a', {'class': 'story__link'}) else 'No title'
                description = article.find('div', {'class': 'story__excerpt'}).get_text(strip=True) if article.find('div', {'class': 'story__excerpt'}) else ''
                link = article.find('a', {'class': 'story__link'})['href'] if article.find('a', {'class': 'story__link'}) else 'No link'
                extracted_data.append({'title': title, 'description': description, 'link': link})
        elif "bbc.com" in url:
            articles = soup.find_all('div', {'data-testid': 'edinburgh-card'})
            for article in articles:
                title = article.find('h2', {'data-testid': 'card-headline'}).get_text(strip=True) if article.find('h2', {'data-testid': 'card-headline'}) else 'No title'
                description = article.find('p', {'data-testid': 'card-description'}).get_text(strip=True) if article.find('p', {'data-testid': 'card-description'}) else ''
                link = 'https://www.bbc.com' + article.find('a', {'data-testid': 'internal-link'})['href'] if article.find('a', {'data-testid': 'internal-link'}) else 'No link'
                extracted_data.append({'title': title, 'description': description, 'link': link})
    
    return extracted_data

def transform_data(ti):
    extracted_data = ti.xcom_pull(task_ids='extract_data')
    transformed_data = []
    
    for item in extracted_data:
        title = preprocess_text(item['title'])
        description = preprocess_text(item['description'])
        link = item['link']
        transformed_data.append({'title': title, 'description': description, 'link': link})
        
    return transformed_data

def store_data(ti):
    transformed_data = ti.xcom_pull(task_ids='transform_data')
    df = pd.DataFrame(transformed_data)
    df.to_csv('articles-data.csv', index=False)

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    return ' '.join(tokens)

with DAG(
    'data_extraction_pipeline_with_dvc',
    default_args=default_args,
    description='A DAG to extract, transform, store data from websites and manage data versioning with DVC',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    t2 = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    t3 = PythonOperator(
        task_id='store_data',
        python_callable=store_data,
    )

    t4 = PythonOperator(
        task_id='dvc_add_commit_push',
        python_callable=dvc_add_commit_push,
    )

    t1 >> t2 >> t3 >> t4

import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def extract_data(url):
    """
    Extracts titles, descriptions, and links from given URL, adjusting for different website structures.
    Args:
        url (str): URL of the website to scrape.

    Returns:
        list of dict: List containing dictionaries with 'title', 'description', and 'link'.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    if "dawn.com" in url:
        articles = soup.find_all('article', {'class': 'story'})
        for article in articles:
            title = article.find('a', {'class': 'story__link'}).get_text(strip=True) if article.find('a', {'class': 'story__link'}) else 'No title'
            description = article.find('div', {'class': 'story__excerpt'}).get_text(strip=True) if article.find('div', {'class': 'story__excerpt'}) else ''
            link = article.find('a', {'class': 'story__link'})['href'] if article.find('a', {'class': 'story__link'}) else 'No link'
            data.append({'title': title, 'description': description, 'link': link})
    elif "bbc.com" in url:
        articles = soup.find_all('div', {'data-testid': 'edinburgh-card'})
        for article in articles:
            title = article.find('h2', {'data-testid': 'card-headline'}).get_text(strip=True) if article.find('h2', {'data-testid': 'card-headline'}) else 'No title'
            description = article.find('p', {'data-testid': 'card-description'}).get_text(strip=True) if article.find('p', {'data-testid': 'card-description'}) else ''
            link = 'https://www.bbc.com' + article.find('a', {'data-testid': 'internal-link'})['href'] if article.find('a', {'data-testid': 'internal-link'}) else 'No link'
            data.append({'title': title, 'description': description, 'link': link})

    return data

def preprocess_text(text):
    """
    Cleans and preprocesses the input text.
    Args:
        text (str): Input text.

    Returns:
        str: Preprocessed text.
    """
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize text
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]  # Remove punctuation and stopwords
    return ' '.join(tokens)

def extract_transform_save(urls, file_name):
    """
    Extracts, transforms, and saves data from multiple URLs.
    Args:
        urls (list): List of URLs to extract data from.
        file_name (str): Name of the file to save the data.

    Returns:
        pandas.DataFrame: DataFrame containing combined data from all URLs.
    """
    combined_data = []
    for url in urls:
        data = extract_data(url)
        for item in data:
            item['title'] = preprocess_text(item['title'])
            item['description'] = preprocess_text(item['description'])
        combined_data.extend(data)
    df = pd.DataFrame(combined_data)
    df.to_csv(file_name, index=False)
    return df

# Store the data
urls = ['https://www.dawn.com', 'https://www.bbc.com']
data = extract_transform_save(urls, 'articles-data.csv')


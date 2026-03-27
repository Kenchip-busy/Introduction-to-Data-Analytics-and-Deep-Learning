# Lab 7: Natural Language Processing with NLTK 
*(Phân tích dữ liệu dạng văn bản với NLTK)*

## Description (Mô tả dự án)

 bài thực hành Lab 7 về Xử lý ngôn ngữ tự nhiên (NLP). Bài lab tập trung vào việc áp dụng thư viện NLTK để rút trích, tiền xử lý và phân tích ngữ nghĩa, cảm xúc từ các tập dữ liệu văn bản thô.

##  Key Features (Các nội dung chính)
The implementation covers the following NLP tasks:
1. **Corpora Management:** Downloading and exploring textual corpora (e.g., Gutenberg, Names).
2. **Text Concordance & Context:** Searching for specific words and their surrounding contexts.
3. **Frequency Distribution (`FreqDist`):** Analyzing word counts and identifying common terminologies.
4. **Data Preprocessing:** Filtering out stopwords and punctuations to clean datasets.
5. **N-grams Analysis:** Extracting Bigrams and Trigrams to identify collocations.
6. **Web Scraping:** Fetching and parsing raw text and HTML from the internet using `urllib` and `BeautifulSoup`.
7. **Lexical Database (`WordNet`):** Fetching definitions, synonyms, antonyms, and calculating semantic similarities (Wu-Palmer similarity).
8. **Sentiment Analysis:** Building a **Naïve Bayes Classifier** to predict whether movie reviews are positive or negative based on extracted features.

##  Technologies Used (Công nghệ sử dụng)
*   **Language:** Python 3.x
*   **Libraries:** 
    *   `nltk` (Natural Language Toolkit)
    *   `bs4` (BeautifulSoup4 - for HTML parsing)
    *   `urllib` (for fetching web data)
    *   `random`, `os`, `string` (Python standard libraries)

##  Installation & Setup (Hướng dẫn cài đặt)

**1. Install dependencies (Cài đặt thư viện):**
Open your terminal/command prompt and run:
```bash
pip install nltk beautifulsoup4 lxml

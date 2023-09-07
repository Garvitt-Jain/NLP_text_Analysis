
# Commented out IPython magic to ensure Python compatibility.
# Import the drive module from the google.colab library
from google.colab import drive

# Mount your Google Drive to a specified directory in Colab
# This will prompt you to authenticate and grant access to your Google Drive
drive.mount('/gdrive')

# Change the current working directory in Colab to a specific location within your Google Drive
# Replace '/gdrive/MyDrive/test' with the desired path in your Google Drive
# %cd '/gdrive/MyDrive/ test'

ls # Checking we are in the coreect directory and all the required files are present

# Import necessary libraries for web scraping, data processing, and natural language processing
import requests  # For making HTTP requests to websites
from bs4 import BeautifulSoup  # For parsing HTML content
import pandas as pd  # For working with data in tabular format
import os  # For file and directory operations
import nltk  # Natural Language Toolkit for text processing
from nltk.tokenize import word_tokenize  # Tokenization for splitting text into words
from nltk.corpus import stopwords  # Stopwords for text preprocessing
import re  # Regular expressions for text processing

# Download NLTK data required for tokenization and stopwords
nltk.download('punkt')  # Download NLTK's tokenization data
nltk.download('stopwords')  # Download NLTK's stopwords data

# Load the DataFrame from the Excel file named 'Input.xlsx'
df = pd.read_excel('Input.xlsx')

# Iterate through rows in the DataFrame
for index, row in df.iterrows():
    # Extract URL and URL_ID from the current row
    url = row['URL']
    url_id = row['URL_ID']

    # Define user-agent header for the HTTP request
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    try:
        # Send an HTTP GET request to the URL with the defined headers
        response = requests.get(url, headers=headers)
        # Check if the response status code indicates success (200 OK)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"Can't get response of {url_id}: {e}")
        continue

    article_text = ""  # Initialize an empty string to store article text

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Define CSS selectors to identify and remove header and footer elements
    header_selector = '.td-header-template-wrap'
    footer_selector = '.td-footer-template-wrap'

    for selector in [header_selector, footer_selector]:
        # Select and remove header/footer elements from the HTML content
        header_footer_elements = soup.select(selector)
        for element in header_footer_elements:
            element.extract()

    # Find and extract the title of the page
    try:
        title = soup.find('h1').get_text()
    except AttributeError:
        # Handle the case where the title is not found
        print(f"Can't get title of {url_id}")
        continue

    try:
        # Extract article text by concatenating text from all 'p' elements
        for p in soup.find_all('p'):
            article_text += p.get_text()
    except:
        # Handle the case where the main article content is not found
        print("Main article content not found.")

    # Define the file name to save the extracted title and article text
    file_name = '/gdrive/MyDrive/ test/article_text/' + str(url_id) + '.txt'

    # Write the title and article text to the specified file
    with open(file_name, 'w') as file:
        file.write(title + '\n' + article_text)

# Define the directory paths for various data and resources within your Google Drive

# Directory path where the extracted article text will be saved
text_dir = "/gdrive/MyDrive/ test/article_text"

# Directory path where the stopwords data is stored
stopwords_dir = "/gdrive/MyDrive/ test/StopWords"

# Directory path where the sentiment analysis-related data (e.g., MasterDictionary) is stored
sentiment_dir = "/gdrive/MyDrive/ test/MasterDictionary"

# Initialize an empty set to store stop words
stop_words = set()

# Iterate through files in the 'stopwords_dir' directory
for filename in os.listdir(stopwords_dir):
    # Open and read each file within the 'stopwords_dir' directory
    with open(os.path.join(stopwords_dir, filename), 'r', encoding='ISO-8859-1') as f:
        # Read the file contents, split lines, and convert them to a set
        file_stopwords = set(f.read().splitlines())

        # Update the 'stop_words' set with the stop words from the current file
        stop_words.update(file_stopwords)

# Initialize an empty list to store tokenized documents
docs = []

# Iterate through text files in the 'text_dir' directory
for text_file in os.listdir(text_dir):
    # Open and read each text file within the 'text_dir' directory
    with open(os.path.join(text_dir, text_file), 'r') as f:
        text = f.read()

        # Tokenize the text content of the current file
        words = word_tokenize(text)

        # Remove stop words from the tokens and create a filtered list
        filtered_text = [word for word in words if word.lower() not in stop_words]

        # Add the filtered tokens of the current file to the 'docs' list
        docs.append(filtered_text)

# Initialize empty sets to store positive and negative sentiment words
pos = set()
neg = set()

# Iterate through files in the 'sentiment_dir' directory
for filename in os.listdir(sentiment_dir):
    # Check if the current file is 'positive-words.txt'
    if filename == 'positive-words.txt':
        # Open and read the 'positive-words.txt' file
        with open(os.path.join(sentiment_dir, filename), 'r', encoding='ISO-8859-1') as f:
            # Update the 'pos' set with positive sentiment words from the file
            pos.update(f.read().splitlines())
    else:
        # For other files (negative sentiment words), open and read the file
        with open(os.path.join(sentiment_dir, filename), 'r', encoding='ISO-8859-1') as f:
            # Update the 'neg' set with negative sentiment words from the file
            neg.update(f.read().splitlines())

# Sentiment Analysis
# Initialize empty lists to store sentiment-related data
positive_words = []  # List of positive sentiment words
Negative_words = []  # List of negative sentiment words
positive_score = []  # List of positive sentiment scores
negative_score = []  # List of negative sentiment scores
polarity_score = []  # List of polarity scores
subjectivity_score = []  # List of subjectivity scores
# Iterate through the list of tokenized documents 'docs'
for i in range(len(docs)):
    # Find words in the current document that are in the 'pos' (positive) and 'neg' (negative) sets
    positive_words.append([word for word in docs[i] if word.lower() in pos])
    Negative_words.append([word for word in docs[i] if word.lower() in neg])

    # Calculate the count of positive and negative words in the current document
    positive_score.append(len(positive_words[i]))
    negative_score.append(len(Negative_words[i]))

    # Calculate the polarity score using a formula that considers both positive and negative counts
    polarity_score.append((positive_score[i] - negative_score[i]) / ((positive_score[i] + negative_score[i]) + 0.000001))

    # Calculate the subjectivity score using a formula that considers the total word count
    subjectivity_score.append((positive_score[i] + negative_score[i]) / ((len(docs[i])) + 0.000001))

# Anlysis of redability
# Function to remove punctuation from text
def remove_punctuation(text):
  return re.sub(r'[^\w\s.]', '', text)

# Function to remove stopwords from text
def remove_stopwords(text):
  words = [word for word in text.split() if word.lower() not in stop_words]
  return words


# Define a function named 'measure' that takes a 'file' as an argument
def measure(file):
    # Open and read the contents of the given file
    with open(os.path.join(text_dir, file), 'r') as f:
        text = f.read()

    # Remove punctuations from the text using a regular expression
    text = remove_punctuation(text)

    # Split the text into sentences based on periods (full stops)
    sentences = text.split('.')

    # Calculate the total number of sentences in the file
    num_sentences = len(sentences)

  # We will not remove the stopwords becaus we are doing redability analysis so we will process the text as it si.

    words = [word for word in text.split()]
    # Calculate the total number of words in the file
    num_words = len(words)

    # Initialize a list to store complex words (words with more than 2 syllables)
    complex_words = []
    # Initialize variables for syllable count and a list to store words with syllables
    syllable_count = 0
    syllable_words = []
    # Iterate through the words to identify and count complex words and syllable count and syllable words
    for word in words:
      # Handle exceptions like words ending with "es" or "ed" by removing those suffixes
        if word.endswith('es'):
            word = word[:-2]
        elif word.endswith('ed'):
            word = word[:-2]
        vowels = 'aeiou'
        # Calculate the syllable count for the current word
        syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
        # Check if the word has more than 2 syllables and add it to the complex_words list
        if syllable_count_word > 2:
            complex_words.append(word)
        # Check if the word has at least 1 syllable and add it to the syllable_words list
        if syllable_count_word >= 1:
            syllable_words.append(word)
            syllable_count += syllable_count_word

    # Calculate average sentence length (words per sentence)
    avg_sentence_len = num_words / num_sentences

    # Calculate the percentage of complex words in the text
    Percent_Complex_words = (len(complex_words) / num_words)

    # Calculate the Fog Index using the formula
    Fog_Index = 0.4 * (avg_sentence_len + Percent_Complex_words)

    # Calculate the average syllable count per word
    avg_syllable_word_count = syllable_count / len(syllable_words)

    # Return the calculated values as a tuple
    return avg_sentence_len, Percent_Complex_words*100, Fog_Index, len(complex_words), avg_syllable_word_count

# Initialize empty lists to store calculated metrics
avg_sentence_length = []          # Average sentence length
Percentage_of_Complex_words = []  # Percentage of complex words
Fog_Index = []                    # Fog Index
complex_word_count = []           # Count of complex words
avg_syllable_word_count = []      # Average syllables per word


# Iterate over each file in the 'text_dir' directory
for file in os.listdir(text_dir):
    # Call the 'measure' function to calculate various text metrics
    x, y, z, a, b = measure(file)

    # Append the calculated metrics to their respective lists
    avg_sentence_length.append(x)
    Percentage_of_Complex_words.append(y)
    Fog_Index.append(z)
    complex_word_count.append(a)
    avg_syllable_word_count.append(b)

# Define a function to calculate word count and average word length for a given text file which only contain cleaned words
def cleaned_words(file):
    # Open the text file located in the 'text_dir' directory
    with open(os.path.join(text_dir, file), 'r') as f:
        # Read the contents of the file into a variable 'text'
        text = f.read()

        # Remove non-alphanumeric characters from the text
        text = remove_punctuation(text)

        # Tokenize the cleaned text into words and filter out stopwords
        words = remove_stopwords(text)

        # Calculate the total word count
        word_count = len(words)

        # Calculate the total length of all words
        total_word_length = sum(len(word) for word in words)

        # Calculate the average word length
        average_word_length = total_word_length / word_count

    # Return the word count and average word length as a tuple
    return word_count, average_word_length

# Initialize empty lists to store word counts and average word lengths for each file
word_count = []
average_word_length = []

# Iterate over the files in the 'text_dir' directory
for file in os.listdir(text_dir):
    # Call the 'cleaned_words' function to calculate word count and average word length
    x, y = cleaned_words(file)

    # Append the results to the respective lists
    word_count.append(x)
    average_word_length.append(y)

# Define a function to count personal pronouns in a given text file
def count_personal_pronouns(file):
    # Open the text file located in the 'text_dir' directory
    with open(os.path.join(text_dir, file), 'r') as f:
        # Read the contents of the file into a variable 'text'
        text = f.read()

        # List of personal pronouns to search for
        personal_pronouns = ["I", "we", "my", "ours", "us"]

        # Initialize a counter to keep track of the pronoun count
        count = 0

        # Iterate over each personal pronoun
        for pronoun in personal_pronouns:
            # Use regular expression to find and count occurrences of the pronoun with word boundaries
            count += len(re.findall(r"\b" + pronoun + r"\b", text))

    # Return the total count of personal pronouns in the text file
    return count

# Initialize an empty list to store personal pronoun counts for each file
pp_count = []

# Iterate over the files in the 'text_dir' directory
for file in os.listdir(text_dir):
    # Call the 'count_personal_pronouns' function to count personal pronouns in the file
    x = count_personal_pronouns(file)

    # Append the result to the 'pp_count' list
    pp_count.append(x)

# Load the output data structure from the Excel file 'Output Data Structure.xlsx' into a DataFrame
output_df = pd.read_excel('Output Data Structure.xlsx')

# Drop rows at index 24 (26-2) and 37 (39-2) from the DataFrame 'output_df' as these urls are not available 404 error.
output_df.drop([24, 37], axis=0, inplace=True)
# We have found that avg sentence length = avg no of words per sentence.
# Define a list 'variables' containing the variables you want to add to the DataFrame
variables = [positive_score,
            negative_score,
            polarity_score,
            subjectivity_score,
            avg_sentence_length,
            Percentage_of_Complex_words,
            Fog_Index,
            avg_sentence_length,
            complex_word_count,
            word_count,
            avg_syllable_word_count,
            pp_count,
            average_word_length]

# Iterate over the 'variables' list along with their corresponding indices
for i, var in enumerate(variables):
    # Assign the values in each 'var' list to the corresponding column in 'output_df'
    output_df.iloc[:, i + 2] = var

# Save the updated DataFrame 'output_df' to an Excel file named 'Output_Data.xlsx'
output_df.to_excel('Output_Data.xlsx')
# LinkedIn Post Generator

## Project Overview:
The **LinkedIn Post Generator** is an interactive application that generates LinkedIn posts based on user-selected parameters such as **length**, **language**, and **topic** (tag). The system uses **few-shot learning** to replicate the writing style from existing posts and generates relevant posts accordingly. The backend uses **LangChain**, **Groq**, and **pandas**, and the frontend is built using **Streamlit**.

## Technologies Used:
- **Streamlit**: For the frontend interface to interact with users.
- **LangChain**: For building a language model pipeline to generate text.
- **Groq**: For using large language models to extract metadata and generate text.
- **Pandas**: For processing and analyzing the post data.
- **JSON**: For storing and managing posts data.

---

## Steps and Workflow:

### Step 1: Create the `requirements.txt` File
The `requirements.txt` file lists all the required dependencies:
```txt
streamlit==1.35.0
langchain==0.2.14
langchain-core==0.2.39
langchain-community==0.2.12
langchain_groq==0.1.9
pandas==2.0.2

- This file ensures that all the necessary libraries are installed in your environment.

### Step 2: Prepare Data (`raw_posts.json`)
You provided sample LinkedIn posts in JSON format, where each post includes:

- **Text**: The content of the LinkedIn post.
- **Engagement**: The engagement score of the post.

These posts are used to generate LinkedIn posts and to extract relevant metadata for future post generation.

### Step 3: Preprocess Data (`preprocess.py`)

The `preprocess.py` script performs preprocessing on the raw posts data. The key operations are:

- **Sanitize Text**: Removes invalid characters (like emojis) from the posts.
  
- **Metadata Extraction**: The script extracts metadata from each post, such as:
  - **Line count**: The number of lines in the post.
  - **Language**: The language of the post (either "English" or "Hinglish").
  - **Tags**: Relevant tags related to the post.

- **Tag Unification**: Similar tags are merged into one category, ensuring consistency.

This helps to clean and standardize the data before using it for post generation.


### Step 4: Few-Shot Learning (`few_shot.py`)

This script loads the processed posts and uses pandas to:

- **Normalize the data** into a structured format.
- **Categorize posts by length** (Short, Medium, Long) based on line count.
- **Filter posts** by different parameters like tag, language, and length.
- **Get the unique tags** present in the dataset.

The few-shot learning approach allows the generator to mimic the style of posts based on user inputs by using the filtered examples.

### Step 5: Post Generation (`post_generator.py`)

The `post_generator.py` script is responsible for generating LinkedIn posts based on user-selected criteria:

- **Length**: The length of the post (Short, Medium, Long).
- **Language**: The language of the post (English/Hinglish).
- **Tag**: The topic or tag of the post.

The system constructs a prompt dynamically, using few-shot examples filtered based on the selected criteria, and sends it to the Groq model to generate the post text.

### Step 6: Main App (`main.py`)

The Streamlit frontend provides an interactive user interface:

- Users can select the **length**, **language**, and **topic (tag)** using dropdowns.
- After selecting the options, users can click the **"Generate"** button to generate the LinkedIn post.
- The post is displayed directly on the page.

#### Final Workflow:
- **User Input**:
  - Selects a **tag (topic)**, **length (post size)**, and **language (English/Hinglish)**.
  
- **Post Generation**:
  - The backend fetches relevant posts based on the selected criteria, formats a prompt using few-shot learning, and sends it to the language model to generate a new post.

- **Output**:
  - The generated post is displayed on the Streamlit app for the user.

#### Key Features:
- Customizable input options for **topic**, **length**, and **language**.
- **Few-shot learning** to replicate the writing style of existing posts.
- **Real-time post generation** that’s both quick and interactive.

## **How to Explain the Project in an Interview:**

#### Introduction:
"I’ve built a LinkedIn Post Generator that helps users create LinkedIn posts based on three customizable inputs: length, language, and topic. The generator produces posts using a combination of a preprocessed dataset, few-shot learning, and natural language generation techniques."

#### Technologies:
"I used **Streamlit** for the front-end to create an interactive app, **LangChain** and **Groq** for generating posts using natural language models, and **pandas** for processing and analyzing data."

#### Data Preparation:
"The dataset includes raw LinkedIn posts with engagement scores. I preprocess the data to clean and extract metadata, such as the number of lines, language, and relevant tags, which are then used for generating similar posts."

#### Post Generation:
"I employed **few-shot learning** to generate new posts. Based on the user’s input, I filter the posts to match the selected criteria (tag, length, language), and then I use these filtered examples to generate a post in the same style using the language model."

#### Interactive Interface:
"The app allows users to easily select their preferred options from dropdown menus, and the system generates a new LinkedIn post accordingly. The entire process is seamless and fast, providing instant results for users."

### Key Features:
"Some key features of the app include:
- Customizable input options for topic, length, and language.
- Few-shot learning to replicate the writing style of existing posts.
- Real-time post generation that’s both quick and interactive."

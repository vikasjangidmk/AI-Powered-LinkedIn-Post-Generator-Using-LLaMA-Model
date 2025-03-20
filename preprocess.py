import json
import re
from llm_helper import llm  # Assuming this is your Groq model wrapper
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def sanitize_text(text):
    """Removes invalid UTF-8 characters (like emojis) from text."""
    return text.encode("utf-8", "ignore").decode("utf-8")


def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            post["text"] = sanitize_text(post["text"])  # Sanitize text
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post["tags"]
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # Use .get() to avoid KeyErrors
        post["tags"] = list(new_tags)

    if processed_file_path:
        with open(processed_file_path, "w", encoding="utf-8", errors="replace") as outfile:
            json.dump(enriched_posts, outfile, indent=4)
    else:
        print("Warning: No output file provided, skipping save step.")


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. Extract the following metadata:
    - "line_count": The number of lines in the post.
    - "language": The language of the post (either "English" or "Hinglish").
    - "tags": An array containing up to two relevant tags.

    Return only a *valid JSON object* with no explanations or extra text.
    
    Example output:
    json
    {{
        "line_count": 3,
        "language": "Hinglish",
        "tags": ["Influencer", "Organic Growth"]
    }}
    

    Post: {post}
    '''

    post = sanitize_text(post)  # Ensure text is clean before sending to Groq

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post}).content.strip()

    try:
        json_parser = JsonOutputParser()
        return json_parser.parse(response)
    except OutputParserException:
        try:
            return json.loads(response)  # Fallback to manual JSON parsing
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON received: {response}")  # Debugging
            raise OutputParserException("Failed to parse JSON response.")


def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post["tags"])

    unique_tags_list = ",".join(unique_tags)
    unique_tags_list = sanitize_text(unique_tags_list)  # Ensure no encoding issues

    template = '''
    I will give you a list of tags. You need to unify them based on these rules:
    1. Merge similar tags into a single category.
       - Example: "Jobseekers", "Job Hunting" → "Job Search"
       - Example: "Motivation", "Inspiration", "Drive" → "Motivation"
    2. Each tag should follow the *Title Case* format.
    3. Output a *valid JSON object*, mapping original tags to unified tags.

    Example Output:
    json
    {{
        "Jobseekers": "Job Search",
        "Job Hunting": "Job Search",
        "Motivation": "Motivation"
    }}
    

    Here is the list of tags: 
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list}).content.strip()

    try:
        json_parser = JsonOutputParser()
        return json_parser.parse(response)
    except OutputParserException:
        try:
            return json.loads(response)  # Fallback to manual JSON parsing
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON received: {response}")  # Debugging
            raise OutputParserException("Failed to parse JSON response.")


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
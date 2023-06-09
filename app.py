import openai
from googleapiclient.discovery import build
import requests
import json
import wikipedia
import requests
from bs4 import BeautifulSoup
import gradio as gr

# Set up the OpenAI API client
openai.api_key = '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'  # Replace with your actual API key

# Set up your YouTube Data API credentials
youtube_api_key = 'AIzaSyDYzXAkPqU6ODnGX9rEEcvL64xh29_LRVs'  # Replace with your actual YouTube API key

# Set up Google SERP API credentials
serp_api_key = '03c74289238ba82d2889379e7a958a07b56c45de'  # Replace with your actual Google SERP API key

# Function to send a message and receive a response from the chatbot
def chat(message):
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',  # Choose the language model/engine you want to use
            prompt=message,
            max_tokens=50,  # Adjust the response length as needed
            n=1,  # Number of responses to generate
            stop=None,  # Specify a stop token to end the response
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("An error occurred:", e)
        return ""

# Function to search for YouTube videos
def search_videos(query, max_results=5):
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    # Make a search request to retrieve video results
    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=max_results,
        type='video'
    ).execute()

    # Extract the video links from the search response
    video_links = []
    for item in search_response['items']:
        video_id = item['id']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        video_links.append(video_link)

    return video_links

# Function to get the latest answers from Google SERP API
def get_latest_answers(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': serp_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        # Parse the response JSON
        data = json.loads(response.text)

        # Extract details from the response
        output = ""

        if 'knowledgeGraph' in data:
            knowledge_graph = data['knowledgeGraph']
            output += "Website: {}\n".format(knowledge_graph.get('website'))
            output += "Description: {}\n".format(knowledge_graph.get('description'))

        if 'organic' in data:
            organic_results = data['organic']
            for result in organic_results:
                output += "Snippet: {}\n".format(result.get('snippet'))

        if 'peopleAlsoAsk' in data:
            people_also_ask = data['peopleAlsoAsk']
            for question in people_also_ask:
                output += "Snippet: {}\n".format(question.get('snippet'))

        return output

    except json.JSONDecodeError:
        print(".")
        return ""

    except Exception as e:
        print(".")
        return ""

# Function to search Wikipedia for an answer and summarize it
def search_wikipedia(query):
    try:
        search_results = wikipedia.search(query)

        # Get the page summary of the first search result
        if search_results:
            page_title = search_results[0]
            page_summary = wikipedia.summary(page_title)
            return page_summary
        else:
            print(".")
            return None
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation error
        print(".")
        return None
    except wikipedia.exceptions.PageError as e:
        # Handle page not found error
        print(".")
        return None
    except Exception as e:
        # Handle other exceptions
        print(".")
        return None

# Function to generate summarized paragraph using OpenAI API
def generate_summary(user_input):
    output = get_latest_answers(user_input)
    page_summary = search_wikipedia(user_input)
    chat_answer = chat(user_input)

    # Generate summarized paragraph using OpenAI API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Data from Google SERP API:\n{output}\nWikipedia summary:\n{page_summary}\n\nOpenAI chat response:\n{chat_answer}\n\nSummarize the above data into a paragraph.",
        max_tokens=200
    )
    summarized_paragraph = response.choices[0].text.strip()

    return summarized_paragraph

# Define the Gradio interface
def summarizer_interface(user_input):
    summarized_text = generate_summary(user_input)
    video_links = search_videos(user_input)
    return summarized_text, video_links

iface = gr.Interface(
    fn=summarizer_interface,
    inputs="text",
    outputs=["text", "text"],
    title="Osana Web-GPT",
    description="Enter your query and get latest and better answer.",
    layout="horizontal",
    examples=[
        ["What is the capital of France?"],
        ["How does photosynthesis work?"],
        ["Who is the president of the United States?"],
        ["What is the capital of Japan?"],
        ["How do I bake a chocolate cake?"],
        ["What is the meaning of life?"],
        ["Who painted the Mona Lisa?"],
        ["What is the population of New York City?"],
        ["How does the internet work?"],
        ["What is the largest planet in our solar system?"],
        ["What are the benefits of regular exercise?"],
        ]
)

# Launch the interface
iface.launch()

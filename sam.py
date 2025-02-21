import requests

# Define the API URL
api_url = "https://jsonplaceholder.typicode.com/posts"

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    # Process and print the first 5 posts
    for post in data[:5]:
        print(f"Post ID: {post['id']}")
        print(f"Title: {post['title']}")
        print(f"Body: {post['body']}\n")
else:
    print("Failed to retrieve data. Status code:", response.status_code)

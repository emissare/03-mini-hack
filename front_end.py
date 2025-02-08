# Python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import uvicorn

app = FastAPI()

LANGSTUDIO_URL = "http://localhost:8001/"  # Adjust as needed


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Professor Snake</title>
  <script>
    function sendQuery(){
      const query = document.getElementById("query").value;
      fetch('/chat', {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: query })
      })
      .then(response => response.json())
      .then(data => {
          document.getElementById("response").value = data.response;
      })
      .catch(error => console.error('Error:', error));
    }
  
    document.addEventListener("DOMContentLoaded", function(){
      document.getElementById("send-btn").addEventListener("click", sendQuery);
      document.getElementById("query").addEventListener("keydown", function(e){
        if(e.ctrlKey && e.key === "Enter"){
          e.preventDefault();
          sendQuery();
        }
      });
    });
  </script>
</head>
<body>
  <h2>Professor Snake</h2>
  <textarea id="query" rows="5" cols="60" placeholder="Enter your query here..."></textarea>
  <br><br>
  <button id="send-btn">Send</button>
  <br><br>
  <textarea id="response" rows="10" cols="60" readonly placeholder="Response will appear here..."></textarea>
</body>
</html>
"""


def send_query_to_langstudio(query):
    # Replace with your LangStudio API endpoint URL
    # l   url = "https://your-langstudio-instance.com/api/query"

    # Prepare the request headers and payload
    headers = {
        "Content-Type": "application/json",
        # If authentication is needed, add a line like:
        # "Authorization": "Bearer YOUR_API_TOKEN"
    }

    payload = {
        "query": query
        # Include any additional parameters, such as context or session info, if required
    }

    try:
        # Send the POST request with the query payload
        response = requests.post(LANGSTUDIO_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        # Process and return the JSON response from LangStudio
        data = response.json()
        return data

    except requests.RequestException as e:
        # Handle request exceptions (e.g., network issues or bad responses)
        print("An error occurred:", e)
        return None


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "")
    # Send the query to the local LangStudio instance
    # response = requests.get(LANGSTUDIO_URL)
    # print(response.content)
    # print(response.json())

    # ls_response = requests.post(LANGSTUDIO_URL, json={"query": query}).json()
    # return JSONResponse({"response": ls_response.get("response", "")})
    result = send_query_to_langstudio(query)
    if result:
        return ("response:", result)
    return {"response": "error"}


if __name__ == "__main__":
    # Run the Uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

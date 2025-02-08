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

    ls_response = requests.post(LANGSTUDIO_URL, json={"query": query}).json()
    return JSONResponse({"response": ls_response.get("response", "")})


if __name__ == "__main__":
    # Run the Uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")

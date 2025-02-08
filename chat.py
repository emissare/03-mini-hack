from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="o3-mini",
  messages=[
    {
      "role": "developer",
      "content": [
        {
          "type": "text",
          "text": "hi\n"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Hello! How can I assist you today?"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Hello there! What’s on your mind today?"
        }
      ]
    }
  ],
  response_format={
    "type": "text"
  },
  reasoning_effort="high"
)

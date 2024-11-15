from langchain_groq import ChatGroq

llm = ChatGroq(

    temperature=0,
    model="llama-3.1-70b-versatile",
    groq_api_key='USE-YOUR-API-KEY',
    
)

response = llm.invoke("What are things you can do, Tell some exam of india that you can able to clear , and can you able to clear aptitude")
print(response.content)
#pandas
import pandas as pd

#Creating a chroma client
import uuid
import chromadb
client = chromadb.Client()

#langchain
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

#main.py
from main import llm

#collection
collection = client.create_collection(name="user_collection")

'''
#Add some text documents to the collection
collection.add(
    documents=[
        "This is a document about New York",
        "This is a document about canada"
    ],
    ids=["id1","id2"]
)

result=collection.query(
    query_texts=['A country which symbol is Maple leaf'],
    n_results=2
)

#print(result)
'''

#webscraping using langchain
loader = WebBaseLoader("https://www.google.com/about/careers/applications/jobs/results/93855920110346950-senior-software-engineer-aiml-genai-google-cloud-ai")
page_data = loader.load().pop().page_content

#print(page_data)

prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
)

chain_extract = prompt_extract | llm 
res = chain_extract.invoke(input={'page_data':page_data})
#print(type(res.content))

json_parser = JsonOutputParser()
json_res = json_parser.parse(res.content)
#print(type(json_res))

#Reading files 'portfolio' using pandas
df = pd.read_csv("files/my_portfolio.csv")


#database creation
client = chromadb.PersistentClient('vectorstore')
collection = client.get_or_create_collection(name="portfolio")

if not collection.count():
    for _, row in df.iterrows():
        collection.add(documents=row["Techstack"],
                       metadatas={"links": row["Links"]},
                       ids=[str(uuid.uuid4())])

job = json_res[0]
job['skills'] 

links = collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])



        
#EMAIL
prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Karthi, a business development executive at Company. Company is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools. 
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
        process optimization, cost reduction, and heightened overall efficiency. 
        Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Company 
        in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase Company's portfolio: {link_list}
        Remember you are Karthi, BDE at Company. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """
        )

chain_email = prompt_email | llm
res = chain_email.invoke({"job_description": str(job), "link_list": links})
print(res.content)



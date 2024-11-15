#Creating a chroma client
import chromadb
client = chromadb.Client()

#collection
collection = client.create_collection(name="user_collection")

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

print(result)
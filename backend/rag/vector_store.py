import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="study_notes"
)


def store_chunks(chunks):

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks
    )
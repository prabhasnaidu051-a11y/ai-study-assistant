from chromadb import PersistentClient

client = PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="study_documents"
)


def store_chunks(chunks: list[str]):

    collection.add(
        documents=chunks,
        ids=[
            str(i)
            for i in range(len(chunks))
        ]
    )

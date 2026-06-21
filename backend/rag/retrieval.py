from .vector_store import collection


def retrieve_context(
    query: str,
    n_results: int = 3
):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if results["documents"] is None:
        return ""

    documents = results["documents"][0]

    return "\n\n".join(documents)

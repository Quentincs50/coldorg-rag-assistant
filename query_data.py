import argparse
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from helper import get_embedding
from langchain_chroma import Chroma
from setup_database import CHROMA_PATH


PROMPT_TEMPLATE = """
Tu es un assistant expert en maintenance (chauffage, climatisation, plomberie).
Réponds à la question du technicien en te basant UNIQUEMENT sur le contexte fourni.
Si tu ne trouves pas la réponse dans le contexte, dis-le clairement.

Contexte :
{context}

---

Question du technicien : {question}
"""

""" def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text) """

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    model = OllamaLLM(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

""" if __name__ == "__main__":
    main() """
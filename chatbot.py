import streamlit as st
from query_data import query_rag
from setup_database import DOCS_PATH, JSON_PATH, add_to_chroma, split_documents, load_interventions, load_txt_docs

with st.sidebar:
    st.header("📂 Ajouter des données")
    uploaded_files = st.file_uploader(
        "Déposez vos fichiers ici",
        type=["txt", "json"],
        accept_multiple_files=True
    )

if uploaded_files and st.button("Indexer les fichiers"):
    docs = []
    # Store the file in the correct directory.
    for file in uploaded_files:
        if file.name.endswith(".json"):
            save_path = f"{JSON_PATH}/{file.name}"
        else:  
            save_path = f" {DOCS_PATH}/{file.name}"

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        st.success(f"Fichier sauvegardé dans {save_path}")

        # Adding the file to the DB.
        with st.spinner("Indexation en cours..."):
            if file.name.endswith(".json"):
                docs = load_interventions()
            else:
                docs = load_txt_docs()

            chunks = split_documents(docs)
            add_to_chroma(chunks)

        st.success("Indexation terminée !")


st.title("🔧 Assistant Maintenance COLDORG")

# Initialise l'historique de conversation.
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour je suis COLDBOT! Décrivez la panne ou posez votre question technique."}]

# Affiche l'historique.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input utilisateur.
if prompt := st.chat_input("Décrivez la panne..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Analyse en cours..."):
        response = query_rag(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
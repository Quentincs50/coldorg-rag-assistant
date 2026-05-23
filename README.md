<a id="readme-top"></a>

<div align="center">
  <br />
      <img src="public/chatbot.png" alt="Project Banner">
  <br />

  <div>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" />
  <img src="https://img.shields.io/badge/ChromaDB-FF6719?style=for-the-badge&logoColor=white" alt="ChromaDB" />
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/Mistral_AI-FF7000?style=for-the-badge&logoColor=white" alt="Mistral" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logoColor=white" alt="uv" />
</div>

  <h3 align="center">Assistant IA Techniciens de Maintenance — COLDBOT</h3>

   <div align="center">
     Prototype d'assistant RAG (Retrieval-Augmented Generation) pour aider les techniciens de maintenance à diagnostiquer des pannes en s'appuyant sur l'historique des interventions et les fiches techniques équipements.
    </div>
</div>


<!-- SOMMAIRE -->
<div>
<details>
  <summary>Table de contenu</summary>
  <ol>
    <li>
      <a href="#le-projet">A propos du projet</a>
      <ul>
        <li><a href="#choix-de-la-stack">Stack Technique</a></li>
      </ul>
    </li>
    <li>
      <a href="#commencement">Commencer</a>
      <ul>
        <li><a href="#choix">Choix de la stack</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#lancement">Lancement</a></li>
      </ul>
    </li>
    <li><a href="#resultats-des-tests">Resultats des tests</a></li>
    <li><a href="#revue-de-code">Revue de code</a></li>
    <li><a href="#limites-identifiées">Limites identifiées</a></li>
    <li><a href="#piste-d-amélioration">Piste d'amélioration</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#inspiration">Inspiration</a></li>
  </ol>
</details>
</div>

## Commencement

### Choix de la stack

Python - Langage de référence pour les projets Data/IA, écosystème riche et adapté au RAG.

LangChain - Framework qui structure le pipeline RAG (loaders, splitters, chaînes). Permet de se concentrer sur la logique métier.

ChromaDB - Base vectorielle légère qui persiste sur disque. Pas besoin de serveur externe, s'intègre nativement avec LangChain. Idéal pour un prototype. À l'échelle 10 000 interventions, on passerait sur Qdrant ou Weaviate.

nomic-embed-text - Modèle d'embeddings open-source tournant en local via Ollama. Performant sur le français, aucune clé API requise, aucun coût.

Mistral 7B / Phi3 - LLM open-source tournant en local via Ollama. Zéro coût. Phi3 recommandé sur CPU avec RAM limitée. En production, on utiliserait une API comme Groq ou OpenAI pour la latence.

Ollama - Permet de faire tourner les modèles en local en une commande. Simplifie énormément le setup et garantit la reproductibilité.

Streamlit - Interface web en quelques lignes de Python. Dropzone pour uploader de nouvelles données, historique de conversation via st.session_state.

uv - Gestionnaire de packages moderne, plus rapide que pip. uv.lock garantit la reproductibilité exacte de l'environnement.

### Installation

1. **Cloner le dépôt :**

```bash
git clone https://github.com/Quentincs50/coldrog-rag-assistant
```
2. **Installer uv (si ce n'est pas déjà fait**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Configurer les variables d'environnements virtuel et installer les dépendances**
```bash
uv venv
source .venv/bin/activate
uv add langchain langchain-community langchain-ollama langchain-chroma chromadb python-dotenv streamlit
```

4. **Installer Ollama et les modèles**
```bash
# Installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Télécharger les modèles
ollama pull nomic-embed-text   # modèle d'embeddings (274 MB)
ollama pull mistral             # LLM principal (4.4 GB)
```
<p align="right">(<a href="#readme-top">retour haut de la page</a>)</p>

### Lancement 

1. **Indexation des données**
```bash
# Si vous utilisez python3
python3 setup_database.py 

# Sinon
python setup_database

# Pour réinitialiser la base ChromaDB
python main.py --reset
```

2. **Lancement streamlit**
```bash
streamlit run chatbot.py
```

## Resultats des tests

```bash
cat result_test.txt
```
<p align="right">(<a href="#readme-top">retour haut de la page</a>)</p>

## Revue de code

| Fichier | Rôle |
|---|---|
| `helper.py` | Initialisation du modèle d'embeddings (nomic-embed-text via Ollama) |
| `query_data.py` | Recherche vectorielle dans ChromaDB + construction du prompt + génération de la réponse via Mistral |
| `setup_database.py` | Chargement des fichiers JSON & TXT → découpage en chunks → calcul des IDs → indexation dans ChromaDB |

## Limites identifiées 

Lenteur en local sur CPU : Mistral 7B nécessite ~5 GB RAM. Sur une machine avec peu de RAM disponible, le modèle swap sur disque. En production : déploiement GPU ou API externe (Groq, OpenAI).

Mémoire de conversation limitée : l'historique Streamlit est en session, pas persistant.

## Pistes d'amélioration 

Si au lieu de 30 interventions il y en a 10 000 il faudrait filtrer par métadonnées, par marque ou code d'erreur avant la recherche. 
```bash
def load_interventions():
    loader = JSONLoader(
    file_path=f"{JSON_PATH}/{JSON_FILE_NAME}",
    jq_schema=".[]", # <--- ici
    text_content=False,
    )
    docs = loader.load()
    return docs
```

## Contact
Quentin Sanchez - [@Quentin_Sanchez](https://www.linkedin.com/in/quentin-sanchez-9b6741b6) - Linkedin

## Inspiration 

[pixegami-github](https://github.com/pixegami/rag-tutorial-v2/blob/main/.gitignore)

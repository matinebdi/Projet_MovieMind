from langchain_groq import ChatGroq
# Import des bibliothèques nécessaires
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from dotenv import load_dotenv
import streamlit as st
import os
from utils.vectorestore import load_vectorstore  # Simplification de l'import

# Chargement des variables d'environnement (clés API, etc.)
load_dotenv()

# Initialisation du modèle d'embedding
@st.cache_resource  # Cache la ressource pour éviter de la recharger à chaque requête
def get_embeddings():
    """
    Initialise le modèle d'embedding d'OpenAI.
    
    Les embeddings sont des représentations vectorielles du texte qui permettent
    de mesurer la similarité sémantique entre différents textes.
    
    Returns:
        OpenAIEmbeddings: Instance du modèle d'embedding configuré
    """
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY non trouvée dans les variables d'environnement")
    return OpenAIEmbeddings(
        api_key=openai_api_key,
        model="text-embedding-3-small"  # Modèle plus léger et économique
    )

# Initialisation du modèle de langage (LLM)
@st.cache_resource
def get_llm():
    """
    Initialise le modèle de langage Grok.
    
    Grok est un modèle de langage développé par xAI,
    offrant des performances de haut niveau pour la génération de texte.
    
    Returns:
        ChatOpenAI: Instance du modèle de langage configuré
    """
    gorq_api_key = st.secrets["GROQ_API_KEY"]
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY non trouvée dans les variables d'environnement")
    
    return ChatOpenAI(
        api_key=groq_api_key,
        temperature=0.7,  # Contrôle la créativité des réponses (0=conservateur, 1=créatif)
         model="llama-3.3-70b-versatile",
        
    )

# Chargement de la base de données vectorielle
@st.cache_resource
def get_vectorstore():
    """
    Charge la base de données vectorielle FAISS
    """
    return load_vectorstore()

# Création de la chaîne de conversation
def get_conversation_chain(vectorstore):
    """
    Configure la chaîne de conversation qui combine recherche et dialogue.
    
    Cette fonction:
    1. Initialise la mémoire pour garder le contexte de la conversation
    2. Crée un template de prompt qui guide le comportement de l'assistant
    3. Configure la chaîne de conversation qui utilise le LLM et la recherche
    
    Args:
        vectorstore: Base de données vectorielle pour la recherche
        
    Returns:
        ConversationalRetrievalChain: Chaîne de conversation configurée
    """
    # Initialisation de la mémoire pour le contexte
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Création du template de prompt
    template = """Tu es un assistant de recommandation de films amical,
                 compétent et créatif. Ta mission est de fournir des recommandations de films détaillées,
                 engageantes et personnalisées, en t'appuyant sur les éléments de contexte suivants.
                 Pour chaque recommandation, utilise le format markdown ci-dessous :

---s

### 🎬 [Nom du film]  
**⏱️ Durée :** [durée]  
**📊 Genre :** [genre]  
**🌟 Note IMDb :** [note]  

#### 🎥 Synopsis  
[description détaillée du film]  

#### 👥 Casting principal  
- [Acteur 1]  
- [Acteur 2]  
...  

#### 📝 Pourquoi le regarder ?  
[explication de l’intérêt ou des points forts du film]  

---

<contexte>  
{context}  
</contexte>  

Historique de conversation :  
{chat_history}  

**Instructions :**  
- Si la question posée est liée aux recommandations de films, réponds avec une ou plusieurs suggestions en suivant le format indiqué.  
- Si la question est hors sujet, réponds de manière polie et concise : "Malheureusement, je ne peux pas vous répondre à ce sujet."  

Humain : {question}  
Assistant : [Ta réponse ici]"""

    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "chat_history", "question"]
    )
    
    # Configuration de la chaîne de conversation
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=get_llm(),
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),  # Récupère les 3 documents les plus pertinents
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    return conversation_chain





    




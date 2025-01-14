"""
Script de génération de la base de données vectorielle pour l'assistant culinaire

Ce script transforme un fichier CSV contenant des recettes en une base de données vectorielle
utilisable par notre assistant culinaire. Il utilise plusieurs concepts clés :

1. Embeddings : Conversion de texte en vecteurs numériques permettant de mesurer
   la similarité sémantique entre différents textes.
   
2. Vectorstore : Base de données spécialisée qui stocke ces vecteurs et permet
   de faire des recherches par similarité.
   
3. RAG (Retrieval Augmented Generation) : Technique qui permet d'enrichir les réponses
   d'un LLM avec des données externes (ici, notre base de recettes).
"""

import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from typing import List
import os
from dotenv import load_dotenv
import pickle

load_dotenv()

def create_vectorstore(texts):
    """
    Crée un vectorstore FAISS à partir des textes donnés
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = FAISS.from_texts(texts, embeddings)
    save_vectorstore(vectorstore)
    return vectorstore

def save_vectorstore(vectorstore, path="data/vectorstore"):
    """
    Sauvegarde le vectorstore
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    vectorstore.save_local(path)

def load_vectorstore(path="data/vectorstore"):
    """
    Charge le vectorstore depuis un fichier
    """
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        return FAISS.load_local(
            path, 
            embeddings,
            allow_dangerous_deserialization=True  # À utiliser uniquement si vous faites confiance à la source du fichier
        )
    except FileNotFoundError:
        return None

def create_documents_from_csv(csv_path: str) -> List[Document]:
    """
    Crée une liste de documents à partir d'un fichier CSV
    """
    try:
        df = pd.read_csv('data/recommendation_dataset.csv')
        documents = []
        
        for _, row in df.iterrows():
            content = f"title: {row['title']}\n\nDescription: {row['overview']}\n\systeme de recommendation: {row['recommendations']}\n\note_moyenne: {row['note_moyenne']}"
            
            metadata = {
                'title': row['title'],
                'Description': row['overview'],
                'url': row['URL'] if 'URL' in row else '',
                'source': 'Movie_Mind'
            }
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        
        return documents
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV: {e}")
        return []

def main():
    """
    Fonction principale
    """
    os.makedirs("data/vectorstore", exist_ok=True)
    
    documents = create_documents_from_csv("data/recommendation_dataset.csv")
    texts = [doc.page_content for doc in documents]
    
    vectorstore = create_vectorstore(texts)
    print("Vectorstore FAISS créé avec succès")

if __name__ == "__main__":
    main()

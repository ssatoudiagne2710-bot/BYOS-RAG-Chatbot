# BYOS RAG Chatbot 🚀

Assistant intelligent basé sur une architecture RAG (Retrieval-Augmented Generation) pour l'analyse des tickets de déploiement chez Sonatel.

## 📸 Aperçu
![Captures d'écran de l'interface Gradio](./screenshots)

## 🛠️ Architecture
Le projet est divisé en 3 modules interconnectés pour plus de scalabilité :
- **DataLoader** : Ingestion et nettoyage des données depuis Elasticsearch.
- **RAGEngine** : Création d'embeddings et recherche vectorielle avec FAISS.
- **BYOSChatbot** : Logique métier et interface utilisateur (Gradio + Ollama).
- **app** : Fichier permettant de deployer l'interface gradio localement.

## 🚀 Installation

1. Cloner le projet :
   ```bash
   git clone [https://github.com/ssatoudiagne2710-bot/BYOS-RAG-Chatbot](https://github.com/ssatoudiagne2710-bot/BYOS-RAG-Chatbot)

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt

3. Créer et configurer le fichier .env :
    Exemple fichier .env.exemple
        ```text
        ES_HOST=votre_url_elasticsearch
        ES_USER=votre_utilisateur
        ES_PASSWORD=votre_mot_de_passe
        ES_INDEX=nom_de_l_index
        OLLAMA_MODEL=mistral

4. Lancer l'interface :
   ```bash
   python app.py

import os
import gradio as gr
from dotenv import load_dotenv # Import this
from data_loader import DataLoader
from rag_engine import RAGEngine
from chatbot import BYOSChatbot

# 1. Load the variables from the .env file
load_dotenv()

# 2. Extract variables using os.getenv
host = os.getenv("ES_HOST")
user = os.getenv("ES_USER")
password = os.getenv("ES_PASSWORD")
index_id = os.getenv("ES_INDEX")
model_name = os.getenv("OLLAMA_MODEL")

# 3. Initialize your classes using these variables
if __name__ == "__main__":
    loader = DataLoader(
        host=host, 
        user=user, 
        password=password, 
        index_id=index_id
    )
    
    print("Chargement des données...")
    raw_texts = loader.fetch_and_process()
    
    print("Indexation vectorielle...")
    engine = RAGEngine()
    engine.build_index(raw_texts)
    
    print("Démarrage du chatbot...")
    # You can also pass the model name here
    bot = BYOSChatbot(engine, model_ollama=model_name)
    
    demo = gr.ChatInterface(
        fn=bot.generate_response,
        title="Assistant BYOS - Sonatel",
        description="Posez vos questions sur les tickets de déploiement et les statistiques projets.",
        examples=["Combien de tâches à Dakar ?", "Donne moi les détails du ticket 41836"]
    )
    
    demo.launch()
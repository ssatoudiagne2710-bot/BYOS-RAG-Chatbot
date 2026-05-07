from langchain_ollama import OllamaLLM

class BYOSChatbot:
    def __init__(self, engine, model_ollama="mistral"):
        self.engine = engine
        self.llm = OllamaLLM(model=model_ollama)

    def generate_response(self, query, history):
        query_clean = query.lower().strip()
        greetings = ["hello", "hi", "bonjour", "salut", "hey", "test"]
        if query_clean in greetings:
            return "Bonjour ! Je suis l'assistant BYOS. Comment puis-je vous aider aujourd'hui ?"
        context = self.engine.search(query, k=7)
        recent_history = history[-4:] if history else []
        history_parts = []
        for msg in recent_history:
            role = "Utilisateur" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            history_parts.append(f"{role}: {content}")
        history_str = "\n".join(history_parts)
        prompt = f"""
        Tu es l'Expert Data Analyst du projet BYOS chez Sonatel. 
        
        CONTEXTE DE RÉFÉRENCE :
        {context}
        
        HISTORIQUE RÉCENT :
        {history_str}

        CONSIGNES :
        - Réponds uniquement en te basant sur le CONTEXTE ci-dessus.
        - Si l'information est absente, réponds que tu ne sais pas.
        - Utilise des tirets pour lister les tickets.
        - Priorise les [STATS] pour les volumes globaux.

        QUESTION : {query}
        RÉPONSE :
        """

        return self.llm.invoke(prompt)
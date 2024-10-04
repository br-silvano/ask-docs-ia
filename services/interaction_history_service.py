class InteractionHistoryService:
    def __init__(self, max_interactions=10):
        self.history = {}
        self.max_interactions = max_interactions

    def add_interaction(self, session_id, interaction):
        if session_id not in self.history:
            self.history[session_id] = []

        # Adiciona a nova interação
        self.history[session_id].append(interaction)

        # Limita o histórico ao máximo definido
        if len(self.history[session_id]) > self.max_interactions:
            self.history[session_id].pop(0)  # Remove a interação mais antiga

    def get_history(self, session_id):
        return self.history.get(session_id, [])

    def clear_history(self, session_id):
        if session_id in self.history:
            del self.history[session_id]

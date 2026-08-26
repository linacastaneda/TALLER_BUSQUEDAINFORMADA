from game import Agent, Directions

class SimpleAgent(Agent):
    """Agente mínimo para comprobar que el entorno Pac-Man inicia correctamente."""
    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        if not legal:
            return Directions.STOP
        return legal[0]

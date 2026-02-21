class AgentHooks:
    def before_ask(self, prompt):
        print(f"[HOOK] About to send prompt: {prompt}")

    def after_ask(self, response):
        print(f"[HOOK] Received response: {response}")

class AgentWithHooks:
    def __init__(self, hooks=None):
        self.hooks = hooks or AgentHooks()

    def ask(self, prompt):
        self.hooks.before_ask(prompt)
        # Simulate OpenAI call
        response = f"Simulated response for: {prompt}"
        self.hooks.after_ask(response)
        return response

# Example usage:
# agent = AgentWithHooks()
# agent.ask("Hello, agent!")


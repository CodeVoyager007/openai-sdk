import openai 
from openai import agents 

class Agent:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def ask(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message["content"]


def main():
    print("Hello from agents!")


if __name__ == "__main__":
    main()

# Example usage:
# agent = Agent()
# print(agent.ask("What is an OpenAI agent?"))

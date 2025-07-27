from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    output_guardrail,
)
from agents.models.gemini_provider import GeminiProvider
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Step 1: Setup Gemini Provider for guardrail
gemini_provider = GeminiProvider(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com",
)

# Step 2: Define output format
class KindResponseCheck(BaseModel):
    is_mean: bool
    reason: str

# Step 3: Guardrail agent using Gemini
guardrail_agent = Agent(
    name="Response Validator",
    instructions="Check if the agent's response is mean or unkind. Be honest.",
    output_type=KindResponseCheck,
    model="gemini/gemini-pro",  # Gemini model
    model_provider=gemini_provider,
)

# Step 4: Guardrail function
@output_guardrail
async def kindness_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem], output: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_mean,
    )

# Step 5: Main agent (OpenAI will be used by default)
main_agent = Agent(
    name="Helpful Agent",
    instructions="Respond kindly to user input with compassion and helpfulness.",
    output_guardrails=[kindness_guardrail],
)

# Step 6: Testing
async def run_tests():
    try:
        print("\n✅ TEST 1: Kind response")
        result = await Runner.run(main_agent, "Hi, how can I reset my password?")
        print("Agent replied:", result.final_output)
    except OutputGuardrailTripwireTriggered:
        print("🚫 Guardrail triggered (unexpected)")

    try:
        print("\n❌ TEST 2: Rude response simulation")
        rude_response = "Figure it out yourself. I'm not here to babysit you."
        result = await Runner.run(main_agent, "How do I fix this?")
        result.final_output = rude_response  # simulate a bad response
        print("Agent replied:", result.final_output)
    except OutputGuardrailTripwireTriggered:
        print("🔥 Guardrail triggered on rude output (expected)")

# Run test
if __name__ == "__main__":
    asyncio.run(run_tests())

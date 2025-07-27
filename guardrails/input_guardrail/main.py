from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables if needed
load_dotenv()

# Step 1: Define the output type for the guardrail agent
class AngryInputCheck(BaseModel):
    is_angry: bool
    reason: str

# Step 2: Create the guardrail agent that checks anger
guardrail_agent = Agent(
    name="Anger Detector",
    instructions="Check if the user sounds angry or is being rude. Say yes or no.",
    output_type=AngryInputCheck,
)

# Step 3: Create the actual guardrail decorator
@input_guardrail
async def angry_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_angry,
    )

# Step 4: Create the main customer support agent with input guardrail attached
main_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a useful agent that responds in a kind and respectful manner.",
    input_guardrails=[angry_guardrail],
)

# Step 5: Run test examples
async def run_tests():
    try:
        print("\n✅ TEST 1: Polite input")
        result = await Runner.run(main_agent, "Hi, can you please help me?")
        print("Agent replied:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🚫 Guardrail triggered on polite input (unexpected)")

    try:
        print("\n❌ TEST 2: Angry input")
        result = await Runner.run(main_agent, "Your service is stupid and terrible!")
        print("Agent replied (should not happen):", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🔥 Guardrail triggered on angry input (expected)")

# Run the test async
if __name__ == "__main__":
    asyncio.run(run_tests())

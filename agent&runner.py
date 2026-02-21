from agents import Agent, Runner,RunContextWrapper
import  os
math_tutor=Agent(
    name="Professor Numbers",
    instructions="you teach math with patience  and clear examples",
    model="gpt-4o",
    temperature=0.3
)

result=Runner.run_sync(math_tutor,"explain derivatives like i am 5 years old")
print(result.final_output)

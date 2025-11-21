from mcp.client.streamable_http import streamablehttp_client 
from strands import Agent 
from strands.tools.mcp.mcp_client import MCPClient
from strands.models import BedrockModel
# Set up the Claude model
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    region_name='us-east-1',
    temperature=0.3,
)
# Define system prompt for the customer support scenario
system_prompt = """
You are a customer support agent for AnyCompany Robotics, a company that makes smart robot vacuum cleaners.
You have access to several tools.
Your responsibilities include:
1. Understanding the customer's issue clearly.
2. Using available tools only when needed based on user input.
3. Always call the appropriate tool using exactly the required input (e.g., order ID, return code).
4. Summarizing the result in a helpful and empathetic tone (e.g., “Looks like your SmartVac S2 is still under warranty!”).
5. If you don’t have enough information to invoke a tool (like a missing order ID), ask the customer politely to provide it.
6. Keep answers focused and avoid unnecessary explanations.
7. Look up company information like what qualifies under warranty policy for returns and troubleshooting information.

If the customer is doing a return, do not ask them for the return code instead, write the return code in your self, based off of what they are returning the item for.
When generating a return label, use the label URL direct from the tool to send to the customer. Do not send any other URLs.
"""
# Transport setup for MCP tool server
def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")
# Initialize MCP client and agent
mcp_client = MCPClient(create_transport)
with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(model=bedrock_model, tools=tools, system_prompt=system_prompt)
    print("🤖 AnyCompany Support Agent — type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Agent: Thanks for chatting. Goodbye!")
            break
        response = agent(user_input)
        print(f"Agent: {response}")
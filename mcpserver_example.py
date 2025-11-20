from mcp.server import FastMCP
import boto3
import json

mcp = FastMCP("Robot Vacuum Customer Support Server")

lambda_client = boto3.client("lambda")
bedrock = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
KB_ID = "<INSERT KNOWLEDGE BASE ID HERE>"

def wrap_tool_result(text_or_dict) -> dict:
    """Wraps any tool response into MCP expected format."""
    if isinstance(text_or_dict, dict):
        text = json.dumps(text_or_dict, indent=2)
    else:
        text = str(text_or_dict)
    return {
        "content": [
            {
                "type": "TEXT",
                "text": text
            }
        ]
    }

def invoke_lambda(function_name: str, payload: dict) -> dict:
    """Helper to invoke Lambda with error handling"""
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )
        raw = json.loads(response["Payload"].read())
        if "errorMessage" in raw:
            return {"error": raw["errorMessage"]}
        return json.loads(raw["body"])
    except Exception as e:
        return {"error": f"Lambda invocation failed: {str(e)}"}

@mcp.tool(description="Fetch a customer’s order details using their orderID.")
def order_lookup(order_id: int) -> dict:
    """Fetch a customer’s order details using their orderID."""
    payload = {"orderId": order_id}
    response = lambda_client.invoke(
        FunctionName="<INSERT LAMBDA NAME HERE>", 
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    raw = json.loads(response["Payload"].read())
    result = json.loads(raw["body"])
    return wrap_tool_result(result)

@mcp.tool(description="Fetch a customer’s product warranty eligibility details using their orderID.")
def warrenty_lookup(order_id: int) -> dict:
    payload = {"orderId": order_id}
    response = lambda_client.invoke(
        FunctionName="<INSERT LAMBDA NAME HERE>", 
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    raw = json.loads(response["Payload"].read())
    result = json.loads(raw["body"])
    return wrap_tool_result(result)

@mcp.tool(description="Generate a return shipping label for a customer's product using orderID and return code.")
def return_label_generator(order_id: int, return_code: str) -> dict:
    payload = {"orderId": order_id, "return_code": return_code}
    response = lambda_client.invoke(
        FunctionName="<INSERT LAMBDA NAME HERE>", 
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )
    raw = json.loads(response["Payload"].read())
    result = json.loads(raw["body"])
    print(result)
    return wrap_tool_result(result)

@mcp.tool(description="Look up product information from manuals, FAQs, and support documentation.")
def product_info_lookup(query: str) -> dict:
    response = bedrock.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": query}
    )
    return wrap_tool_result(response)

mcp.run(transport="streamable-http")
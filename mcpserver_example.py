from mcp.server import FastMCP
import boto3
import json

# Inicialização do servidor MCP
mcp = FastMCP("Servidor de Suporte ao Cliente")

# Clientes AWS Lambda e Bedrock
lambda_client = boto3.client("lambda")
bedrock = boto3.client("bedrock-agent-runtime", region_name="sa-east-1")

# ID da Knowledge Base do Bedrock
KB_ID = "<INSIRA O ID DA KNOWLEDGE BASE AQUI>"

# Funções utilitárias
def encapsular_resultado_tool(text_or_dict) -> dict:
    """
    Encapsula qualquer resposta da tool
    no formato esperado pelo MCP.
    """
    if isinstance(text_or_dict, dict):
        text = json.dumps(text_or_dict, indent=2, ensure_ascii=False)
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
def invocar_lambda(nome_funcao: str, payload: dict) -> dict:
    """
    Função auxiliar para invocar uma Lambda
    com tratamento básico de erro.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=nome_funcao,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )

        raw = json.loads(response["Payload"].read())

        if "errorMessage" in raw:
            return {"erro": raw["errorMessage"]}

        return json.loads(raw["body"])

    except Exception as e:
        return {"erro": f"Falha ao invocar a Lambda: {str(e)}"}

# Tools
@mcp.tool(description="Busca os detalhes de um pedido de um cliente usando o orderId.")
def consultar_pedido(order_id: int) -> dict:
    payload = {"orderId": order_id}

    response = lambda_client.invoke(
        FunctionName="order-lookup-lambda",
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )

    raw = json.loads(response["Payload"].read())
    resultado = json.loads(raw["body"])

    return encapsular_resultado_tool(resultado)


@mcp.tool(description="Consulta a elegibilidade de garantia de um produto usando o orderId.")
def consultar_garantia(order_id: int) -> dict:
    payload = {"orderId": order_id}

    response = lambda_client.invoke(
        FunctionName="warranty-lookup-lambda",
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )

    raw = json.loads(response["Payload"].read())
    resultado = json.loads(raw["body"])

    return encapsular_resultado_tool(resultado)


@mcp.tool(description="Gera uma etiqueta de devolução para um produto usando orderId e código de devolução.")
def gerar_etiqueta_devolucao(order_id: int, codigo_devolucao: str) -> dict:
    payload = {
        "orderId": order_id,
        "return_code": codigo_devolucao
    }

    response = lambda_client.invoke(
        FunctionName="return-label-generator-lambda",
        InvocationType="RequestResponse",
        Payload=json.dumps(payload),
    )

    raw = json.loads(response["Payload"].read())
    resultado = json.loads(raw["body"])

    return encapsular_resultado_tool(resultado)


@mcp.tool(description="Busca informações do produto em manuais, FAQs e documentação de suporte.")
def consultar_informacoes_produto(consulta: str) -> dict:
    response = bedrock.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": consulta}
    )

    return encapsular_resultado_tool(response)


# Inicialização do servidor MCP
mcp.run(transport="streamable-http")

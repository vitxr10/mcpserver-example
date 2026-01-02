from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models import BedrockModel

# Configuração do modelo Claude no Amazon Bedrock
bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    region_name="sa-east-1",
    temperature=0.3,
)

# Prompt de sistema para o cenário de atendimento ao cliente
system_prompt = """
Você é um agente de atendimento ao cliente da AnyCompany Robotics, uma empresa que fabrica robôs aspiradores inteligentes.
Você tem acesso a diversas ferramentas.

Suas responsabilidades incluem:
1. Compreender claramente o problema do cliente.
2. Utilizar as ferramentas disponíveis apenas quando necessário, com base na solicitação do usuário.
3. Sempre chamar a ferramenta adequada usando exatamente os parâmetros exigidos (por exemplo: ID do pedido, código de devolução).
4. Resumir o resultado de forma útil e empática (exemplo: “Parece que o seu SmartVac S2 ainda está na garantia!”).
5. Caso não tenha informações suficientes para invocar uma ferramenta (como a ausência do ID do pedido), solicitar educadamente que o cliente forneça essa informação.
6. Manter as respostas objetivas e evitar explicações desnecessárias.
7. Consultar informações da empresa, como regras de garantia, políticas de devolução e instruções de solução de problemas.

Se o cliente estiver realizando uma devolução, não solicite o código de devolução. 
Em vez disso, determine o código de devolução por conta própria, com base no motivo informado pelo cliente.

Ao gerar uma etiqueta de devolução, utilize exclusivamente a URL da etiqueta retornada pela ferramenta para enviar ao cliente.
Não envie nenhum outro link ou URL.
"""

# Configuração do transporte para o servidor MCP
def create_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

# Inicialização do cliente MCP e do agente
mcp_client = MCPClient(create_transport)

with mcp_client:
    tools = mcp_client.list_tools_sync()
    agent = Agent(
        model=bedrock_model,
        tools=tools,
        system_prompt=system_prompt
    )

    print("🤖 Agente de Suporte AnyCompany — digite 'exit' para sair.\n")

    while True:
        user_input = input("Você: ")

        if user_input.lower() in ("exit", "quit"):
            print("Agente: Obrigado pelo contato. Até logo!")
            break

        response = agent(user_input)
        # print(f"Agente: {response}")

import json

# "Banco de dados" simulado
PEDIDOS_DB = [
    {
        "idPedido": 1001,
        "nomeCliente": "João Silva",
        "produto": "Robô Aspirador X200",
        "dataPedido": "2024-09-10",
        "status": "Entregue",
        "valor": 2499.90
    },
    {
        "idPedido": 1002,
        "nomeCliente": "Maria Oliveira",
        "produto": "Robô Aspirador Mini",
        "dataPedido": "2024-10-01",
        "status": "Enviado",
        "valor": 1799.00
    }
]

def lambda_handler(event, context):
    id_pedido = event.get("orderId")

    pedido = next((p for p in PEDIDOS_DB if p["idPedido"] == id_pedido), None)

    if not pedido:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "mensagem": f"Pedido {id_pedido} não encontrado"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(pedido)
    }
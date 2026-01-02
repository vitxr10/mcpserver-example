import json
from datetime import datetime

# "Banco de dados" simulado
GARANTIAS_DB = [
    {
        "idPedido": 1001,
        "anosGarantia": 2,
        "dataCompra": "2024-09-10"
    },
    {
        "idPedido": 1002,
        "anosGarantia": 1,
        "dataCompra": "2024-10-01"
    }
]

def lambda_handler(event, context):
    id_pedido = event.get("orderId")

    garantia = next((g for g in GARANTIAS_DB if g["idPedido"] == id_pedido), None)

    if not garantia:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "mensagem": f"Não foi encontrada garantia para o pedido {id_pedido}"
            })
        }

    data_compra = datetime.strptime(garantia["dataCompra"], "%Y-%m-%d")
    data_fim_garantia = data_compra.replace(
        year=data_compra.year + garantia["anosGarantia"]
    )

    garantia_valida = datetime.utcnow() <= data_fim_garantia

    resposta = {
        "idPedido": id_pedido,
        "anosGarantia": garantia["anosGarantia"],
        "dataFimGarantia": data_fim_garantia.strftime("%Y-%m-%d"),
        "garantiaValida": garantia_valida
    }

    return {
        "statusCode": 200,
        "body": json.dumps(resposta)
    }
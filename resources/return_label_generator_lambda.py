import json
import uuid
from datetime import datetime

# "Banco de dados" simulado
PEDIDOS_DB = [
    {
        "idPedido": 1001,
        "produto": "Robô Aspirador X200",
        "nomeCliente": "João Silva"
    },
    {
        "idPedido": 1002,
        "produto": "Robô Aspirador Mini",
        "nomeCliente": "Maria Oliveira"
    }
]

CODIGOS_RETORNO_VALIDOS = ["DEFEITO", "ITEM_ERRADO", "INSATISFACAO"]

def lambda_handler(event, context):
    id_pedido = event.get("orderId")
    codigo_retorno = event.get("return_code")

    if codigo_retorno not in CODIGOS_RETORNO_VALIDOS:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "mensagem": f"Código de devolução inválido: {codigo_retorno}"
            })
        }

    pedido = next((p for p in PEDIDOS_DB if p["idPedido"] == id_pedido), None)

    if not pedido:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "mensagem": f"Pedido {id_pedido} não encontrado"
            })
        }

    etiqueta = {
        "idEtiquetaDevolucao": str(uuid.uuid4()),
        "idPedido": id_pedido,
        "produto": pedido["produto"],
        "cliente": pedido["nomeCliente"],
        "codigoDevolucao": codigo_retorno,
        "geradoEm": datetime.utcnow().isoformat(),
        "transportadora": "UPS",
        "codigoRastreio": f"UPS-{uuid.uuid4().hex[:10].upper()}"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(etiqueta)
    }
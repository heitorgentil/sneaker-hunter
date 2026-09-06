import requests
import pandas as pd


def coletar_tenis_yourid():

    url = "https://www.youridstore.com.br/api"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.youridstore.com.br",
        "Referer": "https://www.youridstore.com.br/"
    }

    tenis_encontrados = []
    pagina = 1

    while True:

        payload = {
            "json": None,
            "params": f"?page={pagina}&pageSize=24&textLink=sale&showProductGroupingFilter=true",
            "request": "111d873e-0fb6-4e48-88af-082c64b65e66/198bca71-8b1e-48d8-947f-79baa37b8fa7"
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        dados = response.json()
        produtos = dados["products"]

        if len(produtos) == 0:
            break

        print(f"\nPágina {pagina}")

        for produto in produtos:

            if "skUs" not in produto:
                continue

            skus = produto["skUs"]

            for sku in skus:

                tamanho = sku["variations"][0]["name"]
                estoque = sku["stock"]

                if "Tênis" in produto["name"] and tamanho == "41" and estoque > 0:

                    tenis = {
                        "id_produto": produto["idProduct"],
                        "nome": produto["name"],
                        "marca": produto["brand"]["name"],
                        "preco_original": produto["price"],
                        "preco_promocional": produto["pricePromotion"],
                        "tamanho": tamanho,
                        "estoque": estoque,
                        "imagem": "https:" + produto["imageHome"],
                        "link": f"https://www.youridstore.com.br/{produto['urlFriendly']}?sku={sku['idSku']}"
                    }

                    tenis_encontrados.append(tenis)

        pagina = pagina + 1

    df = pd.DataFrame(tenis_encontrados)
    df = df.drop_duplicates(subset=["id_produto"])
    df["desconto_pct"] = ((1 - (df["preco_promocional"] / df["preco_original"])) * 100).round(0)

    return df


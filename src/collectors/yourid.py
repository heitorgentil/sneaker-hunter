import requests

url = "https://www.youridstore.com.br/api"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://www.youridstore.com.br",
    "Referer": "https://www.youridstore.com.br/"
}

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
                print("\n👟", produto["name"])
                print("Preço original:", produto["price"])
                print("Preço promocional:", produto["pricePromotion"])
                print("Tamanho:", tamanho)
                print("Estoque:", estoque)

    pagina = pagina + 1
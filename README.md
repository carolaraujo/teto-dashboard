# TETO PE – Matriz de Expansão

Dashboard estático da Matriz de Expansão do TETO Pernambuco.

## Gerar o dashboard

Coloque a planilha `MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx` na pasta `conf` e execute no PowerShell, a partir da raiz do projeto:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install pandas openpyxl
Set-Location .\conf
..\.venv\Scripts\python.exe .\gerar_estatico.py .\MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx
```

O comando acima gera `conf/index.html` usando OpenStreetMap. A planilha de entrada e esse HTML gerado não são versionados, pois a planilha contém dados de contato e a página pode conter uma chave de API.

Para publicar o mapa com Google Maps, use uma chave com restrições de domínio e API configuradas no Google Cloud. Não salve nem envie a chave ao GitHub.

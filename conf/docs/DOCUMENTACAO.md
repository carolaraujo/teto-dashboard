# Dashboard Matriz de Expansão – TETO Pernambuco

Documento de referência para pessoas e IAs generativas entenderem, corrigirem e evoluírem o projeto.
Leia tudo antes de alterar código.

> O passo a passo de atualização do painel (conta no GitHub, pull request, regeração do `index.html`) está no `README.md`.

## 1. Objetivo
Painel que transforma a planilha **MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx** (aba `BASE_LOOKER`) em visualizações para priorizar expansão em comunidades de Pernambuco. Fluxo desejado (fluxograma): filtros por cidade → critérios (liderança, situação do terreno/fundiário, risco ambiental, segurança, idade/"mais de 1 ano") → % que atende aos critérios → MV (demanda construtiva, % barracos, nº de famílias) → indicação → comunidades em rede. Mapa georreferenciado quando possível.

## 2. Arquivos
| Arquivo | Função |
|---|---|
| `gerar_estatico.py` | **Fonte única** do dashboard estático. Lê a planilha, limpa os dados, embute tudo num `index.html` único (modelo HTML/JS na variável `MODELO`). |
| `index.html` | Saída gerada. É o que o GitHub Pages publica (precisa estar na **raiz** do repositório). Não editar à mão: edite o `.py` e gere de novo. |
| `app.py` + `requirements.txt` | Versão alternativa em Streamlit + Plotly (mesmos conceitos). Ver seção 9. |
| `MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx` | Dados. **Não versionar**: tem telefones e nomes de representantes. |

## 3. Como gerar
```bash
pip install pandas openpyxl
python gerar_estatico.py MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx --chave SUA_CHAVE_GOOGLE   # com Google Maps
python gerar_estatico.py MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx                             # sem chave: OpenStreetMap
```
A saída `index.html` é criada na pasta onde o comando roda. A última linha impressa informa quantas comunidades e quantas estão no mapa. Depois, substitua o `index.html` na raiz do repositório.

## 4. Dados (aba `BASE_LOOKER`, 62 linhas)
Colunas usadas e regras de limpeza (função na seção de dados do `.py`):
- `NOME_COMUNIDADE`: duplicatas por nome normalizado (sem acento/caixa) são unificadas, mantendo a primeira (62 → 59).
- `MUNICIPIO` → `mun`; vazio vira "Não informado".
- `STATUS_PADRONIZADO` → `status` (Já trabalhamos / Já visitamos / Não visitamos).
- `CATEGORIA` → `cat`. O valor numérico `2026` é erro de digitação na base e vira "Revisar (valor 2026)".
- `LIDERANCA_PADRONIZADA` → `lid` (Sim / Não / Não informado).
- `ORIGEM_MV` → `mv` (se ausente: `Aba_Origem == "MV2604"` → "MV 2026", senão "Fora do MV").
- `ENQUETE_FLAG` → `enq` (0/1). `N_FAMILIAS` → `fam`. `ANO_FORMACAO` → `ano`. `IDADE_ANOS` → `idade` (se vazio, calculada como ano atual − `ano`). `ANO_VISITA` → `visita`.
- `SITUACAO_FUNDIARIA`, `RISCO_AMBIENTAL`, `DEMANDA_CONSTRUTIVA` → `fund`, `risco`, `dem`.
- Coordenadas (prioridade): `COORDENADAS_MANUAL` ("lat,lon") → `LATITUDE_LINK`/`LONGITUDE_LINK` → extraídas de `LINK_EARTH` por regex `@lat,lon`.
- `LINK_EARTH` → `earth` (só se começar com http).
- Aba `PENDENCIAS`: exibida na aba "Pendências".

### Lacunas conhecidas da base (afetam gráficos)
Só 17 de 62 têm coordenadas; `N_FAMILIAS` 10; `ANO_FORMACAO` 9; `SITUACAO_FUNDIARIA` 7; `RISCO_AMBIENTAL`, `DEMANDA_CONSTRUTIVA`, `SEGURANCA`, `PCT_BARRACOS`, `INDICACAO` estão 100% vazias. O painel esconde filtros sem dados e avisa. Colunas sem uso ainda: `MAIS_DE_1_ANO`, `PCT_BARRACOS`, `INDICACAO`, `SEGURANCA`.

## 5. Estrutura do `index.html` gerado
- Dados embutidos como JSON (`const D=...`, pendências em `P`). **Sem telefone nem representante** (a página é pública).
- Filtros (`F` no JS): município, status, categoria, liderança, origem MV, situação fundiária, risco ambiental, demanda construtiva. Filtro com só "Não informado" é ocultado.
- Indicadores: comunidades, famílias (soma), % enquete, idade média.
- Abas: Visão geral, Mapa, Tabela, Pendências. A função `draw()` renderiza só a aba ativa.
- Gráficos (Plotly 2.35.2 via CDN): comunidades por município (seletor com a contagem por cidade e clique na barra filtram o painel inteiro; a aba Mapa mostra "Município: N comunidades · M no mapa"); status (rosca); liderança por status (barras empilhadas); seletor com enquete por status, visitas por ano e completude dos dados.
- Mapa: com `--chave`, Google Maps JS API (marcadores `google.maps.Marker`, enquadramento por `fitBounds`); sem chave, Plotly `scattermapbox` com OpenStreetMap, com centro e zoom calculados pelos pontos.
- A meta `notranslate` evita que o Chrome traduza a página e quebre o JavaScript.

## 6. Como alterar (receitas)
- **Novo gráfico:** adicionar um `<div class="p"><div id="cN" class="ch"></div></div>` na seção `viz` do `MODELO` e um `Plotly.react("cN", ...)` no bloco `if(aba==="viz")`.
- **Novo campo:** ler a coluna na construção de `rows` no `.py`, usar o campo no JS. Nunca incluir telefone, nome de representante ou outros dados pessoais.
- **Novo filtro:** acrescentar `["campo","Rótulo"]` em `F`.
- **Estilo:** bloco `<style>` no `MODELO` (variáveis CSS `--bg --fg --card --bd --ac`; suporta modo escuro).
- Depois de qualquer mudança: rodar o script, validar o JavaScript (`node --check` no conteúdo do `<script>`) e testar no navegador.

## 7. Google Maps (chave de API)
1. Google Cloud → projeto → ativar **Maps JavaScript API** → vincular faturamento (cartão; há uso gratuito mensal limitado, confira os preços atuais).
2. Criar chave em Credenciais. **Restringir por site:** `https://carolaraujo.github.io/*`. **Restringir por API:** só Maps JavaScript API.
3. Definir limite diário de carregamentos e alerta de orçamento.
4. A chave **fica visível no HTML** (é assim que a API funciona); a proteção são as restrições. Nunca versionar chave sem restrição.
5. O Google bloqueia o mapa em arquivo aberto localmente (`file://`); testar pelo endereço publicado.
6. Chave inválida ou sem faturamento mostra erro do Google; a página não volta sozinha ao OpenStreetMap (gerar sem `--chave`).

## 8. Publicação (GitHub Pages)
- Repositório `carolaraujo/teto-dashboard` (**público**; o plano gratuito exige isso). Settings → Pages → Deploy from a branch → `main` → `/ (root)`.
- Endereço: `https://carolaraujo.github.io/teto-dashboard/`.
- **Não preencher "Domínio personalizado"** (a menos que exista domínio registrado com DNS apontado). Preencher o campo cria um arquivo `CNAME` e, sem DNS válido, bloqueia a publicação com `InvalidDNSError`. Se isso ocorrer: remover o domínio e apagar o `CNAME`.
- Atualizar dados: regerar o `index.html` e substituir na raiz.

## 9. Versão Streamlit (`app.py`)
Streamlit Community Cloud, `app/app.py`, branch `master`. Funciona com upload da planilha (`dados_enviados.xlsx` salvo no servidor, apagado quando o app reinicia). `requirements.txt`: `streamlit>=1.50`, `pandas`, `plotly>=5.24`, `openpyxl`. Usa `width="stretch"` (o parâmetro `use_container_width` está depreciado). A planilha opcional deve ficar na mesma pasta do `app.py`.

## 10. Problemas já encontrados
- Streamlit "Failed to download the sources": falha de acesso ao GitHub; reiniciar o app e conferir permissões.
- `removeChild ... não é filho deste nó`: tradução automática do navegador; desativar a tradução.
- Mapa abrindo no oceano: faltava `center`/`zoom`; corrigido com enquadramento pelos pontos.
- Gráficos sobrepostos em tela grande: faltava altura fixa nos contêineres (`.ch`); corrigido.

## 11. Privacidade
O repositório é público: não versionar a planilha, telefones, nomes de representantes nem chaves sem restrição. O `index.html` contém nomes de comunidades, municípios, coordenadas, número de famílias e status.
<p align="center">
  <img src="logo-teto.png" alt="TETO Pernambuco" width="160">
</p>

# Dashboard Matriz de Expansão – TETO Pernambuco

Painel interativo das comunidades mapeadas pela equipe de Diagnóstico da TETO Pernambuco: filtros por município, status, liderança e outros critérios, mapa, indicadores e gráficos.

**Painel no ar:** https://carolaraujo.github.io/teto-dashboard/

**Conteúdo deste README**
1. Como atualizar o painel (passo a passo, para quem vai enviar uma planilha nova)
2. Para quem mantém o projeto (gerar e publicar o painel)
3. Documentação técnica

---

## 1. Como atualizar o painel (passo a passo)

A atualização é feita por **pull request**: você envia a planilha nova para o repositório, o responsável revisa e atualiza a página. Tudo é feito pelo navegador, sem instalar nada.

> **Aviso importante – privacidade.** Este repositório é **público**. Tudo o que é enviado, inclusive um pull request que ainda não foi aceito, pode ser visto por qualquer pessoa na internet. **Nunca envie telefones, nomes de representantes ou outros contatos.** A Parte 3 explica como preparar o arquivo.

> **Dica.** Se o seu navegador traduz o GitHub automaticamente, desative a tradução nessa página. Os botões abaixo aparecem em inglês e, entre parênteses, em português.

### Parte 1 – Ter acesso ao Drive da equipe
1. A planilha da Matriz de Expansão fica na pasta do Drive da equipe:
   https://drive.google.com/drive/folders/1h9vQgtb7PviNVxH9oLyvAUUpph8BbP26
2. Para ter acesso, **entre em contato com a equipe de Diagnóstico da TETO Pernambuco** e peça permissão para a pasta, informando o e-mail do Google que você usa.
3. Com o acesso liberado, abra a pasta e baixe a versão mais atual da planilha em **.xlsx**.

### Parte 2 – Criar a conta no GitHub (só na primeira vez)
1. Acesse **github.com** e clique em **Sign up** (Cadastrar-se).
2. Informe um e-mail, crie uma senha e escolha um nome de usuário (por exemplo, `nome-sobrenome`).
3. Resolva a verificação de que você não é um robô e digite o código recebido por e-mail.
4. Na pergunta sobre o plano, escolha o **gratuito (Free)**. Se aparecerem perguntas de personalização, clique em **Skip** (Pular).
5. Recomendado: ative a verificação em duas etapas em **Settings → Password and authentication → Two-factor authentication**.
6. Depois, entre sempre em **github.com** com esse usuário e senha.

### Parte 3 – Preparar a planilha
1. O arquivo precisa se chamar exatamente **`MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx`** e ser do tipo **.xlsx**. Se estiver em `.xls`, abra no Excel e use **Salvar como → Pasta de Trabalho do Excel (.xlsx)**.
2. Mantenha os nomes das abas (**`BASE_LOOKER`** e **`PENDENCIAS`**) e dos cabeçalhos das colunas. O programa que gera o painel procura por esses nomes e, se mudarem, os dados somem do painel.
3. **Antes de enviar, remova as colunas com dados de contato.** Faça isso numa **cópia** do arquivo e guarde o original completo no Drive da equipe:
   - `NOME_REPRESENTANTE`
   - `TELEFONE`
   - `OUTROS CONTATOS`

   O painel público não usa essas colunas, então removê-las não altera nada.
4. Colunas que o painel usa (não apague): `NOME_COMUNIDADE`, `MUNICIPIO`, `STATUS_PADRONIZADO`, `CATEGORIA`, `LIDERANCA_PADRONIZADA`, `ORIGEM_MV` (ou `Aba_Origem`), `ENQUETE_FLAG`, `N_FAMILIAS`, `ANO_FORMACAO`, `IDADE_ANOS`, `ANO_VISITA`, `SITUACAO_FUNDIARIA`, `RISCO_AMBIENTAL`, `DEMANDA_CONSTRUTIVA`, `LATITUDE_LINK`, `LONGITUDE_LINK`, `COORDENADAS_MANUAL` e `LINK_EARTH`.
5. Confira que nenhuma outra coluna ou célula contém dado pessoal (telefones escritos em observações, por exemplo).

### Parte 4 – Enviar a planilha e abrir o pull request

**4.1 Criar a sua cópia do repositório (fork)**
1. Entre no GitHub e abra **https://github.com/carolaraujo/teto-dashboard**.
2. Clique em **Fork** (Bifurcar), no canto superior direito, e depois em **Create fork** (Criar fork). Isso cria uma cópia do repositório na sua conta.
3. Se você já fez isso antes: abra o seu fork e, se aparecer o aviso "This branch is X commits behind", clique em **Sync fork → Update branch**. Assim a sua cópia fica igual à original.

**4.2 Enviar o arquivo**
1. No **seu fork**, abra a pasta **`conf`**.
2. Clique em **Add file → Upload files** (Adicionar arquivo → Fazer upload de arquivos).
3. Arraste o arquivo `MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx` para a área indicada. Se já existir um arquivo com esse nome, ele será substituído pelo novo.
4. Em **Commit changes** (Confirmar alterações):
   - No título, escreva algo como `Atualiza planilha - 16/11/2026`.
   - Marque a opção **Create a new branch for this commit and start a pull request** (Criar uma nova ramificação para esse commit e iniciar um pull request). Pode manter o nome sugerido.
5. Clique em **Propose changes** (Propor alterações).

**4.3 Abrir o pull request**
1. A tela **Open a pull request** (Abrir um pull request) aparece. Confira no topo:
   - **base repository:** `carolaraujo/teto-dashboard`, **base:** `main`.
   - **head repository:** o seu fork.
2. Preencha o título (por exemplo, `Atualização da planilha – novembro/2026`) e, na descrição, escreva:
   - a data da planilha;
   - o que mudou (novas comunidades, coordenadas preenchidas e assim por diante);
   - a confirmação de que as colunas de telefone e de representantes foram removidas.
3. Em **Files changed** (Arquivos alterados), confirme que aparece **apenas** o arquivo da planilha.
4. Clique em **Create pull request** (Criar pull request).

Pronto: o pull request foi enviado. Avise o responsável e aguarde a revisão. Se ele pedir ajustes, volte ao seu fork, repita o passo 4.2 e o pull request se atualiza sozinho.

### Parte 5 – Depois da aprovação (responsável pelo painel)
Aceitar o pull request guarda a planilha no repositório, mas **não atualiza a página publicada**. A página é um arquivo gerado a partir da planilha.
1. Revise o pull request: baixe a planilha em **Files changed** e confirme que não há telefones nem nomes de representantes.
2. Clique em **Merge pull request → Confirm merge**.
3. Atualize a cópia local da branch principal com a planilha aprovada (`git pull origin main`).
4. Gere o painel de novo (seção 2 abaixo) e substitua o **`index.html` da raiz** do repositório (**Add file → Upload files**), na branch `main`.
5. Espere 1 a 2 minutos e abra o painel com Ctrl+Shift+R para conferir.

### Problemas comuns
| Problema | O que fazer |
|---|---|
| Não tenho acesso à pasta do Drive | Peça à equipe de Diagnóstico da TETO Pernambuco, usando o mesmo e-mail com que você abre o Drive. |
| Não encontro o botão **Fork** | Entre no GitHub primeiro. Sem login, o botão não aparece. |
| O painel não mostrou os dados novos | O pull request ainda não foi aceito, ou o `index.html` ainda não foi regenerado (Parte 5). |
| O painel ficou vazio depois da atualização | Alguma aba ou coluna teve o nome alterado. Compare com a Parte 3. |
| O pull request mostra muitos arquivos | A sua cópia estava desatualizada. Faça **Sync fork → Update branch** e envie de novo. |
| O upload falha ou fica parado | O navegador aceita arquivos de até 25 MB. Tente outro navegador. |
| O mapa do Google mostra erro | Confira se a Maps JavaScript API e o faturamento estão ativos e se a chave permite o domínio do GitHub Pages. Ao abrir o HTML como arquivo local (`file://`), o painel usa OpenStreetMap. |
| Apareceu um erro de DNS ou de domínio na página | Não preencha "Custom domain" em Settings → Pages. Avise o responsável. |
| Enviei telefones por engano | Avise o responsável imediatamente. Fechar o pull request não apaga o arquivo do histórico, e pode ser necessário remover o fork e pedir suporte ao GitHub. |

---

## 2. Para quem mantém o projeto

O painel é um único `index.html` gerado pelo script `conf/gerar_estatico.py` a partir da planilha. O GitHub Pages publica o `index.html` da **raiz** do repositório. O gráfico de comunidades por município permite selecionar uma cidade ou clicar em uma barra para filtrar o painel e o mapa.

### Gerar o painel no PowerShell

Execute os comandos a partir da raiz do projeto. Se o ambiente virtual ainda não existir, crie-o:

```powershell
if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    py -3.10 -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install pandas openpyxl
Set-Location .\conf
```

Sem chave, o mapa usa OpenStreetMap:

```powershell
..\.venv\Scripts\python.exe .\gerar_estatico.py .\MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx
```

Para usar o Google Maps no site HTTPS do GitHub Pages, restrinja primeiro a chave no Google Cloud e gere o HTML com ela:

```powershell
$env:GOOGLE_MAPS_API_KEY = Read-Host "Cole a chave da API do Google Maps"
..\.venv\Scripts\python.exe .\gerar_estatico.py .\MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx --chave $env:GOOGLE_MAPS_API_KEY
Remove-Item Env:\GOOGLE_MAPS_API_KEY
```

O script cria `conf/index.html`. Copie-o para a raiz para atualizar o site:

```powershell
Copy-Item .\index.html ..\index.html -Force
Set-Location ..
```

- Mesmo com `--chave`, a cópia aberta diretamente como arquivo local (`file://`) usa OpenStreetMap. O Google Maps é carregado quando a página é servida por HTTP/HTTPS.
- A chave do Google fica **visível no HTML** (é assim que a API funciona). Restrinja-a ao site `https://carolaraujo.github.io/teto-dashboard/*` e à Maps JavaScript API, com limite diário e alerta de orçamento. Nunca publique uma chave sem restrições; se ela for exposta, revogue-a e crie outra.
- A planilha enviada por pull request deve ser a versão **sem contatos** (Parte 3). A planilha completa fica só no Drive da equipe.
- Não preencha "Custom domain" em Settings → Pages.
- Depois de conferir os arquivos, publique o `index.html` atualizado na branch `main`.

## 3. Documentação técnica

Regras de limpeza dos dados, estrutura do painel, configuração do Google Maps e do GitHub Pages, problemas já encontrados e receitas para alterar o código: veja [`DOCUMENTACAO.md`](./conf/docs/DOCUMENTACAO.md).

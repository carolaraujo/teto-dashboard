# Como atualizar o dashboard (pull request com a nova planilha)

Guia para quem vai enviar uma planilha nova para o repositório
**https://github.com/carolaraujo/teto-dashboard**. Não precisa saber programar nem instalar nada: tudo é feito pelo navegador.

> **Aviso importante – privacidade.** O repositório é **público**. Tudo o que é enviado, inclusive um pull request que ainda não foi aceito, pode ser visto por qualquer pessoa na internet. Por isso, **nunca envie telefones, nomes de representantes ou outros contatos**. A Parte 2 explica como preparar o arquivo.

> **Dica.** Se o seu navegador traduz o GitHub automaticamente, desative a tradução nessa página. Os nomes dos botões abaixo aparecem em inglês e, entre parênteses, em português.

## Visão geral
1. Criar a conta no GitHub (só na primeira vez).
2. Preparar a planilha.
3. Enviar a planilha e abrir o pull request.
4. Aguardar a revisão. Depois que o pull request for aceito, o responsável atualiza a página (Parte 4).

---

## Parte 1 – Criar a conta no GitHub (só na primeira vez)
1. Acesse **github.com** e clique em **Sign up** (Cadastrar-se).
2. Informe um e-mail, crie uma senha e escolha um nome de usuário (por exemplo, `nome-sobrenome`).
3. Resolva a verificação de que você não é um robô e digite o código recebido por e-mail.
4. Na pergunta sobre o plano, escolha o **gratuito (Free)**. Se aparecerem perguntas de personalização, clique em **Skip** (Pular).
5. Recomendado: ative a verificação em duas etapas em **Settings → Password and authentication → Two-factor authentication**.
6. Depois, entre sempre em **github.com** com esse usuário e senha.

## Parte 2 – Preparar a planilha
1. O arquivo precisa se chamar exatamente **`MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx`** e ser do tipo **.xlsx**. Se estiver em `.xls`, abra no Excel e use **Salvar como → Pasta de Trabalho do Excel (.xlsx)**.
2. Mantenha os nomes das abas (**`BASE_LOOKER`** e **`PENDENCIAS`**) e os nomes das colunas. O programa que gera o painel procura por esses nomes e, se mudarem, os dados somem do painel.
3. **Antes de enviar, remova as colunas com dados de contato.** Faça isso numa **cópia** do arquivo, e guarde o original completo com a equipe:
   - `NOME_REPRESENTANTE`
   - `TELEFONE`
   - `OUTROS CONTATOS`

   O painel público não usa essas colunas, então removê-las não altera nada.
4. Colunas que o painel usa (não apague): `NOME_COMUNIDADE`, `MUNICIPIO`, `STATUS_PADRONIZADO`, `CATEGORIA`, `LIDERANCA_PADRONIZADA`, `ORIGEM_MV` (ou `Aba_Origem`), `ENQUETE_FLAG`, `N_FAMILIAS`, `ANO_FORMACAO`, `IDADE_ANOS`, `ANO_VISITA`, `SITUACAO_FUNDIARIA`, `RISCO_AMBIENTAL`, `DEMANDA_CONSTRUTIVA`, `LATITUDE_LINK`, `LONGITUDE_LINK`, `COORDENADAS_MANUAL` e `LINK_EARTH`.
5. Confira que nenhuma outra coluna ou célula contém dado pessoal (telefones escritos em observações, por exemplo).

## Parte 3 – Enviar a planilha e abrir o pull request

### 3.1 Criar a sua cópia do repositório (fork)
1. Entre no GitHub e abra **https://github.com/carolaraujo/teto-dashboard**.
2. Clique em **Fork** (Bifurcar), no canto superior direito, e depois em **Create fork** (Criar fork). Isso cria uma cópia do repositório na sua conta.
3. Se você já fez isso antes: abra o seu fork e, se aparecer o aviso "This branch is X commits behind", clique em **Sync fork → Update branch**. Assim a sua cópia fica igual à original.

### 3.2 Enviar o arquivo
1. No **seu fork**, abra a pasta **`conf`**.
2. Clique em **Add file → Upload files** (Adicionar arquivo → Fazer upload de arquivos).
3. Arraste o arquivo `MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx` para a área indicada. Se já existir um arquivo com esse nome, ele será substituído pelo novo.
4. Em **Commit changes** (Confirmar alterações):
   - No título, escreva algo como `Atualiza planilha - 16/11/2026`.
   - Marque a opção **Create a new branch for this commit and start a pull request** (Criar uma nova ramificação para esse commit e iniciar um pull request). Pode manter o nome sugerido.
5. Clique em **Propose changes** (Propor alterações).

### 3.3 Abrir o pull request
1. A tela **Open a pull request** (Abrir um pull request) aparece. Confira no topo:
   - **base repository:** `carolaraujo/teto-dashboard`, **base:** `main`.
   - **head repository:** o seu fork.
2. Preencha o título (por exemplo, `Atualização da planilha – novembro/2026`) e, na descrição, escreva:
   - a data da planilha;
   - o que mudou (novas comunidades, coordenadas preenchidas e assim por diante);
   - a confirmação de que as colunas de telefone e de representantes foram removidas.
3. Em **Files changed** (Arquivos alterados), confirme que aparece **apenas** o arquivo da planilha.
4. Clique em **Create pull request** (Criar pull request).

Pronto: o pull request foi enviado. Avise o responsável e aguarde a revisão. Se ele pedir ajustes, volte ao seu fork, repita o passo 3.2 e o pull request se atualiza sozinho.

---

## Parte 4 – Depois da aprovação (responsável pelo painel)
Aceitar o pull request guarda a planilha no repositório, mas **não atualiza a página publicada**. A página é um arquivo gerado a partir da planilha.
1. Revise o pull request: baixe a planilha em **Files changed** e confirme que não há telefones nem nomes de representantes.
2. Clique em **Merge pull request → Confirm merge**.
3. No computador, coloque `gerar_estatico.py` e a planilha na mesma pasta e rode:
   ```bash
   python gerar_estatico.py MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx --chave SUA_CHAVE_GOOGLE
   ```
   A última linha informa quantas comunidades foram lidas e quantas aparecem no mapa. Se o número parecer errado, verifique a planilha.
4. Substitua o **`index.html` da raiz** do repositório (**Add file → Upload files**) pelo novo, na branch `main`.
5. Espere 1 a 2 minutos e abra **https://carolaraujo.github.io/teto-dashboard/** com Ctrl+Shift+R para conferir.

Os detalhes técnicos do projeto estão em `DOCUMENTACAO.md`.

---

## Problemas comuns
| Problema | O que fazer |
|---|---|
| Não encontro o botão **Fork** | Entre no GitHub primeiro. Sem login, o botão não aparece. |
| O painel não mostrou os dados novos | O pull request ainda não foi aceito, ou o `index.html` ainda não foi regenerado (Parte 4). |
| O painel ficou vazio depois da atualização | Alguma aba ou coluna teve o nome alterado. Compare com a Parte 2. |
| O pull request mostra muitos arquivos | A sua cópia estava desatualizada. Faça **Sync fork → Update branch** e envie de novo. |
| O upload falha ou fica parado | O navegador aceita arquivos de até 25 MB. Tente outro navegador ou reduza o arquivo. |
| Apareceu um erro de DNS ou de domínio na página | Não preencha "Custom domain" em Settings → Pages. Avise o responsável. |
| Enviei telefones por engano | Avise o responsável imediatamente. Fechar o pull request não apaga o arquivo do histórico, e pode ser necessário remover o fork e pedir suporte ao GitHub. |

# Flashcards de Luxemburguês para Anki

Este repositório contém flashcards de áudio em luxemburguês para usar no Anki.

Há duas versões:

- `FLASHCARDS/`: cards com tradução em português do Brasil.
- `FLASHCARDS_EN/`: cards com tradução em inglês dos EUA.

As duas versões usam os mesmos áudios:

```text
FLASHCARDS_MEDIA/
```

Cada áudio gera dois cards:

1. Frente com áudio; verso com transcrição em luxemburguês e tradução.
2. Frente com transcrição em luxemburguês; verso com áudio e tradução.

## 1. Baixar e instalar o Anki

1. Acesse o site oficial:

```text
https://apps.ankiweb.net/
```

2. Baixe a versão para o seu computador.
3. Instale e abra o Anki.
4. Crie um perfil se o Anki pedir.

Você não precisa criar conta no AnkiWeb para importar estes cards. A conta só é necessária se quiser sincronizar entre computador e celular.

## 2. Baixar este repositório

No GitHub, clique em:

```text
Code > Download ZIP
```

Depois extraia o arquivo `.zip` no seu computador.

Após extrair, você deve ver estas pastas:

```text
FLASHCARDS/
FLASHCARDS_EN/
FLASHCARDS_MEDIA/
```

Importante: os áudios estão armazenados com Git LFS. Se você baixar pelo botão `Download ZIP`, o GitHub normalmente inclui os arquivos reais. Se você clonar pelo Git, instale o Git LFS e rode:

```powershell
git lfs pull
```

## 3. Escolher qual versão importar

Para cards com tradução em português, use:

```text
FLASHCARDS/
```

Para cards com tradução em inglês, use:

```text
FLASHCARDS_EN/
```

Em qualquer uma das versões, você também precisa da pasta:

```text
FLASHCARDS_MEDIA/
```

Ela contém os áudios usados pelos cards.

## 4. Encontrar a pasta de mídia do Anki

O Anki guarda áudios e imagens em uma pasta chamada:

```text
collection.media
```

Locais mais comuns:

Windows:

```text
%APPDATA%\Anki2\NOME_DO_PERFIL\collection.media
```

macOS:

```text
/Users/SEU_USUARIO/Library/Application Support/Anki2/NOME_DO_PERFIL/collection.media
```

Linux:

```text
/home/SEU_USUARIO/.local/share/Anki2/NOME_DO_PERFIL/collection.media
```

Se você não sabe o nome do perfil, abra o Anki e vá em:

```text
File > Switch Profile
```

Em instalações novas, o perfil geralmente se chama `User 1`.

## 5. Abrir a pasta `collection.media`

### Windows

1. Feche o Anki.
2. Abra o Explorador de Arquivos.
3. Clique na barra de endereço.
4. Cole:

```text
%APPDATA%\Anki2
```

5. Pressione Enter.
6. Abra a pasta do seu perfil, por exemplo `User 1`.
7. Abra `collection.media`.

### macOS

1. Feche o Anki.
2. Abra o Finder.
3. No menu superior, clique em:

```text
Go > Go to Folder...
```

4. Cole:

```text
~/Library/Application Support/Anki2
```

5. Pressione Enter.
6. Abra a pasta do seu perfil, por exemplo `User 1`.
7. Abra `collection.media`.

### Linux

1. Feche o Anki.
2. Abra o gerenciador de arquivos.
3. Vá para:

```text
~/.local/share/Anki2
```

4. Abra a pasta do seu perfil, por exemplo `User 1`.
5. Abra `collection.media`.

## 6. Copiar os áudios

Abra a pasta deste repositório:

```text
FLASHCARDS_MEDIA/
```

Copie todos os arquivos `.mp3` de dentro dela para a pasta do Anki:

```text
collection.media/
```

Correto:

```text
collection.media/
  inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
  inll_6ec08fc98d25_A1_KAPITEL_1_Audio_01_002.mp3
```

Errado:

```text
collection.media/
  FLASHCARDS_MEDIA/
    inll_efebb85a6dde_A1_KAPITEL_1_Audio_01_001.mp3
```

Os arquivos `.mp3` precisam ficar diretamente dentro de `collection.media`, e não dentro de uma subpasta.

## 7. Criar os baralhos no Anki

Abra o Anki e crie os baralhos antes de importar os arquivos.

Uma estrutura recomendada é:

```text
Luxembourgish::A1::Kapitel 1
Luxembourgish::A1::Kapitel 2
Luxembourgish::A2::Kapitel 1
Luxembourgish::B1::Kapitel 1
```

Para a versão em inglês:

```text
Luxembourgish EN::A1::Kapitel 1
Luxembourgish EN::A2::Kapitel 1
Luxembourgish EN::B1::Kapitel 1
```

No Anki, `::` cria subbaralhos. Por exemplo:

```text
Luxembourgish::A1::Kapitel 1
```

cria `Kapitel 1` dentro de `A1`, dentro de `Luxembourgish`.

## 8. Importar os arquivos CSV

Cada capítulo tem um arquivo `.csv`.

Exemplos:

```text
FLASHCARDS/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
FLASHCARDS_EN/A1/KAPITEL 1/A1_KAPITEL 1_flashcards.csv
```

Para importar um capítulo:

1. Abra o Anki.
2. Clique no baralho onde esse capítulo deve entrar.
3. Vá em:

```text
File > Import
```

4. Escolha o arquivo `.csv` do capítulo.
5. Na tela de importação, confira:

```text
Type / Note Type: Basic
Deck: o baralho correto do capítulo
Field 1: Front
Field 2: Back
Separator: comma
Allow HTML in fields: ativado
```

6. Clique em Import.
7. Repita para cada capítulo que quiser importar.

Os arquivos CSV já começam com:

```text
#separator:comma
#html:true
#columns:Front,Back
```

Essas linhas ajudam o Anki a ler o arquivo corretamente.

## 9. Conferir se o áudio está funcionando

Depois de importar o primeiro capítulo:

1. Abra o navegador de cards do Anki.
2. Clique em um card importado.
3. Use a pré-visualização.
4. Aperte o botão de áudio/play.

Se o áudio não tocar:

1. Confira se os arquivos `.mp3` foram copiados para `collection.media`.
2. Confira se eles não ficaram dentro de uma subpasta.
3. No Anki, rode:

```text
Tools > Check Media
```

O Anki vai avisar se algum arquivo de mídia estiver faltando.

Se você já importou uma versão antiga deste baralho, apague os cards antigos antes de importar de novo. Os arquivos antigos começavam com `flashcards_`; os novos começam com `inll_` e incluem um hash do áudio para manter cada card sincronizado com o arquivo correto.

## 10. Configuração recomendada do Anki

Estas configurações são um bom ponto de partida para estudar idioma com áudio.

Abra as opções do baralho:

```text
Clique na engrenagem ao lado do baralho > Options
```

Configuração recomendada:

```text
FSRS: ativado
Desired retention: 0.90
New cards/day: 20 a 40
Maximum reviews/day: 9999
Learning steps: 10m
Relearning steps: 10m
Bury new siblings: ativado
Bury review siblings: ativado
```

Por que usar assim:

- `FSRS` é o agendador moderno do Anki e costuma funcionar melhor que o agendador antigo.
- `0.90` de retenção é um bom equilíbrio entre lembrar bem e não gerar revisões demais.
- `20 a 40` cards novos por dia já é bastante para progredir sem acumular uma fila enorme.
- `9999` em revisões evita que o Anki esconda cards vencidos.
- `Bury siblings` é útil porque cada áudio gera dois cards relacionados, e normalmente é melhor não ver os dois no mesmo dia.

Depois de algumas semanas estudando, rode:

```text
Deck Options > FSRS > Optimize
```

Assim o Anki ajusta o agendamento com base no seu histórico real de estudo.

## 11. Como estudar estes cards

Nos cards em que a frente é áudio:

1. Escute antes de ler qualquer coisa.
2. Tente entender o significado.
3. Mostre o verso.
4. Leia a transcrição em luxemburguês.
5. Leia a tradução.
6. Repita a frase em voz alta.

Nos cards em que a frente é a frase em luxemburguês:

1. Leia o luxemburguês.
2. Tente lembrar o significado.
3. Mostre o verso.
4. Escute o áudio.
5. Compare com a tradução.

Use os botões do Anki com honestidade:

- `Again`: você não entendeu ou esqueceu.
- `Hard`: você entendeu, mas com bastante esforço.
- `Good`: você entendeu bem o suficiente.
- `Easy`: foi imediato.

Não aperte `Hard` quando você esqueceu completamente. Nesse caso, use `Again`.

## 12. Referência das pastas

```text
FLASHCARDS/        CSVs com cards em português
FLASHCARDS_EN/     CSVs com cards em inglês
FLASHCARDS_MEDIA/  MP3s usados pelas duas versões
TRANSCRIPTS/       Transcrições em luxemburguês
TRANSLATION/       Traduções em português do Brasil
TRANSLATION_EN/    Traduções em inglês dos EUA
MANIFESTS/         Arquivos para auditar áudio, transcrição e tradução
scripts/           Scripts usados para gerar o projeto
```

## 13. Documentação oficial do Anki

- Baixar o Anki: https://apps.ankiweb.net/
- Importação: https://docs.ankiweb.net/importing/intro.html
- Importar arquivos de texto e mídia: https://docs.ankiweb.net/importing/text-files.html
- Arquivos do Anki e `collection.media`: https://docs.ankiweb.net/files.html
- Opções de baralho e FSRS: https://docs.ankiweb.net/deck-options

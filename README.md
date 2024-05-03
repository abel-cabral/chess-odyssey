# Chess Odyssey

## Descrição

Chess Odyssey é um jogo de xadrez interativo desenvolvido em Python utilizando a biblioteca Pygame. Este projeto foi criado como parte de uma disciplina de Desenvolvimento de Software do curso de Sistemas de Informação, onde o foco foi aprender sobre o ciclo de vida do desenvolvimento de software, incluindo planejamento, mensuração de tempo e organização de entregas. O jogo apresenta um modo de jogo onde um jogador humano desafia uma inteligência artificial (IA) otimizada pelo uso do motor de xadrez Stockfish.

## Stockfish: A Escolha de IA para Xadrez

Stockfish é um motor de xadrez de código aberto extremamente poderoso, conhecido por sua capacidade de análise profunda e velocidade, tornando-o uma excelente escolha para fortalecer a experiência de jogo em ChessMasterAI.

## Recursos

- Modo de Jogo Único\*\*: Enfrente a IA desafiadora em um jogo de xadrez.
- Interface Gráfica e Sonora\*\*: Aproveite uma interface simplificada com música de fundo que acompanha a jogabilidade.
- Compatibilidade\*\*: Jogue no macOS (arquivo DMG) e Windows (executável), com uma versão adicional disponível para desenvolvedores.

## Instalação e Execução

### Configuração do Ambiente

Siga as instruções detalhadas para configurar o ambiente e executar o jogo em modo de desenvolvimento:

1. Criar um ambiente virtual\*\* (Recomendado para isolar as dependências):

```bash
python3 -m venv chess
```

2. \*\*Ativar o ambiente virtual:

```bash
source chess/bin/activate
```

3. Instalar as dependências:

```bash
pip install -r requirements.txt
```

4. Para desativar o ambiente virtual, use:

```bash
deactivate
```

### Executar em modo desenvolvimento

Para iniciar o jogo, certifique-se de que o ambiente virtual esteja ativado e execute:

```bash
python3 app.py
```

### Build do Jogo

#### Criando o Executável para macOS:

1. Instale o UPX para ajudar a comprimir os binários:

```bash
brew install upx
brew install create-dmg
```

2. Crie o .app usando PyInstaller com a especificação dada:

```bash
pyinstaller chess.spec
```

3. Crie o arquivo DMG usando create-dmg:

```bash
create-dmg --volname "Xadrez" --window-pos 200 120 --window-size 800 400 --icon-size 100 --icon "Xadrez.app" 200 150 --hide-extension "Xadrez.app" --app-drop-link 600 150 --volicon "chess.icns" "dist/chess.dmg" "dist/Xadrez.app"
```

#### Criando o Executável:

O PyInstaller vai gerar um app de acordo com o Sistema Operacinal que esta rodando,
ou seja se em windows vai gerar .exe, se em MacOs vai gerar um .app e assim por diante.

1. Simplesmente execute o PyInstaller com o arquivo spec:

```bash
pyinstaller chess.spec
```

## Instalação e Execução (Mac)

Para limpar os diretórios de build após a compilação:

```bash
rm -fr build dist && pyinstaller chess.spec
```

Para executar o jogo diretamente no macOS a partir da raiz do projeto:

```bash
cd dist/Chess Odyssey.app/Contents/MacOS/ && ./Chess Odyssey
```

## Licença

Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## Contato

Abel Cabral de Arruda - https://github.com/abel-cabral

abel-cabral@outlook.com

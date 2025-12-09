# ♟️ Jogo de Damas Multiplayer (Python + FastAPI + WebSocket)

Este projeto é um **jogo de Damas multiplayer online**, desenvolvido em
**Python**, utilizando:

-   ⚡ FastAPI --- servidor HTTP + WebSocket\
-   🔌 WebSockets --- comunicação em tempo real entre dois jogadores\
-   🎨 HTML/CSS/JavaScript --- interface visual no navegador\
-   🧠 Regras da dama implementadas no backend em Python

Permite que **dois jogadores joguem entre si em tempo real**, cada um a
partir do navegador.

------------------------------------------------------------------------

## 🚀 Funcionalidades

-   ✔️ Tabuleiro 8x8 com peças posicionadas automaticamente\
-   ✔️ Turnos alternados (vermelho → preto)\
-   ✔️ Movimentos validados no servidor\
-   ✔️ Capturas por salto\
-   ✔️ Promoção para dama (rainha)\
-   ✔️ Atualização instantânea para os dois jogadores via WebSocket\
-   ✔️ Interface web simples e funcional\
-   ✔️ Sala padrão `default` funcionando automaticamente

> 🔧 Este projeto é ideal para estudos de game dev, lógica, multiplayer
> e WebSockets.

------------------------------------------------------------------------

## 🧱 Estrutura do Projeto

    dama-multiplayer/
    ├── server.py            # Servidor FastAPI + WebSocket
    ├── game.py              # Regras e lógica do jogo
    └── static/
        ├── index.html       # Interface do jogador
        └── client.js        # Cliente WebSocket + renderização

------------------------------------------------------------------------

## 🛠️ Requisitos

-   Python 3.8+\
-   pip instalado

Dependências:

    fastapi
    uvicorn[standard]

------------------------------------------------------------------------

## 🔧 Instalação

Clone o repositório:

``` bash
git git@github.com:TMJacometti/PythonGames.git
cd PythonGames
```

Crie um ambiente virtual (opcional):

``` bash
python -m venv .venv
```

Ative o ambiente:

**Windows**

``` bash
.venv\Scripts\activate
```

**Linux/Mac**

``` bash
source .venv/bin/activate
```

Instale as dependências:

``` bash
pip install fastapi "uvicorn[standard]"
```

------------------------------------------------------------------------

## ▶️ Como Executar

Na raiz do projeto, execute:

``` bash
uvicorn server:app --reload
```

O servidor ficará disponível em:

    http://localhost:8000

Abra o jogo no navegador:

    http://localhost:8000/static/index.html

💡 Para jogar multiplayer:

-   Abra duas janelas/abas do navegador\
-   O primeiro jogador conectado será **vermelho**\
-   O segundo será **preto**

------------------------------------------------------------------------

## 🎮 Como Jogar

-   Clique na peça que deseja mover\
-   Clique na casa de destino\
-   Se a jogada for válida, o servidor atualiza para ambos os jogadores\
-   Turnos são alternados automaticamente\
-   Promoção ocorre ao alcançar a última linha

Regras implementadas:

-   Movimentos diagonais\
-   Peças comuns movem apenas para frente\
-   Capturas por salto\
-   Promoção para dama

Regras ainda não implementadas:

-   Captura obrigatória\
-   Múltiplas capturas em sequência

------------------------------------------------------------------------

## 🌐 Arquitetura do Multiplayer

O servidor mantém:

-   Uma sala única `"default"`\
-   Estado completo do jogo (tabuleiro + turno)\
-   Lista de jogadores conectados\
-   Regras e validação das jogadas\
-   Broadcast do estado atualizado

Fluxo:

1.  Jogador envia:

    ``` json
    { "type": "move", "from": [r,c], "to": [r,c] }
    ```

2.  O servidor valida a jogada\

3.  O estado é enviado para ambos os jogadores\

4.  A interface se atualiza automaticamente

------------------------------------------------------------------------

## 📌 Melhorias Futuras

-   🔁 Suporte a múltiplas salas (códigos únicos para jogar com amigos)\
-   ♛ Regras completas da dama brasileira\
-   📱 Versão mobile otimizada\
-   🎨 Layout mais moderno\
-   💬 Chat no lobby\
-   🧠 Jogar contra IA\
-   🏆 Ranking e placar

------------------------------------------------------------------------

## 🤝 Contribuições

Pull requests são bem-vindos!\
Abra uma *issue* se quiser sugerir melhorias ou reportar bugs.

------------------------------------------------------------------------

## 📜 Licença

Este projeto está sob licença MIT.\
Sinta-se livre para usar e modificar.

------------------------------------------------------------------------

## 👨‍💻 Autor

Projeto criado e mantido por **Thiago Jacometti (TMJ Sistemas).\
Se quiser evoluir o game, bora codar. 🚀

# Classic Tetris Multiplayer

## Descrição

Classic Tetris Multiplayer é inspirado em __CTWC__(_Classic Tetris World Championship_), um Campeonato da versão de NES do Tetris, onde os jogadores jogam uns contra os outros para ver quem faz a maior pontuação. Como a versão original do jogo não conta com uma versão Multiplayer (No campeonato eles jogam com 2 consoles), esse trabalho tenta recriar o design do Campeonato sem a necessidade de 2 Nintendinhos. Para mais informações, ler o Relatório do Trabalho.

## Screenshots
> ADICIONAR Screenshots

## Como Utilizar

### Instale o Python3 + Pygame

> sudo apt-get install python3 \
> sudo apt-get install python3-pip \
> python3 -m pip install pygame

### Atualize os Códigos do server.py e tetris.py com o HOST e a Porta utilizada
> HOST = '127.0.0.1' # Modificar com o HOST a ser utilizado \
> PORT = 5000 # Modificar com a porta a ser utilizada 

### Inicialize o Servidor
> make server

### Entre no Jogo com o seu Usuário
> Python3 main.py NOMEDEUSUÁRIO

### Seu adversário entre no jogo com o Usuário dele
> Python3 main.py NOMEDOADVERSÁRIO

### Divirta-se!

## Considerações

Código do Tetris baseado do Site [Making Games with Python & Pygame](http://inventwithpython.com/pygame/)
	* [Chapter 7 - Tetromino](http://inventwithpython.com/pygame/chapter7.html)
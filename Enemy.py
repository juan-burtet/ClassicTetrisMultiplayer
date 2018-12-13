
'''
Classe inimigo que possui as informações do adversário
'''
class Enemy:

	'''
	Construtor da classe Enemy
	'''
	def __init__(self):
		# Nome do Inimigo
		self.name = ''
		# Pontuação Atual do Inimigo
		self.score = 0
		# Nivel do inimigo
		self.level = 0
		# Quantidade de linhas eliminadas
		self.lines = 0
		# Peça que está caindo
		self.fallingPiece = None
		# Próxima peça
		self.nextPiece = None
		# Campo do Inimigo
		self.board = []
		# Quantidade de vitórias
		self.wins = 0
		# Estado para saber se o inimigo está morto
		self.state = False

	'''
	Método que adiciona o
	nome do inimigo
	'''
	def setName(self, name):
		self.name = name
 
	'''
	Método que retorna o
	nome do inimigo
	'''
	def getName(self):
		return self.name

	'''
	Método que retorna a
	pontuação do inimigo
	'''
	def getScore(self):
		return self.score

	'''
	Método que retorna o
	nivel do inimigo
	'''
	def	getLevel(self):
		return self.level

	'''
	Método que retorna a quantidade
	de linhas eliminadas do inimigo
	'''
	def getLines(self):
		return self.lines

	'''
	Método que retorna a 
	peça que está caindo do inimigo
	'''
	def	getFallingPiece(self):
		return self.fallingPiece

	'''
	Método que retorna a 
	próxima peça do inimigo
	'''
	def	getNextPiece(self):
		return self.nextPiece

	'''
	Método que retorna o 
	campo do inimigo
	'''
	def	getBoard(self):
		return self.board

	'''
	Método que retorna a quantidade 
	de vitórias do inimigo
	'''
	def getWins(self):
		return self.wins

	'''
	Método que retorna o estado do inimigo
	'''
	def getState(self):
		return self.state
#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		# Diferênça de Pontuação
		self.diff = 0

	def setDiff(self, diff):
		self.diff = diff

	def getDiff(self):
		return self.diff

	'''
	Método que retorna um dict com os status
	'''
	def getStatus(self):
		# Dict com status
		status = {'name'		: self.name,
				  'score'		: self.score,
				  'level'		: self.level,
				  'lines'		: self.lines,
				  'fallingPiece': self.fallingPiece,
				  'nextPiece'	: self.nextPiece,
				  'board'		: self.board,
				  'wins'		: self.wins,
				  'state'		: self.state}

		# Retorna um dict com os status
		return status

	'''
	Método que adiciona o
	nome do inimigo
	'''	
	def setName(self, name):
		self.name = name
 	
	#Método que reseta os Status do inimigo
	def reset(self):
		self.score = 0
		self.level = 0
		self.lines = 0
		self.fallingPiece = None
		self.nextPiece = None
		self.board = []
		self.state = False

	'''
	Método para atualizar o status do inimigo
	'''
	def update(self, status):
		self.name = status['name']
		self.score = status['score']
		self.level = status['level']
		self.lines = status['lines']
		self.fallingPiece = status['fallingPiece']
		self.nextPiece = status['nextPiece']
		self.board = status['board']
		self.wins = status['wins']
		self.state = status['state']
		
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
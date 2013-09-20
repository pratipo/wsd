#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import RPi.GPIO as GPIO
import time, random

class Wsd:
	def __init__(self, o=0, m=20, h=7, w=5):
		# Open SPI device
		dev 		= "/dev/spidev0.0"
		self.spidev = file(dev, "wb")

		self.gamma 			= bytearray(256)
		for i in range(256):
			self.gamma[i] 	= int(pow(float(i) / 255.0, 2.5) * 255.0 + 0.5)
		self.asciiTable 	= [
				[0x00,0x00,0x00,0x00,0x00],   #   0x20 32
				[0x00,0x00,0x6f,0x00,0x00],   # ! 0x21 33
				[0x00,0x07,0x00,0x07,0x00],   # " 0x22 34
				[0x14,0x7f,0x14,0x7f,0x14],   # # 0x23 35
				[0x00,0x07,0x04,0x1e,0x00],   # $ 0x24 36
				[0x23,0x13,0x08,0x64,0x62],   # % 0x25 37
				[0x36,0x49,0x56,0x20,0x50],   # & 0x26 38
				[0x00,0x00,0x07,0x00,0x00],   # ' 0x27 39
				[0x00,0x1c,0x22,0x41,0x00],   # ( 0x28 40
				[0x00,0x41,0x22,0x1c,0x00],   # ) 0x29 41
				[0x14,0x08,0x3e,0x08,0x14],   # * 0x2a 42
				[0x08,0x08,0x3e,0x08,0x08],   # + 0x2b 43
				[0x00,0x50,0x30,0x00,0x00],   # , 0x2c 44
				[0x08,0x08,0x08,0x08,0x08],   # - 0x2d 45
				[0x00,0x60,0x60,0x00,0x00],   # . 0x2e 46
				[0x20,0x10,0x08,0x04,0x02],   # / 0x2f 47
				[0x3e,0x51,0x49,0x45,0x3e],   # 0 0x30 48
				[0x00,0x42,0x7f,0x40,0x00],   # 1 0x31 49
				[0x42,0x61,0x51,0x49,0x46],   # 2 0x32 50
				[0x21,0x41,0x45,0x4b,0x31],   # 3 0x33 51
				[0x18,0x14,0x12,0x7f,0x10],   # 4 0x34 52
				[0x27,0x45,0x45,0x45,0x39],   # 5 0x35 53
				[0x3c,0x4a,0x49,0x49,0x30],   # 6 0x36 54
				[0x01,0x71,0x09,0x05,0x03],   # 7 0x37 55
				[0x36,0x49,0x49,0x49,0x36],   # 8 0x38 56
				[0x06,0x49,0x49,0x29,0x1e],   # 9 0x39 57
				[0x00,0x36,0x36,0x00,0x00],   # : 0x3a 58
				[0x00,0x56,0x36,0x00,0x00],   # ; 0x3b 59
				[0x08,0x14,0x22,0x41,0x00],   # < 0x3c 60
				[0x14,0x14,0x14,0x14,0x14],   # = 0x3d 61
				[0x00,0x41,0x22,0x14,0x08],   # > 0x3e 62
				[0x02,0x01,0x51,0x09,0x06],   # ? 0x3f 63
				[0x3e,0x41,0x5d,0x49,0x4e],   # @ 0x40 64
				[0x7e,0x09,0x09,0x09,0x7e],   # A 0x41 65
				[0x7f,0x49,0x49,0x49,0x36],   # B 0x42 66
				[0x3e,0x41,0x41,0x41,0x22],   # C 0x43 67
				[0x7f,0x41,0x41,0x41,0x3e],   # D 0x44 68
				[0x7f,0x49,0x49,0x49,0x41],   # E 0x45 69
				[0x7f,0x09,0x09,0x09,0x01],   # F 0x46 70
				[0x3e,0x41,0x49,0x49,0x7a],   # G 0x47 71
				[0x7f,0x08,0x08,0x08,0x7f],   # H 0x48 72
				[0x00,0x41,0x7f,0x41,0x00],   # I 0x49 73
				[0x20,0x40,0x41,0x3f,0x01],   # J 0x4a 74
				[0x7f,0x08,0x14,0x22,0x41],   # K 0x4b 75
				[0x7f,0x40,0x40,0x40,0x40],   # L 0x4c 76
				[0x7f,0x02,0x0c,0x02,0x7f],   # M 0x4d 77
				[0x7f,0x04,0x08,0x10,0x7f],   # N 0x4e 78
				[0x3e,0x41,0x41,0x41,0x3e],   # O 0x4f 79
				[0x7f,0x09,0x09,0x09,0x06],   # P 0x50 80
				[0x3e,0x41,0x51,0x21,0x5e],   # Q 0x51 81
				[0x7f,0x09,0x19,0x29,0x46],   # R 0x52 82
				[0x46,0x49,0x49,0x49,0x31],   # S 0x53 83
				[0x01,0x01,0x7f,0x01,0x01],   # T 0x54 84
				[0x3f,0x40,0x40,0x40,0x3f],   # U 0x55 85
				[0x0f,0x30,0x40,0x30,0x0f],   # V 0x56 86
				[0x3f,0x40,0x30,0x40,0x3f],   # W 0x57 87
				[0x63,0x14,0x08,0x14,0x63],   # X 0x58 88
				[0x07,0x08,0x70,0x08,0x07],   # Y 0x59 89
				[0x61,0x51,0x49,0x45,0x43],   # Z 0x5a 90
				[0x3c,0x4a,0x49,0x29,0x1e],   # [ 0x5b 91
				[0x02,0x04,0x08,0x10,0x20],   # \ 0x5c 92
				[0x00,0x41,0x7f,0x00,0x00],   # ] 0x5d 93
				[0x04,0x02,0x01,0x02,0x04],   # ^ 0x5e 94
				[0x40,0x40,0x40,0x40,0x40],   # _ 0x5f 95
				[0x00,0x00,0x03,0x04,0x00],   # ` 0x60 96
				[0x20,0x54,0x54,0x54,0x78],   # a 0x61 97
				[0x7f,0x48,0x44,0x44,0x38],   # b 0x62 98
				[0x38,0x44,0x44,0x44,0x20],   # c 0x63 99
				[0x38,0x44,0x44,0x48,0x7f],   # d 0x64 100
				[0x38,0x54,0x54,0x54,0x18],   # e 0x65 101
				[0x08,0x7e,0x09,0x01,0x02],   # f 0x66 102
				[0x0c,0x52,0x52,0x52,0x3e],   # g 0x67 103
				[0x7f,0x08,0x04,0x04,0x78],   # h 0x68 104
				[0x00,0x44,0x7d,0x40,0x00],   # i 0x69 105
				[0x20,0x40,0x44,0x3d,0x00],   # j 0x6a 106
				[0x00,0x7f,0x10,0x28,0x44],   # k 0x6b 107
				[0x00,0x41,0x7f,0x40,0x00],   # l 0x6c 108
				[0x7c,0x04,0x18,0x04,0x78],   # m 0x6d 109
				[0x7c,0x08,0x04,0x04,0x78],   # n 0x6e 110
				[0x38,0x44,0x44,0x44,0x38],   # o 0x6f 111
				[0x7c,0x14,0x14,0x14,0x08],   # p 0x70 112
				[0x08,0x14,0x14,0x18,0x7c],   # q 0x71 113
				[0x7c,0x08,0x04,0x04,0x08],   # r 0x72 114
				[0x48,0x54,0x54,0x54,0x20],   # s 0x73 115
				[0x04,0x3f,0x44,0x40,0x20],   # t 0x74 116
				[0x3c,0x40,0x40,0x20,0x7c],   # u 0x75 117
				[0x1c,0x20,0x40,0x20,0x1c],   # v 0x76 118
				[0x3c,0x40,0x30,0x40,0x3c],   # w 0x77 119
				[0x44,0x28,0x10,0x28,0x44],   # x 0x78 120
				[0x0c,0x50,0x50,0x50,0x3c],   # y 0x79 121
				[0x44,0x64,0x54,0x4c,0x44],   # z 0x7a 122
				[0x00,0x08,0x36,0x41,0x41],   # [ 0x7b 123
				[0x00,0x00,0x7f,0x00,0x00],   # | 0x7c 124
				[0x41,0x41,0x36,0x08,0x00],   # ] 0x7d 125
				[0x04,0x02,0x04,0x08,0x04]   # ~ 0x7e 126
			]

		self.orientation	= o
		self.modules		= m
		self.moduleH		= h
		self.moduleW		= w
		self.mN 		= self.moduleH*self.moduleW

		self.preOffset		= self.moduleW * 10
		
		self.asciiString	= [32 for i in range(140 + 10)]
		if (self.orientation == 0):
			self.binMatrix 	= [[0 for i in range(h)] for j in range((140+10)*(w+1))]
		#TODO
		#elif (self.orientation == 1):
		#	self.binMatrix 	= [[0 for i in range(w)] for j in range(140*(h+1))]
		self.pixels 		= bytearray(m*w*h*3)
		
	def setText(self, t):
		self.asciiString  = [ord(c) for c in t]
		self.asciiTobinMatrix()

	def asciiTobinMatrix(self):
		bits = [1,2,4,8,16,32,64,128]
		# print range(len(self.asciiString))
		for char in range(len(self.asciiString)):

			if(self.orientation == 0):
				for col in range(self.moduleW):
					for row in range(self.moduleH):
						self.binMatrix[char*self.moduleW + col + char  + self.preOffset][row] = bool( self.asciiTable[self.asciiString [char]-32][col] & bits[row] )
			
			#TODO -> vertical assembly
			#elif(self.orientation == 1):
			#	for col in range(self.moduleW):
			#		for row in range(self.moduleH):
			#			self.binMatrix[char*self.moduleW + col][row]= bool( self.asciiTable[self.asciiString [char]-32][col] & bits[row] )




	def setPixel(self, x, y, color):
		
		b = x/int(self.moduleW)

		r = x%self.moduleW 			# division left-over part
		if (y%2 == 1): 				# if odd raw
			r = (self.moduleW-1) - r

		# pixels in previous panels + previous pixels in panel
		pindex = ( b*self.mN + ( y*int(self.moduleW) + r ) )*3
		for i in range(3):	
			self.pixels[pindex + i] = self.gamma[color[i]]

	def display(self):
		# print 'displaying text'
		self.spidev.write(self.pixels)
		self.spidev.flush()
		time.sleep(0.001)

	def loadPixels(self, color, offset=0):
		for x in range(self.modules*self.moduleW):
			for y in range(self.moduleH):

				if ( (x+offset)>=len(self.binMatrix) ): #OUT OF RANGE -> pixel is off 
					self.setPixel(x, y, [0, 0 ,0])
				else:
					if (self.binMatrix[x + offset][y]):
						c = [0,0,0]
						# fix diferent color schema in the last 9 modules
						#remap R G B chanels
						if (x < self.moduleW*11):
							# first 11 modules are GBR :$
							c = [color[1],color[2],color[0]]
						else:
							# last 9 modules are BRG :$
							c = [color[2],color[0],color[1]]
						#end fix

						self.setPixel(x, y, color)
					else:
						self.setPixel(x, y, [0, 0 ,0])
		self.display()

	def rollPixels(self):
		c = [0,0,0]
		ci = 0 #andom.randint(0,2)
		if ci == 0:
			c = [255,0,0]
		if ci == 1:
			c = [0,255,0]
		if ci == 2:
			c = [0,0,255]
	 	for offset in range(self.moduleW*len(self.asciiString)):
			self.loadPixels(c,offset)
	 		time.sleep(0.2)


d = Wsd()
d.setText('HELLO PARIS! testing the urban Word Space Display. Twit hashtagPKDECLICTIS to go on the street!!!')
while (True):
	d.rollPixels()

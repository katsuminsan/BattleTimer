import ui
import sound
import threading
import time


class BattleTimer(ui.View):
	setlist = [
		1,
		3,
		5,
		8,
		10,
		15,
		30,
		40,
		50,
		60
	]
	
	color_Lon = '#7878ff'
	color_Loff = '#0000ff'
	color_Ron = '#ff7878'
	color_Roff = '#ff0000'
	
	sound_effects = ['rpg:Footstep03', 'rpg:HandleCoins']
	#
	def __init__(self, width=820, height=400):
		self.bg_color = 'black'
		self.tint_color = '#0079ff'
		
		slider = ui.Slider(
			name='slider'
		)
		
		slider.frame = (373, 20, 240, 34)
		slider.value = 0.5
		slider.action = self.offset_slider
		
		_id = int(0.5 * (len(BattleTimer.setlist) - 1) // 1)
		lblTime = ui.Label(
			name='lblTime',
			text=f'{BattleTimer.setlist[_id]}',
			font=('<system>', 24)
		)
		
		lblTime.frame = (300, 20, 65, 34)
		lblTime.bg_color = 'darkgreen'
		lblTime.text_color = 'white'
		
		btnLeft = ui.Button(
			name='btnLeft',
			title='0',
			font=('<system>', 70)
		)
		btnLeft.frame = (80, 60, 320, 320)
		btnLeft.bg_color = BattleTimer.color_Loff
		btnLeft.tint_color = 'white'
		
		btnLeft.action = self.button_tapped
		
		btnRight = ui.Button(
			name='btnRight',
			title='0',
			font=('<system>', 70)
		)
		btnRight.frame = (430, 60, 320, 320)
		btnRight.bg_color = BattleTimer.color_Roff
		btnRight.tint_color = 'white'
		
		btnRight.action = self.button_tapped
		
		self.add_subview(slider)
		self.add_subview(lblTime)
		self.add_subview(btnLeft)
		self.add_subview(btnRight)
		
		self.init_appArds()
		
	def init_appArds(self):
		
		self.turn = ''
		self.counter = self.value2()
		
	def value2(self):
		_id = int(
			self['slider'].value * (len(BattleTimer.setlist) - 1) // 1
		)
		return BattleTimer.setlist[_id]
		
	def offset_slider(self, sender):
		tmr = self.value2()
		
		self['lblTime'].text = str(tmr)
		self['btnLeft'].title = str(tmr)
		self['btnRight'].title = str(tmr)
		self.turn = ''
		self.counter = tmr
		
	def button_tapped(self, sender):
		#
		if (sender.name == self.turn) or (self.turn == ''):
			if sender.name == 'btnRight':
				self.turn = 'btnLeft'
				self['btnLeft'].bg_color = BattleTimer.color_Lon
				self['btnRight'].bg_color = BattleTimer.color_Roff
			elif sender.name == 'btnLeft':
				self.turn = 'btnRight'
				self['btnRight'].bg_color = BattleTimer.color_Ron
				self['btnLeft'].bg_color = BattleTimer.color_Loff
			
			if sender.name != self.turn:
				self[self.turn].alpha = 0.6
				self[self.turn].alpha = 1.0
				self.counter_change()
		
	def counter_change(self):
		#
		self.th1 = threading.Thread(
			name=1,
			target=self.countdown,
			args=[self.counter]
		)
		self.th1.start()
		print(self.th1.ident)
		
	def countdown(self, set_sec):
		turn = self.turn
		set_sec += 1
		self[self.turn].title = str(set_sec)
		set_sec *= 1000
		for i in range(set_sec):
			if turn == self.turn:
				time.sleep(1/1000)
				ii = i % 1000
				iii = i // 1000
				if (ii == 0) & (iii >= 5):
					sound.play_effect(BattleTimer.sound_effects[0])
				elif (ii == 0) & (iii < 5):
					sound.play_effect(BattleTimer.sound_effects[1])
			else:
				return
			self[turn].title = str((set_sec - i)//1000)
		
		

w, h = ui.get_screen_size()

canvas_size = max(w, h)

sv = BattleTimer(canvas_size, canvas_size)
sv.name = 'BattleTimer2'
sv.present('fullscreen')

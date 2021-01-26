import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.app import App
import csv

class irenicApp(App):
	def build(self):
		
		# We are going to use screen manager, so we can add multiple screens
		# and switch between them
		self.screen_manager = ScreenManager()

		# Initial, connection screen (we use passed in name to activate screen)
		# First create a page, then a new screen, add page to screen and screen to screen manager
		self.ventas_page = VentasPage()
		screen = Screen(name='Ventas')
		screen.add_widget(self.ventas_page)
		self.screen_manager.add_widget(screen)

		# Info page
		self.info_page = InfoPage()
		screen = Screen(name='Info')
		screen.add_widget(self.info_page)
		self.screen_manager.add_widget(screen)


		return self.screen_manager

class VentasPage(BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"
			
		buscador = TextInput(
							text = "",
							multiline=False, 
							readonly=False, 
							halign="left", 
							font_size=55,
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
							)
		
		titulos = GridLayout(
							cols = 5,
							size_hint = (1, .2)
							)

		tit1 = Label (text = "Articulos",
						size_hint =(.4, 1),
						)
		tit2 = Label (text = "Precio",
						size_hint = (.2, 1),
						)
		tit3 = Label (text = "Stock",
					size_hint = (.2, 1),
					)
		tit4 = Label (text = "Cantidad",
					size_hint = (.1, 1),
					)
		tit5 = Label(text = "Agregar",
					size_hint = (.1, 1),
					)

		titulos.add_widget(tit1)
		titulos.add_widget(tit2)
		titulos.add_widget(tit3)
		titulos.add_widget(tit4)
		titulos.add_widget(tit5)

		buscador.bind(text = self.on_text)
		
		
		self.add_widget(buscador)

		self.add_widget(titulos)

		self.layout = GridLayout(cols = 5,
							spacing=5, 
							size_hint_y=None
							)
		# Make sure the height is such that there is something to scroll.
		self.layout.bind(minimum_height=self.layout.setter('height'))
		
			
		rotador = ScrollView(
							size_hint=(1, 1), 
							#size=(Window.width, Window.height),
							)
		
		rotador.add_widget(self.layout)
		
		self.add_widget(rotador)
	
	def agregar_art(self, instance):
		descripcion = self.desc.text
		precio_unit = self.precio.text
		cantidad_venta = self.cantidad.text
		subtotal = int(self.precio.text) * int(self.cantidad.text)
		
		info = f"{descripcion} {precio_unit} {cantidad_venta} {subtotal}"
		irenic_app.info_page.update_info(info)
		irenic_app.screen_manager.current = 'Info'
		#Clock.schedule_once(self.connect, 1)	
	
	def on_text(self, instance, value):
		self.layout.clear_widgets()
		with open("lista de productos total.csv") as f:
			lista = csv.reader(f, delimiter=',')
			indice = 0
			for articulo in lista:
				if value.lower() in articulo[1].lower() and value != "" and articulo[1] != "ARTICULOS":
					indice +=1
					var_desc = "desc"+ str(indice)
					lab_desc = "Label(text=articulo[1][0:30],halign = 'left',size_hint=(.4, .3),size_hint_y=None,height=40,)"
					exec(f"self.{var_desc} = {lab_desc}")
					"""self.desc = Label(text=articulo[1][0:30],
								halign = "left", 
								#size = self.texture_size,
								size_hint=(.4, .3),
								size_hint_y=None,
								height=40,
								#text_size = self.size,
								)"""
					var_prec = "prec"+ str(indice)
					lab_prec = "Label(text = articulo[3],size_hint=(.2, .3),size_hint_y=None,height=40,)"
					exec(f"self.{var_prec} = {lab_prec}")
					"""self.precio = Label(text = articulo[3],
								halign = "right", 
								#size = self.texture_size,
								size_hint=(.2, .3),
								size_hint_y=None,
								height=40,
								#text_size = self.size,
								)"""
					var_stock = "stock"+ str(indice)
					lab_stock = "Label(text = articulo[4],size_hint=(.2, .3),size_hint_y=None,height=40,)"
					exec(f"self.{var_stock} = {lab_stock}")
					"""self.stock = Label(text = articulo[4],
								halign = "right", 
								#size = self.texture_size,
								size_hint=(.2, .3),
								size_hint_y=None,
								height=40,
								#text_size = self.size,
								 )"""
					var_cantidad = "cantidad"+str(indice)
					text_cantidad = "TextInput(multiline=False, readonly=False,align='right', font_size=20,size_hint=(.1, .3),input_filter = 'float',write_tab = 'False')"
					exec(f"self.{var_cantidad} = {text_cantidad}")
					"""self.cantidad = TextInput(
							multiline=False, 
							readonly=False, 
							halign="right", 
							font_size=20,
							size_hint=(.1, .3),
							input_filter = "float",
							write_tab = "False",
							)"""

					var_but = "but_agregar"+str(indice)
					but_agregar_inst = f"Button (text = "+",size_hint = (.1, .3),)"
					exec(f"{var_but} = {but_agregar_inst}")
					"""but_agregar = Button (text = "+",
							size_hint = (.1, .3),	
							)"""

					exec(f"{var_but}.bind(on_press=self.agregar_art)")

					"""but_agregar.bind(on_press=self.agregar_art)"""

					exec(f"self.layout.add_widget(self.{var_desc})")
					exec(f"self.layout.add_widget(self.{var_prec})")
					exec(f"self.layout.add_widget(self.{var_stock})")
					exec(f"self.layout.add_widget(self.{var_cantidad})")
					exec(f"self.layout.add_widget({var_but})")

class InfoPage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		# Just one column
		self.cols = 1

		# And one label with bigger font and centered text
		self.message = Label(halign="center", valign="middle", font_size=30)

		# By default every widget returns it's side as [100, 100], it gets finally resized,
		# but we have to listen for size change to get a new one
		# more: https://github.com/kivy/kivy/issues/1044
		self.message.bind(width=self.update_text_width)

		# Add text widget to the layout
		self.add_widget(self.message)

	# Called with a message, to update message text in widget
	def update_info(self, message):
		self.message.text = message

	# Called on label width update, so we can set text width properly - to 90% of label width
	def update_text_width(self, *_):
		self.message.text_size = (self.message.width * 0.9, None)
								
				

if __name__ == '__main__':
	irenic_app = irenicApp()
	irenic_app.run()
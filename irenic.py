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
from kivy.clock import Clock
import csv

list_desc = []

class irenicApp(App):
	def build(self):
		
		# We are going to use screen manager, so we can add multiple screens
		# and switch between them
		self.screen_manager = ScreenManager()

		# Initial, connection screen (we use passed in name to activate screen)
		# First create a page, then a new screen, add page to screen and screen to screen manager
		self.start_page = StartPage()
		screen = Screen(name='Start')
		screen.add_widget(self.start_page)
		self.screen_manager.add_widget(screen)

		self.ventas_page = VentasPage()
		screen = Screen(name='Ventas')
		screen.add_widget(self.ventas_page)
		self.screen_manager.add_widget(screen)

		# Info page
		self.carrito_page = CarritoPage()
		screen = Screen(name='Carrito')
		screen.add_widget(self.carrito_page)
		self.screen_manager.add_widget(screen)


		return self.screen_manager

class StartPage(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"
		lista_botones = ["INGRESOS", "VENTAS", "INFORMES"]
		for idx in range(len(lista_botones)):
			button_start = Button (text = lista_botones[idx])
			button_start.ID = str(idx)
			self.add_widget(button_start)

			button_start.bind(on_press = self.elijo_pantalla)

	def elijo_pantalla(self, instance):

		if instance.text == "INGRESOS":
			#PANTALLA INGRESOS
			return
		elif instance.text == "VENTAS":
			irenic_app.screen_manager.current = 'Ventas'
		else:
			#PANTALLA INFORMES
			return
			

class VentasPage(BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"
			
		#AGREGO LOS WIDGETS QUE VOY A USAR MAS TARDE CUANDO HAGA LA LISTA
		desc = Label(
					halign = "left", 
					#size = self.texture_size,
					size_hint=(.4, .3),
					size_hint_y=None,
					height=40,
					#text_size = self.size,
					)
		precio = Label(
					halign = "right", 
					#size = self.texture_size,
					size_hint=(.2, .3),
					size_hint_y=None,
					height=40,
					#text_size = self.size,
					)
		stock = Label(
					halign = "right", 
					#size = self.texture_size,
					size_hint=(.2, .3),
					size_hint_y=None,
					height=40,
					#text_size = self.size,
					 )
		cantidad = TextInput(
				multiline=False, 
				readonly=False, 
				halign="right", 
				font_size=20,
				size_hint=(.1, .3),
				input_filter = "float",
				write_tab = "False",
				)
		########################################################
		
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

		box_buttons = BoxLayout(size_hint = (1, .2))

		but_vuelvo = Button(text = "Volver",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)
		but_carrito = Button(text = "Carrito",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)

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

		box_buttons.add_widget(but_vuelvo)
		box_buttons.add_widget(but_carrito)
		
		self.add_widget(box_buttons)

		but_vuelvo.bind(on_press=self.vuelvo_start)
		but_carrito.bind(on_press = self.voy_carrito)
		
	
	def voy_carrito(self,instance):
		irenic_app.screen_manager.current = "Carrito"

	def vuelvo_start(self, instance):
		irenic_app.screen_manager.current = "Start"


	def on_text(self, instance, value):
		self.layout.clear_widgets()
		with open("lista de productos total.csv") as f:
			lista = csv.reader(f, delimiter=',')
			self.indice = 0
			self.matrix_art = []
			for articulo in lista:
				if value.lower() in articulo[1].lower() and value != "" and articulo[1] != "ARTICULOS":
					
					self.desc = Label(text=articulo[1][0:30],
								halign = "left", 
								#size = self.texture_size,
								size_hint=(.4, .3),
								size_hint_y=None,
								height=40,
								#text_size = self.size,
								)
					self.precio = Label(text = articulo[3],
								halign = "right", 
								#size = self.texture_size,
								size_hint=(.2, .3),
								size_hint_y=None,
								height=40,
								#text_size = self.size,
								)
					self.stock = Label(text = articulo[4],
								halign = "right", 
								#size = self.texture_size,
								size_hint=(.2, .3),
								size_hint_y=None,
								height=40,
								 )
					self.var_cant = f"self.cantidad{self.indice}"
					asig_text = """TextInput(
							multiline=False, 
							readonly=False, 
							halign="right", 
							font_size=20,
							size_hint=(.1, .3),
							input_filter = "int",
							write_tab = "False",
							)"""
					
					exec("%s = %s" %(self.var_cant,asig_text))
					"""self.cantidad = TextInput(
							multiline=False, 
							readonly=False, 
							halign="right", 
							font_size=20,
							size_hint=(.1, .3),
							input_filter = "float",
							write_tab = "False",
							)"""

					var_but_agregar = """Button (text = "agregar",
							size_hint = (.1, .3),
											)"""

					exec(f"but_agregar{str(self.indice)} = {var_but_agregar}") 
					exec(f"but_agregar{str(self.indice)}.ID = {str(self.indice)}")
					
					
					
					self.matrix_art.append([self.desc.text, self.precio.text])
					exec(f"but_agregar{str(self.indice)}.bind(on_press=self.agregar_art)")

					self.layout.add_widget(self.desc)
					self.layout.add_widget(self.precio)
					self.layout.add_widget(self.stock)
					exec("self.layout.add_widget(%s)" %(self.var_cant))
					exec(f"self.layout.add_widget(but_agregar{str(self.indice)})")
					self.indice +=1	

	def agregar_art(self, instance):
		
		
		descripcion = self.matrix_art[int(instance.ID)][0]
		precio_unit = self.matrix_art[int(instance.ID)][1]
		var_cantidad = f"self.cantidad{instance.ID}.text"
		ldic = locals()
		
		exec(f"cantidad = {var_cantidad}", globals(), ldic)
		cantidad = ldic["cantidad"]

		if cantidad!="" and int(cantidad)>0:

			exec(f"subtotal = int(precio_unit) * int({var_cantidad})", globals(),ldic)
			subtotal = ldic["subtotal"]
			
			info = f"{descripcion} {precio_unit} {cantidad} {subtotal}"
			
			irenic_app.carrito_page.update_info(info)
			irenic_app.screen_manager.current = 'Carrito'
			
		#Clock.schedule_once(self.vuelvo_ventas, 1)	
	
	def vuelvo_ventas(self, instance):
		irenic_app.screen_manager.current = 'Ventas'
		



class CarritoPage(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"
		
		
		self.lab_total = Label(text = "",
							size_hint = (1,.2),
							font_size = 55,
							color = [0,1,0,1],

								)
		self.add_widget(self.lab_total)
		
		#GridLayout
		self.grid_desc = GridLayout(cols = 2,
								#size_hint = (1,.6),
									row_force_default=True, 
									row_default_height=40,
									)
		self.box_buttons = BoxLayout(size_hint = (1, .2))
		# And one label with bigger font and centered text
		self.message = Label(
							#halign="center", 
							font_size=30,
							size_hint = (.2, 1)
							)
		
		
		self.grid_desc.add_widget(self.message)
		

		self.but_vuelvo = Button(text = "Seguir comprando",
								pos_hint={"center_x": 0.5, "center_y": 0.5},
								#size_hint = (.3, .2),
								)
		self.but_vuelvo.bind(on_press=irenic_app.ventas_page.vuelvo_ventas)	

		self.but_pagar = Button(text = "Pagar",
								pos_hint={"center_x": 0.5, "center_y": 0.5},
								#size_hint = (.3, .2),
								)
		self.but_pagar.bind(on_press = self.realizo_pago)
		# By default every widget returns it's side as [100, 100], it gets finally resized,
		# but we have to listen for size change to get a new one
		# more: https://github.com/kivy/kivy/issues/1044
		
		#self.message.bind(width=self.update_text_width)

		# Add text widget to the layout
		self.add_widget(self.grid_desc)
		self.box_buttons.add_widget(self.but_vuelvo)
		self.box_buttons.add_widget(self.but_pagar)
		self.add_widget(self.box_buttons)
		

	# Called with a message, to update message text in widget
	def realizo_pago(self, instance):
		return

	def update_info(self, message):
		

		if len(list_desc)>0:

			for i in range(len(list_desc)):
				if list_desc[i].split()[0:-2] == message.split()[0:-2]:
					list_desc[i] = message
					agrego = False
					break
				else:
					agrego = True
		else:
			agrego = True

		if agrego:
			list_desc.append(message)
					
		
		self.armo_items()
		
	def armo_items(self, suma = 0):
		self.grid_desc.clear_widgets()
		self.lab_total.text = str(suma)

		if len(list_desc)==0:
			carrito_vacio = Label(text="Carrito Vacio",
							size_hint = (1,.2),
								)
			self.grid_desc.add_widget(carrito_vacio)
		
		for msg in list_desc:
			total = msg.split()
			
			var_cada_desc = f"self.cada_desc{str(list_desc.index(msg))}"
			var_lab = """Label(text=msg,
							size_hint = (1,.2),
								)"""
			exec(f"{var_cada_desc} = {var_lab}")
			var_but_elimino = """Button(text = "borrar",
								size_hint = (.1, .3)
								)"""
			exec(f"but_elimino{str(list_desc.index(msg))} = {var_but_elimino}")
			exec(f"self.grid_desc.add_widget({var_cada_desc})")
			exec(f"self.grid_desc.add_widget(but_elimino{str(list_desc.index(msg))})")

			exec(f"but_elimino{str(list_desc.index(msg))}.bind(on_press= self.elimino_item)")
		
			exec(f"but_elimino{str(list_desc.index(msg))}.ID = {str(list_desc.index(msg))}")
			suma += int(total[len(total)-1])
			self.lab_total.text = str(suma)

		#self.message.text = message
		
	def elimino_item(self, instance):

		exec(f"self.grid_desc.remove_widget(self.cada_desc{instance.ID})")
		exec(f"self.grid_desc.remove_widget(instance)")
		
		
		list_desc.remove(list_desc[int(instance.ID)])

		self.armo_items()


	# Called on label width update, so we can set text width properly - to 90% of label width
	def update_text_width(self, *_):
		carrito_page.grid_desc.message.text_size = (carrito_page.grid_desc.message.width * 0.9, None)
								
				

if __name__ == '__main__':
	irenic_app = irenicApp()
	irenic_app.run()
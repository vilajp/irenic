import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup 
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
import csv

list_desc = []
lista = []
lista_pop = []


def cargo_lista_confirmacion(lista_muestro, lista_ing = []):
	lista_ing.append(lista_muestro)
	return lista_ing

def cargo_art():
		with open("lista de productos total.csv") as f:
			copio_lista = csv.reader(f, delimiter=',')
			for cada_art in copio_lista:
				lista.append(cada_art)

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

		self.ingresos_page = IngresosPage()
		screen = Screen(name='Ingresos')
		screen.add_widget(self.ingresos_page)
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

		#CARGO LISTA DE ARTICULOS
		cargo_art()

		self.orientation = "vertical"
		lista_botones = ["INGRESOS", "VENTAS", "INFORMES"]
		for idx in range(len(lista_botones)):
			button_start = Button (text = lista_botones[idx])
			button_start.ID = str(idx)
			self.add_widget(button_start)

			button_start.bind(on_press = self.elijo_pantalla)

	def elijo_pantalla(self, instance):

		if instance.text == "INGRESOS":
			irenic_app.screen_manager.current = 'Ingresos'
		
		elif instance.text == "VENTAS":
			irenic_app.screen_manager.current = 'Ventas'
		else:
			#PANTALLA INFORMES
			return
			
class IngresosPage(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"
		self.spacing = 5

		self.lab_ask = Label(text = "Seleccione Proveedor:", size_hint = (1,.2))

		self.add_widget(self.lab_ask)

		self.grid_botones = BoxLayout(size_hint = (1,.2))

		with open("proveedores.csv") as prov:
			lista_proveedor = csv.reader(prov, delimiter = ",")
			indice = 1
			for proveedor in lista_proveedor:
				if proveedor[0]!= "NOMBRE":
					exec(f"bot_prov{indice} = Button(text = proveedor[0],)")
					exec(f"self.grid_botones.add_widget(bot_prov{indice})")
					exec(f"bot_prov{indice}.bind(on_press= self.articulo_proveedor)")
					exec(f"bot_prov{indice}.ID = indice")
					indice += 1

			exec(f"bot_prov{indice} = Button(text = 'Nuevo Proveedor',)")
			exec(f"self.grid_botones.add_widget(bot_prov{indice})")
			exec(f"bot_prov{indice}.bind(on_press= self.articulo_proveedor)")
			exec(f"bot_prov{indice}.ID = indice")
										
		self.add_widget(self.grid_botones)

		self.box_text_lab = BoxLayout (orientation = "vertical",
										size_hint = (1, .2),
										)
		self.add_widget(self.box_text_lab)

		
		self.grid_tex_art = GridLayout (cols = 4,
										spacing=5, 
										size_hint_y=None,
										)


		self.grid_tex_art.bind(minimum_height=self.grid_tex_art.setter('height'))
		
		rotador = ScrollView(size_hint = (1,1),
							 size=(Window.width, Window.height),)
		rotador.add_widget(self.grid_tex_art)
		self.add_widget(rotador)

	def articulo_proveedor(self, instance):
		#,ARTICULOS,MAYORISTA,MINORISTA,100,proveedor,margen
		self.grid_botones.clear_widgets()
		self.remove_widget(self.lab_ask)
		if instance.text != "Nuevo Proveedor":
			self.lab_prov = Label ( text = instance.text)
			buscador_ing = TextInput(
							text = "",
							multiline=False, 
							readonly=False, 
							halign="left", 
							font_size=30,
							size_hint=(1, 1),
							#input_filter = "float",
							write_tab = "False",
							)
			barra_titulos_ingreso = GridLayout(cols = 4,
												row_force_default=True, 
												row_default_height=40,
												)
			
			tit_desc = Label(text="Descripcion", size_hint=(.5, 1),)
			tit_cant = Label(text="Cantidad", size_hint=(.2, 1),)
			tit_precio = Label(text="Precio", size_hint=(.2, 1),)
			tit_boton = Label(text="", size_hint=(.2,1))
		
			barra_titulos_ingreso.add_widget(tit_desc)
			barra_titulos_ingreso.add_widget(tit_cant)
			barra_titulos_ingreso.add_widget(tit_precio)
			barra_titulos_ingreso.add_widget(tit_boton)
		
			self.grid_botones.add_widget(self.lab_prov)
			self.box_text_lab.add_widget(buscador_ing)
			self.box_text_lab.add_widget(barra_titulos_ingreso)

			buscador_ing.bind(text = self.armo_items_ing)
		else:
			label_ing = Label(text = "Ingrese los datos del Nuevo Proveedor")
			self.box_text_lab.add_widget(label_ing)
			self.box_text_lab.add_widget(barra_titulos_ingreso)


	def armo_items_ing(self, instance, value):
		self.grid_tex_art.clear_widgets()
		
		indice = 0
		self.matrix_art = []
		
		for i in range(len(lista)):
			if value.lower() in lista[i][1].lower() and value != "" and lista[i][5] == self.lab_prov.text:
				var_lab_desc_art="""Label(
							text = lista[i][1][0:30], 
							halign = "left", 
							#size = self.texture_size,
							size_hint=(.5, .3),
							size_hint_y=None,
							height=40,)"""
				
				exec(f"self.lab_desc_art{indice}= {var_lab_desc_art}")
				exec(f"self.grid_tex_art.add_widget(self.lab_desc_art{indice})")

				exec(f"self.text_cant_art{indice}= TextInput(size_hint=(.2,.3))")
				exec(f"self.grid_tex_art.add_widget(self.text_cant_art{indice})")

				exec(f"self.text_precio_art{indice}= TextInput(size_hint=(.2,.3))")
				exec(f"self.grid_tex_art.add_widget(self.text_precio_art{indice})")

				var_bot_art_ing = """Button(
									text = "agregar", 
									size_hint=(.2,.3),
											)"""
				exec(f"bot_art_ing{indice} = {var_bot_art_ing}")
				exec(f"bot_art_ing{indice}.ID = {indice}")
				exec(f"self.grid_tex_art.add_widget(bot_art_ing{indice})")
				exec(f"bot_art_ing{indice}.bind(on_press = self.agrego_art_ing)")
				exec(f"self.matrix_art = cargo_lista_confirmacion([i,self.lab_desc_art{indice}.text, self.text_cant_art{indice}.text, self.text_precio_art{indice}.text],self.matrix_art)")		
				indice = + 1

	def agrego_art_ing(self, instance):
				
		print(instance.ID)
		ing_desc = self.matrix_art[int(instance.ID)][1]
		ing_cant = self.matrix_art[int(instance.ID)][2]
		ing_precio = self.matrix_art[int(instance.ID)][3]

		lista_pop.append([ing_desc, ing_cant, ing_precio])

		layout = GridLayout(cols = 1, spacing = 5) 

		for cada_item in lista_pop:

			itemLabel = Label(text = f"{cada_item} {ing_cant} {ing_precio}",
							size_hint = (.2, 1),
							) 
			closeButton = Button(text = "Actualizar Stock",
								size_hint=(.5,.5),
								) 
	  
			layout.add_widget(itemLabel)
	  
			# Instantiate the modal popup and display 
	
		layout.add_widget(closeButton)        

		self.popup = Popup(title ='UD. INGRESO', 
					  content = layout, 
					  size_hint =(None, None), size =(500, 500))   

		self.popup.open()    
  		# Attach close button press with popup.dismiss action 
		closeButton.bind(on_press = self.actualizo_stock)
			
	def actualizo_stock(self, instance):
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
		
		self.buscador = TextInput(
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

		self.buscador.bind(text = self.on_text)

		box_buttons = BoxLayout(size_hint = (1, .2))

		but_vuelvo = Button(text = "Volver",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)
		but_carrito = Button(text = "Carrito",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)

		self.add_widget(self.buscador)

		
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

		but_vuelvo.bind(on_press = self.vuelvo_start)
		but_carrito.bind(on_press = self.voy_carrito)

		


	
	def voy_carrito(self,instance):
		irenic_app.carrito_page.armo_items()
		irenic_app.screen_manager.current = "Carrito"

	def vuelvo_start(self, instance):
		irenic_app.screen_manager.current = "Start"

		
	def on_text(self, instance, value):
		self.layout.clear_widgets()
		
		self.indice = 0
		self.matrix_art = []
		
		for articulo in lista:
			if value.lower() in articulo[1].lower() and value != "" and articulo[1] != "ARTICULOS" and articulo[3] != "":
				
				art_ind_stock = lista.index(articulo)
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
				
				
				
				#self.matrix_art.append([self.desc.text, self.precio.text, str(art_ind_stock)])
				self.matrix_art = cargo_lista_confirmacion([self.desc.text, self.precio.text, str(art_ind_stock)], self.matrix_art)
				
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
		codigo_art = self.matrix_art[int(instance.ID)][2]
		var_cantidad = f"self.cantidad{instance.ID}.text"
		ldic = locals()
		
		exec(f"cantidad = {var_cantidad}", globals(), ldic)
		cantidad = ldic["cantidad"]

		if cantidad!="" and int(cantidad)>0:

			exec(f"subtotal = int(precio_unit) * int({var_cantidad})", globals(),ldic)
			subtotal = ldic["subtotal"]
			
			info = f"{codigo_art},{descripcion},{precio_unit},{cantidad},{subtotal}"
			
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
		self.but_pagar.bind(on_press = self.pido_confirmacion)
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

	def pido_confirmacion(self, instance):

		if self.lab_total.text != "0":
			layout = GridLayout(cols = 1, padding = 10) 
	  
			askLabel = Label(text = "Confirma compra por:",
							size_hint = (1,.5),
							) 
			totalLabel = Label(text = self.lab_total.text,
								size_hint = (1,1),
								font_size = 55,
								color = [0,1,0,1],
								)
			closeButton = Button(text = "Pagar",
								size_hint=(1,.5),
								) 
	  
			layout.add_widget(askLabel)
			layout.add_widget(totalLabel) 
			layout.add_widget(closeButton)        
	  
			# Instantiate the modal popup and display 
			self.popup = Popup(title ='ATENCION!', 
						  content = layout, 
						  size_hint =(None, None), size =(300, 300))   
			self.popup.open()    
	  
			# Attach close button press with popup.dismiss action 
			closeButton.bind(on_press = self.realizo_pago)
			


	def update_info(self, message):
		

		if len(list_desc)>0:

			for i in range(len(list_desc)):
				if list_desc[i].split(",")[0:-2] == message.split(",")[0:-2]:
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
			total = msg.split(",")
			
			var_cada_desc = f"self.cada_desc{str(list_desc.index(msg))}"
			var_lab = """Label(text=msg.replace(",", " ")[2:],
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
								
	def realizo_pago(self, instance):
		with open("lista venta productos diaria.csv" , mode = "a") as v:
			venta = csv.writer(v, delimiter = "," , lineterminator='\n')
			for item in list_desc:
				now = datetime.now()
				linea = f"{now.date()},{now.time()},{item}"
				venta.writerow(linea.split(','))
				indice = int(item.split(",")[0])
				lista[indice][4] = str(int(lista[indice][4])-int(item.split(",")[-2]))
				
		with open("lista de productos total.csv" , mode = "w") as f:
			articulos = csv.writer(f, delimiter = "," , lineterminator='\n')
			for articulo in lista:
				articulos.writerow(articulo)
		list_desc[:] = []
		self.armo_items()
		irenic_app.ventas_page.layout.clear_widgets()
		irenic_app.ventas_page.buscador.text = ""
		self.popup.dismiss()

			

if __name__ == '__main__':
	irenic_app = irenicApp()
	irenic_app.run()
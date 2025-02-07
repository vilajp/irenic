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
proveedores = []
clientes = []
prov_udtd = False


def cargo_lista_confirmacion(lista_muestro, lista_ing = []):
	lista_ing.append(lista_muestro)
	return lista_ing

def cargo_art():
		with open("lista de productos total.csv") as f:
			copio_lista = csv.reader(f, delimiter=',')
			for cada_art in copio_lista:
				lista.append(cada_art)

def cargo_clientes():
	with open("clientes.csv") as cli:
			lista_clientes = csv.reader(cli, delimiter = ",")
			
			for cliente in lista_clientes:
				clientes.append(cliente)
		

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

		#CARGO LISTA DE ARTICULOS
		
		cargo_art()

		cargo_clientes()

		self.orientation = "vertical"
		lista_botones = ["INGRESOS", "VENTAS", "INFORMES"]
		for idx in range(len(lista_botones)):
			button_start = Button (text = lista_botones[idx])
			button_start.ID = str(idx)
			self.add_widget(button_start)

			button_start.bind(on_press = self.elijo_pantalla)

	def elijo_pantalla(self, instance):
		
		if instance.text.upper() == "INGRESOS":
			irenic_app.ventas_page.ingresos()
		elif instance.text.upper() == "VENTAS":
			irenic_app.ventas_page.seleccion_clientes(instance)
		else:
			irenic_app.ventas_page.informes()

		irenic_app.ventas_page.botones_abajo()
		irenic_app.screen_manager.current = "Ventas"

			

class VentasPage(BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.orientation = "vertical"

		self.layout = GridLayout(cols = 5,
							spacing=5, 
							size_hint_y=None
							)
		self.rotador = ScrollView(
							size_hint=(1, 1), 
							#size=(Window.width, Window.height),
							)
			
	def botones_abajo(self):    
		self.box_buttons = BoxLayout(size_hint = (1,.2))

		self.but_vuelvo = Button(text = "Volver",
								#pos_hint={"center_x": 0.1, "center_y": 0.1},
								height = "50dp",
								size_hint_y = None,
								#size_hint = (1,1),
								)
		but_carrito = Button(text = "Carrito",
								#pos_hint={"center_x": 0.1, "center_y": 0.1},
								#size_hint = (1,1),
								height = "50dp",
								size_hint_y = None,
								)

		self.box_buttons.add_widget(self.but_vuelvo)
		self.box_buttons.add_widget(but_carrito)
		
		self.add_widget(self.box_buttons)

		self.but_vuelvo.bind(on_press = self.vuelvo_start)
		but_carrito.bind(on_press = self.voy_carrito)


###############################################################################
###############################################################################

	def ventas(self, codigo_cliente):
		
		self.codigo_cliente = codigo_cliente.ID
		self.clear_widgets()
		self.rotador.clear_widgets()
		self.layout.cols=5
		self.layout.size_hint_y=None
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
		self.buscador.ID="ventas"
		
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

		self.add_widget(self.buscador)

		
		self.add_widget(titulos)

		
		# Make sure the height is such that there is something to scroll.
		self.layout.bind(minimum_height=self.layout.setter('height'))
		
			
		
		self.rotador.add_widget(self.layout)
		
		self.add_widget(self.rotador)
		
		self.botones_abajo()    


		
	def seleccion_clientes(self, origen):

		
		self.clear_widgets()
		self.rotador.clear_widgets()
		
		self.lab_ask = Label(text = "Seleccione Cliente:", size_hint = (1,.1))

		self.add_widget(self.lab_ask)

		self.grid_botones = BoxLayout(size_hint=(1,.1))

		self.text_busco_cli = TextInput(
							text = "",
							multiline=False, 
							readonly=False, 
							halign="left", 
							font_size=30,
							size_hint=(1,1),
							#input_filter = "float",
							write_tab = "False",
							)

		self.grid_botones.add_widget(self.text_busco_cli)
		self.text_busco_cli.bind(text = self.listo_clientes)
		self.text_busco_cli.ID = f"{origen}"
		self.add_widget(self.grid_botones)
		
		self.rotador = ScrollView()

		self.box_text_lab = BoxLayout (orientation = "vertical",
										size_hint = (1, .2),
										)
		
		self.but_agregar_cliente = Button(text="Nuevo Cliente", 
											size_hint = (1,1),
											)
		self.but_agregar_cliente.bind(on_press=self.nuevo_cliente)
		
		
		self.rotador.add_widget(self.layout)
		
		self.add_widget(self.rotador)
		
		self.box_text_lab.add_widget(self.but_agregar_cliente)

		
		self.add_widget(self.box_text_lab)



	def listo_clientes(self, instance, value):
		
		self.layout.clear_widgets()
		self.layout.cols = 6
		self.layout.size_hint_y= 1
			
		
		
		indice = 0

		if clientes != []:
			for cliente in clientes:

				if cliente[1]!= "NOMBRE" and value.upper() in cliente[1] and value !="":
					self.listado_clientes(cliente, indice, instance)
				indice +=1
					
	def listado_clientes(self, cliente, indice, instance):

		#exec(f"self.lab_codigo_cli{indice} = Label(text=cliente[0],height = '20dp', size_hint_y=None)")     
		exec(f"""self.lab_nombre_cli{indice} = Label(text=cliente[1],
													height = '20dp',
													size_hint_y=None,
													width = '260dp',
													size_hint_x=None,
													)""")
		#exec(f"self.lab_localidad_cli{indice} = Label(text=cliente[2],height = '20dp',size_hint_y=None)")
		exec(f"""self.lab_whatsapp_cli{indice} = Label(text=cliente[3],
													height = '20dp',
													size_hint_y=None,
													width = '100dp',
													size_hint_x=None,
													)""")
		exec(f"""self.lab_instagram_cli{indice} = Label(text=cliente[4],
													height = '20dp',
													size_hint_y=None,
													width = '100dp',
													size_hint_x=None,
													)""")
		exec(f"""self.lab_email_cli{indice} = Label(text=cliente[5],
													height = '20dp',
													size_hint_y=None,
													width = '210dp',
													size_hint_x=None,
													)""")

		self.bot_selec_cliente = Button(
									text="Selec",
									height = "20dp", 
									size_hint_y=None,
									width = '50dp',
									size_hint_x=None,
									)
		
		self.bot_selec_cliente.bind(on_press=self.sigo_con_ventas)
		self.bot_selec_cliente.ID = str(indice)
		
		self.bot_modif_cliente = Button(
									text="Modif",
									height = "20dp",
									size_hint_y=None,
									width = '50dp',
									size_hint_x=None,
									)

		self.bot_modif_cliente.bind(on_press=self.modifico_cliente)
		self.de_donde_vengo = instance.ID
	
		self.bot_modif_cliente.ID = str(clientes.index(cliente))
				
		#exec(f"self.layout.add_widget(self.lab_codigo_cli{indice})")
		exec(f"self.layout.add_widget(self.lab_nombre_cli{indice})")
		#exec(f"self.layout.add_widget(self.lab_localidad_cli{indice})")
		exec(f"self.layout.add_widget(self.lab_whatsapp_cli{indice})")
		exec(f"self.layout.add_widget(self.lab_instagram_cli{indice})")
		exec(f"self.layout.add_widget(self.lab_email_cli{indice})")
										
		self.layout.bind(minimum_height=self.layout.setter('height'))

		self.layout.add_widget(self.bot_selec_cliente)
		self.layout.add_widget(self.bot_modif_cliente)


	def sigo_con_ventas(self, instance):
		
		if "ventasx" in f"{self.de_donde_vengo}":
			irenic_app.ventas_page.informes()
			
		else:
			irenic_app.ventas_page.ventas(instance) 

	def modifico_cliente(self, instance):
		#CODIGO,NOMBRE,LOCALIDAD,WHATSAPP,INSTAGRAM,EMAIL

		self.remove_widget(self.lab_ask)        
		self.box_text_lab.clear_widgets()
		self.grid_botones.clear_widgets()
		self.layout.clear_widgets()
		self.layout.cols = 2
		self.layout.size_hint_y = 1


		label_ing = Label(text = "Modifique los datos del Cliente")
		
		lab_nombre = Label(text= "Nombre")
		self.text_nombre = TextInput(text = f"{clientes[int(instance.ID)][1]}",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_nombre)
		self.layout.add_widget(self.text_nombre)
		
		lab_localidad = Label(text="Localidad")
		self.text_localidad = TextInput(text = f"{clientes[int(instance.ID)][2]}",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_localidad)
		self.layout.add_widget(self.text_localidad)
		
				
		lab_whatsapp = Label(text="Whatsapp")
		self.text_whatsapp = TextInput(text = f"{clientes[int(instance.ID)][3]}",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_whatsapp)
		self.layout.add_widget(self.text_whatsapp)
		
		lab_instagram = Label(text="Instagram/facebook")
		self.text_instagram = TextInput(text = f"{clientes[int(instance.ID)][4]}",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_instagram)
		self.layout.add_widget(self.text_instagram)
		
		lab_email = Label(text="email")
		self.text_email = TextInput(text = f"{clientes[int(instance.ID)][5]}",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_email)
		self.layout.add_widget(self.text_email)
		
		bot_guardar_prov = Button(text="Guardar")
		bot_guardar_prov.ID = f"modifcliente{clientes[int(instance.ID)][0]}"
		bot_guardar_prov.bind(on_press=self.guardo_cliente)
		
		self.grid_botones.add_widget(label_ing)
		
		self.layout.add_widget(bot_guardar_prov)				
		return
	
	def nuevo_cliente(self, instance):
		#CODIGO,NOMBRE,LOCALIDAD,WHATSAPP,INSTAGRAM,EMAIL

		self.remove_widget(self.lab_ask)        
		self.box_text_lab.clear_widgets()
		self.grid_botones.clear_widgets()
		self.layout.clear_widgets()
		self.layout.cols = 2
		self.layout.size_hint_y = 1


		label_ing = Label(text = "Ingrese los datos del Nuevo Cliente")
		
		lab_nombre = Label(text= "Nombre")
		self.text_nombre = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_nombre)
		self.layout.add_widget(self.text_nombre)
		
		lab_localidad = Label(text="Localidad")
		self.text_localidad = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_localidad)
		self.layout.add_widget(self.text_localidad)
		
				
		lab_whatsapp = Label(text="Whatsapp")
		self.text_whatsapp = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_whatsapp)
		self.layout.add_widget(self.text_whatsapp)
		
		lab_instagram = Label(text="Instagram/facebook")
		self.text_instagram = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_instagram)
		self.layout.add_widget(self.text_instagram)
		
		lab_email = Label(text="email")
		self.text_email = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_email)
		self.layout.add_widget(self.text_email)
		
		bot_guardar_prov = Button(text="Guardar")
		bot_guardar_prov.ID = "cliente"
		bot_guardar_prov.bind(on_press=self.guardo_cliente)
		
		self.grid_botones.add_widget(label_ing)
		
		self.layout.add_widget(bot_guardar_prov)
	
##################################################################################
##################################################################################
	def informes(self):
		self.clear_widgets()
		self.box_ventas = GridLayout(
								cols = 1,
								)
		self.box_rankings = GridLayout(
								cols = 1,
								)

		bot_ventas_cli = Button(
								text = "Ventas x Cliente",
								)
		bot_ventas_cli.ID = "ventasxcliente"

		bot_ventas_fecha = Button(
								text = "Ventas x Fecha",
								)
		bot_ventas_fecha.ID = "ventasxfecha"

		bot_ventas_art = Button(
								text = "Ventas x Articulo",
								)
		bot_ventas_art.ID = "ventasxarticulo"
								
		bot_ventas_prov = Button(
								text = "Ventas x Proveedor",
								)
		bot_ventas_prov.ID = "ventasxproveedor"
								
		bot_ventas_cli.bind(on_press=self.proceso_boton_ventas)
		bot_ventas_art.bind(on_press=self.proceso_boton_ventas)
		bot_ventas_prov.bind(on_press=self.proceso_boton_ventas)
		bot_ventas_fecha.bind(on_press=self.proceso_boton_ventas)
		
		self.box_ventas.add_widget(bot_ventas_cli)
		self.box_ventas.add_widget(bot_ventas_fecha)
		self.box_ventas.add_widget(bot_ventas_prov)
		self.box_ventas.add_widget(bot_ventas_art)

		bot_rank_art = Button(
							text= "Ranking x Articulo",
							)
		bot_rank_art.ID = "rankingxarticulo"

		bot_rank_cli = Button(
							text = "Ranking x Cliente",
							)
		bot_rank_cli.ID = "rankingxcliente"

		bot_rank_margen = Button(
							text = "Ranking x Margen",
							)
		bot_rank_margen.ID = "rankingxmargen"

		bot_rank_art.bind(on_press=self.proceso_boton_ventas)
		bot_rank_cli.bind(on_press=self.proceso_boton_ventas)
		bot_rank_margen.bind(on_press=self.proceso_boton_ventas)

		self.box_rankings.add_widget(bot_rank_art)
		self.box_rankings.add_widget(bot_rank_cli)
		self.box_rankings.add_widget(bot_rank_margen)

		self.add_widget(self.box_ventas)
		self.add_widget(self.box_rankings)

	def proceso_boton_ventas(self, instance):
		#ventas x: cliente, articulo, proveedor y fecha
		#ranking: articulo, cliente, margen
		self.box_ventas.clear_widgets()
		self.box_rankings.clear_widgets()

		titulo_listado = Label(
								text = f"{instance.text}",
								height = "40dp",
								size_hint_y = None,
								)
		origen = instance.ID
		self.box_ventas.add_widget(titulo_listado)
		self.seleccion_clientes(origen)
		self.botones_abajo()   



##################################################################################
##################################################################################	
	def ingresos(self):

		self.clear_widgets()

		self.lab_ask = Label(text = "Seleccione Proveedor:", size_hint = (1,.2))

		self.add_widget(self.lab_ask)

		self.grid_botones = BoxLayout(size_hint = (1,.2))

		with open("proveedores.csv") as prov:
			lista_proveedor = csv.reader(prov, delimiter = ",")
			indice = 1
			global prov_udtd
			for proveedor in lista_proveedor:
				if not prov_udtd:
					proveedores.append(proveedor)
				if proveedor[0]!= "NOMBRE":
					exec(f"bot_prov{indice} = Button(text = proveedor[0],)")
					exec(f"self.grid_botones.add_widget(bot_prov{indice})")
					exec(f"bot_prov{indice}.bind(on_press= self.articulo_proveedor)")
					exec(f"bot_prov{indice}.ID = indice")
					indice += 1
			prov_udtd = True

			exec(f"bot_prov{indice} = Button(text = 'Nuevo Proveedor',)")
			exec(f"self.grid_botones.add_widget(bot_prov{indice})")
			exec(f"bot_prov{indice}.bind(on_press= self.articulo_proveedor)")
			exec(f"bot_prov{indice}.ID = indice")
										
		self.add_widget(self.grid_botones)

		self.box_text_lab = BoxLayout (orientation = "vertical",
										size_hint = (1, .2),
										)
		self.add_widget(self.box_text_lab)

		
		self.layout = GridLayout (cols = 4,
										spacing=5, 
										size_hint_y=None,
										)


		self.layout.bind(minimum_height=self.layout.setter('height'))
		
		self.rotador = ScrollView(size_hint = (1,1),
							 size=(Window.width, Window.height),)
		self.rotador.add_widget(self.layout)
		self.add_widget(self.rotador)

	

	def articulo_proveedor(self, instance):
		#,ARTICULOS,MAYORISTA,MINORISTA,100,proveedor,margen
		self.grid_botones.clear_widgets()
		self.remove_widget(self.lab_ask)
		if instance.text != "Nuevo Proveedor":
			self.lab_prov = Label ( text = instance.text)
			self.buscador = TextInput(
							text = "",
							multiline=False, 
							readonly=False, 
							halign="left", 
							font_size=30,
							size_hint=(1, 1),
							#input_filter = "float",
							write_tab = "False",
							)
			self.buscador.ID = "ingresos"
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
			self.box_text_lab.add_widget(self.buscador)
			self.box_text_lab.add_widget(barra_titulos_ingreso)

			self.buscador.bind(text = self.on_text)
		else:
			self.nuevo_proveedor()
	
	def nuevo_proveedor(self):
		#NOMBRE,DIRECCION,LOCALIDAD,TELEFONO,WHATSAPP,CONTACTO1,CONTACTO2

		self.box_text_lab.clear_widgets()
		self.layout.clear_widgets()
		self.layout.cols = 2
		self.layout.size_hint_y = 1


		label_ing = Label(text = "Ingrese los datos del Nuevo Proveedor")
		
		lab_nombre = Label(text= "Nombre")
		self.text_nombre = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_nombre)
		self.layout.add_widget(self.text_nombre)
		
		lab_direccion = Label(text="Direccion")
		self.text_direccion = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
									)
		self.layout.add_widget(lab_direccion)
		self.layout.add_widget(self.text_direccion)
		
		lab_localidad = Label(text="Localidad")
		self.text_localidad = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_localidad)
		self.layout.add_widget(self.text_localidad)
		
		lab_telefono = Label(text="Telefono")
		self.text_telefono = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_telefono)
		self.layout.add_widget(self.text_telefono)
		
		lab_whatsapp = Label(text="Whatsapp")
		self.text_whatsapp = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_whatsapp)
		self.layout.add_widget(self.text_whatsapp)
		
		lab_contacto = Label(text="Nombre de Contacto")
		self.text_contacto = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_contacto)
		self.layout.add_widget(self.text_contacto)
		
		lab_contacto2 = Label(text="Nombre de Contacto 2")
		self.text_contacto2 = TextInput(text = "",
							multiline=False, 
							readonly=False, 
							halign="left",
							size_hint=(1, .2),
							#input_filter = "float",
							write_tab = "False",
								)
		self.layout.add_widget(lab_contacto2)
		self.layout.add_widget(self.text_contacto2)
		
		bot_guardar_prov = Button(text="Guardar")
		bot_guardar_prov.ID = "proveedor"
		bot_guardar_prov.bind(on_press=self.guardo_proveedor)
		
		self.grid_botones.add_widget(label_ing)
		
		self.layout.add_widget(bot_guardar_prov)

				
	def guardo_proveedor(self, instance):
		self.registro_prov = f"{self.text_nombre.text.upper()},{self.text_direccion.text.upper()},{self.text_localidad.text.upper()},{self.text_telefono.text},{self.text_whatsapp.text},{self.text_contacto.text.upper()},{self.text_contacto2.text.upper()}"
		proveedores.append(self.registro_prov.split(","))
		with open("proveedores.csv", mode = "w") as prov:
			lista_proveedor = csv.writer(prov, delimiter = ",", lineterminator='\n')
			for proveedor in proveedores:       
				lista_proveedor.writerow(proveedor)

		irenic_app.ventas_page.ingresos()
		irenic_app.ventas_page.botones_abajo()
	
	
				
	def guardo_cliente(self, instance):
		if instance.ID == "cliente":
			nro_codigo_cliente = int(clientes[len(clientes)-1][0])+1
			codigo_cliente = "0" * (7 - len(str(nro_codigo_cliente))) + str(nro_codigo_cliente)
			self.registro_cli = f"{codigo_cliente},{self.text_nombre.text.upper()},{self.text_localidad.text.upper()},{self.text_whatsapp.text},{self.text_instagram.text.upper()},{self.text_email.text.lower()}"
			clientes.append(self.registro_cli.split(","))
		else:
			self.registro_cli = f"{instance.ID[12:]},{self.text_nombre.text.upper()},{self.text_localidad.text.upper()},{self.text_whatsapp.text},{self.text_instagram.text.upper()},{self.text_email.text.lower()}"		
			clientes[int(instance.ID[12:])] = self.registro_cli.split(",")

		with open("clientes.csv", mode = "w") as cli:
			lista_clientes = csv.writer(cli, delimiter = ",", lineterminator='\n')
			for cliente in clientes:        
				lista_clientes.writerow(cliente)

		irenic_app.ventas_page.seleccion_clientes()
		irenic_app.ventas_page.botones_abajo()


	def guardo_proveedor(self, instance):
		self.registro_prov = f"{self.text_nombre.text.upper()},{self.text_direccion.text.upper()},{self.text_localidad.text.upper()},{self.text_telefono.text},{self.text_whatsapp.text},{self.text_contacto.text.upper()},{self.text_contacto2.text.upper()}"
		proveedores.append(self.registro_prov.split(","))
		with open("proveedores.csv", mode = "w") as prov:
			lista_proveedor = csv.writer(prov, delimiter = ",", lineterminator='\n')
			for proveedor in proveedores:       
				lista_proveedor.writerow(proveedor)

		irenic_app.ventas_page.ingresos()
		irenic_app.ventas_page.botones_abajo()
		
	
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
			if instance.ID == "ingresos":
				if value.lower() in articulo[1].lower() and value != "" and articulo[1] != "ARTICULOS" and articulo[3] != "" and articulo[5]==self.lab_prov.text:
					self.on_text_ingresos(articulo)
					self.indice +=1 
					
			elif instance.ID == "ventas":       
				if value.lower() in articulo[1].lower() and value != "" and articulo[1] != "ARTICULOS" and articulo[3] != "":
					self.on_text_ventas(articulo)
					self.indice +=1 

					
	
	def on_text_ventas(self, articulo):
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
		
		if len(str(self.indice))== 1:
			cod_id = f"00{self.indice}"
		elif len(str(self.indice)) == 2:
			cod_id = f"0{self.indice}"
		elif len(str(self.indice)) == 3:
			cod_id = str(self.indice)
		
		exec(f"but_agregar{str(self.indice)}.ID = 'ventas  {cod_id}'")
		
		
		
		#self.matrix_art.append([self.desc.text, self.precio.text, str(art_ind_stock)])
		self.matrix_art = cargo_lista_confirmacion([self.desc.text, self.precio.text, str(art_ind_stock), self.codigo_cliente], self.matrix_art)
		
		exec(f"but_agregar{str(self.indice)}.bind(on_press=self.agregar_art)")

		self.layout.add_widget(self.desc)
		self.layout.add_widget(self.precio)
		self.layout.add_widget(self.stock)
		exec("self.layout.add_widget(%s)" %(self.var_cant))
		exec(f"self.layout.add_widget(but_agregar{str(self.indice)})")

					
	def on_text_ingresos(self, articulo):
		var_lab_desc_art="""Label(
					text = lista[lista.index(articulo)][1][0:30], 
					halign = "left", 
					#size = self.texture_size,
					size_hint=(.5, .3),
					size_hint_y=None,
					height=40,)"""
		
		exec(f"self.lab_desc_art{self.indice}= {var_lab_desc_art}")
		exec(f"self.layout.add_widget(self.lab_desc_art{self.indice})")

		exec(f"self.text_cant_art{self.indice}= TextInput(size_hint=(.2,.3))")
		exec(f"self.layout.add_widget(self.text_cant_art{self.indice})")

		exec(f"self.text_precio_art{self.indice}= TextInput(size_hint=(.2,.3))")
		exec(f"self.layout.add_widget(self.text_precio_art{self.indice})")

		var_bot_art_ing = """Button(
							text = "agregar", 
							size_hint=(.2,.3),
									)"""
		exec(f"bot_art_ing{self.indice} = {var_bot_art_ing}")
		if len(str(self.indice))== 1:
			cod_id = f"00{self.indice}"
		elif len(str(self.indice)) == 2:
			cod_id = f"0{self.indice}"
		elif len(str(self.indice)) == 3:
			cod_id = str(self.indice)
		exec(f"bot_art_ing{self.indice}.ID = 'ingresos{cod_id}'")
		exec(f"self.layout.add_widget(bot_art_ing{self.indice})")
		exec(f"bot_art_ing{self.indice}.bind(on_press = self.agregar_art)")
		exec(f"self.matrix_art = cargo_lista_confirmacion([lista.index(articulo),self.lab_desc_art{self.indice}.text], self.matrix_art)")
	

	def agregar_art(self, instance):
		ldic = locals() 
		exec(f"info = self.agregar_art_{instance.ID[0:8].strip()}(instance)", globals(), ldic)
		info = ldic["info"]
		
		if info:
			irenic_app.carrito_page.update_info(info)
			irenic_app.screen_manager.current = 'Carrito'
			

	def agregar_art_ventas(self, instance): 
		descripcion = self.matrix_art[int(instance.ID[-3:])][0]
		precio_unit = self.matrix_art[int(instance.ID[-3:])][1]
		codigo_art = self.matrix_art[int(instance.ID[-3:])][2]
		codigo_cli = self.matrix_art[int(instance.ID[-3:])][3]
		var_cantidad = f"self.cantidad{int(instance.ID[-3:])}.text"
		
		ldic = locals()
		
		exec(f"cantidad = {var_cantidad}", globals(), ldic)
		cantidad = ldic["cantidad"]
		info = ""
		if cantidad!="" and int(cantidad)>0:
			exec(f"subtotal = int(precio_unit) * int({var_cantidad})", globals(),ldic)
			subtotal = ldic["subtotal"]
			
			exec(f"info = '{instance.ID[0:8].strip()},{codigo_cli},{codigo_art},#{descripcion},{precio_unit},{cantidad},{subtotal}'")
			info = ldic["info"]
		return info

	def agregar_art_ingresos(self, instance):

			
		ing_cod = self.matrix_art[int(instance.ID[-3:])][0]
		ing_desc = self.matrix_art[int(instance.ID[-3:])][1]

		ldic = locals()
		exec(f"ing_cant = self.text_cant_art{int(instance.ID[-3:])}.text", globals(), ldic)
		ing_cant = ldic["ing_cant"]
		
		exec(f"ing_precio = self.text_precio_art{int(instance.ID[-3:])}.text")
		ing_precio = ldic["ing_precio"]

		info = ""
		
		if ing_cant != "" and ing_precio!= "":
			exec(f"info = '{instance.ID[0:8].strip()},{ing_cod},#{ing_desc},{ing_cant},{ing_precio}'")  
			info = ldic["info"]
		return info

			
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
		
		but_vuelvo = Button(text = "Vuelvo",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)
		but_pagar = Button(text = "Termino",
							pos_hint={"center_x": 0.5, "center_y": 0.5},
							#size_hint = (.3, .2),
							)
			

		but_vuelvo.bind(on_press=irenic_app.ventas_page.vuelvo_ventas)  
		but_pagar.bind(on_press = self.pido_confirmacion)

		self.box_buttons.add_widget(but_vuelvo)
		self.box_buttons.add_widget(but_pagar)
		
		# By default every widget returns it's side as [100, 100], it gets finally resized,
		# but we have to listen for size change to get a new one
		# more: https://github.com/kivy/kivy/issues/1044
		
		#self.message.bind(width=self.update_text_width)

		# Add text widget to the layout
		self.add_widget(self.grid_desc)
		self.add_widget(self.box_buttons)
		

	# Called with a message, to update message text in widget

	def pido_confirmacion(self, instance):

		if self.lab_total.text != "0":
			layout = GridLayout(cols = 1, padding = 10) 
	  
			askLabel = Label(text = "Confirma?:",
							size_hint = (1,.5),
							) 
			totalLabel = Label(text = self.lab_total.text,
								size_hint = (1,1),
								font_size = 55,
								color = [0,1,0,1],
								)
			closeButton = Button(text = "OK",
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

		if len(list_desc) > 0:

			for i in range(len(list_desc)):
				if list_desc[i].split(",")[3][0:-2] == message.split(",")[3][0:-2]:
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
			var_lab = """Label(text=msg.replace(",", " ")[msg.index('#')+1:],
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
			if total[0].strip() == "ventas":
				suma += int(total[len(total)-1])
			elif total[0].strip() == "ingresos":
				suma += 1
			
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
		if list_desc[0].split(",")[0]=="ventas":

			with open("lista venta productos diaria.csv" , mode = "a") as v:
				venta = csv.writer(v, delimiter = "," , lineterminator='\n')
				for item in list_desc:
					now = datetime.now()
					linea = f"{now.date()},{now.time()},{item}"
					venta.writerow(linea.split(','))
					indice = int(item.split(",")[2])
					lista[indice][4] = str(int(lista[indice][4])-int(item.split(",")[-2]))
					
		elif list_desc[0].split(",")[0]=="ingresos":
			with open("lista ingresos productos diaria.csv" , mode = "a") as v:
				ingresos = csv.writer(v, delimiter = "," , lineterminator='\n')
				for item in list_desc:
					now = datetime.now()
					linea = f"{now.date()},{now.time()},{item}"
					ingresos.writerow(linea.split(','))
					indice = int(item.split(",")[1])
					lista[indice][4] = str(int(lista[indice][4])+int(item.split(",")[-2]))
			
		
		with open("lista de productos total.csv" , mode = "w") as f:
			articulos = csv.writer(f, delimiter = "," , lineterminator='\n')
			for articulo in lista:
				articulos.writerow(articulo)
		
		instance.text = list_desc[0].split(",")[0]
		list_desc[:] = []
		
		self.popup.dismiss()

		exec(f"irenic_app.start_page.elijo_pantalla(instance)")
			

if __name__ == '__main__':
	irenic_app = irenicApp()
	irenic_app.run()
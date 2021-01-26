import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class MyTextInput(TextInput):
	def on_parent(self, widget, parent):
		self.focus = True
		self.multiline=False
		self.readonly=False
		self.halign="left"
		self.font_size=55
		self.size_hint=(.7,.5)
		self.input_filter = "float"
		self.write_tab = "False"
		self.use_handles = "True"


class NoSaveApp(App):
	icon = 'no-save-512x512.png'
	def build(self):
		hlayout = GridLayout(
							cols = 2, 
							row_force_default=True, 
							row_default_height=70,
							)
		main_layout = BoxLayout(
							orientation="vertical",
							padding = 10, 
							#spacing = 10,
							)
		self.quehago= Label(
						text ="Enter Phone number:",
						size_hint = (.3,.5),
						font_size = "24sp",
						)
		hlayout.add_widget(self.quehago)

		self.numtel = MyTextInput()
		hlayout.add_widget(self.numtel)
		
		main_layout.add_widget(hlayout)

		button = Button(
                    #text= "[size=55sp]NO SAVE![/size]", markup = True,
					text= "NO SAVE!",
                    font_size = "55sp",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint=(.5,.5),
                    
               		)
		main_layout.add_widget(button)

		hlayoutabajo = GridLayout(
							cols = 2, 
							row_force_default=True, 
							row_default_height=60,
							)

		self.rotulo = Label (
							text = "Last Number",
							font_size = "55sp",
							size_hint=(1,.5),
							)
		hlayoutabajo.add_widget(self.rotulo)

		button2 = Button(
                    #text= "[size=55sp]NO SAVE![/size]", markup = True,
					text= "Re-use",
                    font_size = "30sp",
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint=(.2,.5),
                    
             )
		hlayoutabajo.add_widget(button2)

		
		main_layout.add_widget(hlayoutabajo)

		button2.bind(on_press=self.on_button2_press)
		

		button.bind(on_press=self.on_button_press)

		return main_layout

	def on_button_press(self, instance):
		numtel = self.numtel.text
		urlwhats = numtel.join(
								["https://api.whatsapp.com/send?phone=",
								"&text=&source=&data=&app_absent="]
		)
		webbrowser.open(urlwhats)
		self.numtel.text = ""
		self.rotulo.text = numtel
		

	def on_button2_press(self, instance):
		if self.rotulo.text != "Last Number":
			self.numtel.text = self.rotulo.text
		
		

if __name__ == "__main__":
    app = NoSaveApp()
    app.run()
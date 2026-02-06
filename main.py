import json
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.clipboard import Clipboard


class HomeScreen(Screen):
    categorias = ListProperty([])
    busca = StringProperty("")


class CodeScreen(Screen):
    titulo = StringProperty("")
    codigo = StringProperty("")


class Manager(ScreenManager):
    pass


class CodePocketApp(App):
    def build(self):
        self.data = json.load(open("code_data.json", "r", encoding="utf-8"))
        self.sm = Builder.load_file("code.kv")
        self.home = self.sm.get_screen("home")
        self.load_buttons()
        return self.sm

    def load_buttons(self):
        grid = self.home.ids.grid
        grid.clear_widgets()

        for cat in self.data["categorias"]:
            # categoria
            grid.add_widget(
                Builder.load_string(
                    f"""
Label:
    text: "[b]{cat['nome']}[/b]"
    markup: True
    size_hint_y: None
    height: "30dp"
"""
                )
            )

            for item in cat["items"]:
                if self.home.busca.strip().lower() not in item["titulo"].lower():
                    continue

                # ESCAPANDO O TEXTO COM json.dumps()
                titulo = json.dumps(item['titulo'])
                codigo = json.dumps(item['codigo'])

                btn = Builder.load_string(
                    f"""
Button:
    text: {titulo}
    size_hint_y: None
    height: "45dp"
    on_release:
        app.open_code({titulo}, {codigo})
"""
                )
                grid.add_widget(btn)

    def open_code(self, titulo, codigo):
        code_screen = self.sm.get_screen("code")
        code_screen.titulo = titulo
        code_screen.codigo = codigo
        self.sm.current = "code"


if __name__ == "__main__":
    CodePocketApp().run()

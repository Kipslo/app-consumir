import flet as ft
import socket
class app():
    def __init__(self):
        ft.app(target=self.main)
    def sendstr(self, data):
        self.PORT = 55261
        self.HOST = "26.108.30.186"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.sendall(str.encode(data))
        data = self.s.recv(1024)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        return data.decode()
    
    def main(self, page: ft.Page):
        def initpage(event = 0):
            def commandpage(number):
                pass
            page.scroll = "always"
            page.clean()
            limitcommands = (self.sendstr("LIMITCOMMANDS"))
            print(limitcommands)
            opencommands = self.sendstr("OPENCOMMANDS")
            opencommands = opencommands.split(",")
            print(opencommands)


            head = ft.Row([ft.TextButton(text="Recarregar", on_click=initpage, width=150, height=75)], width=150, alignment="top-center")
            commands = ft.Row(wrap=True)
            for i in range(int(limitcommands)):
                if str(i + 1) in opencommands:
                    commands.controls.append(ft.ElevatedButton(text=str(i + 1), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.RED, width=100,height=50))
                else:
                    commands.controls.append(ft.ElevatedButton(text=str(i + 1), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.GREEN, width=100,height=50))
            main = ft.Column([head, commands], horizontal_alignment="center")
            page.add(main)

        def login(event):
            data = ""
            data = self.sendstr("LOGIN," + self.entry_name.value + "," + self.entry_password.value)
            data = data
            print(data)
            if data == "YES":
                self.name, self.password = self.entry_name.value, self.entry_password.value
                initpage()
            elif data == "NOT":
                self.errorlogintext.value = "NOME E/OU SENHA INCORRETOS"
                self.errorlogintext.update()
        
        
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"

        page.title = "APP"

        self.entry_name = ft.TextField(label="NOME", width=350)

        self.entry_password = ft.TextField(label="SENHA", width=350)

        self.errorlogintext = ft.Text(value="", width=350, height=50, size=22)

        conteiner = ft.Container(content=ft.Column([ft.Container(width=500, height=100), self.entry_name, self.entry_password, ft.ElevatedButton("LOGIN", width=350, height=50, on_click=login), self.errorlogintext], horizontal_alignment= "center"), width=500, height=500, bgcolor=ft.colors.BLACK12)
        


        loginarea = ft.Column([conteiner], horizontal_alignment="center")

        page.add(loginarea)
app()
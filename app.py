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
                page.clean()
                page.scroll = "always"
                page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(number)) ,actions=[ft.ElevatedButton(text="Voltar", on_click=initpage)])
                
                products = self.sendstr("PRODUCTS," + str(number))
                print(products)
                products = products.split(",")
                print(products)
                for k, i in enumerate(products):
                    products[k] = i.split("|")
                print(products)
                for i in products:
                    page.add(ft.Row(ft.Container(content=(), height=49, alignment="center"), height=50))
            page.appbar = ft.AppBar(bgcolor="#efefef", actions=[ft.ElevatedButton(text="Recarregar", on_click=initpage)])
            page.clean()
            page.scroll = "always"
            limitcommands = (self.sendstr("LIMITCOMMANDS"))
            opencommands = self.sendstr("OPENCOMMANDS")
            opencommands = opencommands.split(",")

            commands = ft.Row(wrap=True)
            for i in range(int(limitcommands)):
                n = i + 1
                if str(n) in opencommands:
                    commands.controls.append(ft.ElevatedButton(text=str(n), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.RED_700, width=100,height=50))
                else:
                    commands.controls.append(ft.ElevatedButton(text=str(n), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.GREEN, width=100,height=50))
            main = ft.Column([commands], horizontal_alignment="center")
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
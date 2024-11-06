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
                def reviewpage(event):
                    pass
                self.number = number
                def categorypage(category):
                    def addproductlist(product):
                        self.products.append([product, category])
                    def sizepage(product):
                        sizes = self.sendstr(f"SIZESCATEGORY,{product},{category}")
                        page.clean()
                        sizes = sizes.split(",")
                        for k, i in enumerate(sizes):
                            sizes[k] = i.split("|")
                        page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = category:categorypage(y)), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                        sizesbutton = ft.Row(wrap=True, spacing=10)
                        for i in sizes:
                            sizesbutton.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}

                            {i[1]}""", width=150, height=75, on_click=lambda x, y = product + f" ({i[0]})":addproductlist(y)), bgcolor=ft.colors.BLACK12, width=150, height=75))

                        page.add(sizesbutton)   
                    productscategory = self.sendstr(f"PRODUCTSCATEGORY,{category}")
                    page.clean()
                    productscategory = productscategory.split(",")
                    vcategorypage = ft.Row(wrap=True, spacing=10)
                    for k, i in enumerate(productscategory):
                        productscategory[k] = i.split("|")
                    for i in productscategory:
                        if i[1] != "SIZE":
                            vcategorypage.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}

                            {i[2]}""", width=150, height=75, on_click=lambda x, y = i[0]:addproductlist(y)), bgcolor=ft.colors.BLACK12, width=150, height=75))
                        else:
                            vcategorypage.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}
                            
                            """, width=150, height=75, on_click=lambda x, y = i[0]: sizepage(y)), bgcolor=ft.colors.BLACK12, width=150, height=75))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))                        
                    page.add(vcategorypage)
                def addpage(event):
                    pdt = self.sendstr("CATEGORIES")
                    page.clean()
                    self.products = []
                    pdt = pdt.split(",")
                    vaddpage = ft.Row(wrap=True, spacing=10)
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.number)))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = self.number:(commandpage(y))), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                    for i in pdt:
                        vaddpage.controls.append(ft.Container(content=ft.CupertinoButton(i, width=150, height=75, on_click=lambda x, y = i:categorypage(y)), width=150, height=75, bgcolor=ft.colors.BLACK12))
                    page.add(vaddpage)
                page.scroll = "always"
                page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.number)) ,actions=[ft.ElevatedButton(text="Voltar", on_click=initpage)])
                
                products = self.sendstr("PRODUCTSON," + str(self.number))
                page.clean()
                products = products.split(",")
                for k, i in enumerate(products):
                    products[k] = i.split("|")
                column = ft.Column(spacing=2)
                column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text("PRODUTO"), expand=True), ft.Container(ft.Text("QUANTIDADE", text_align="center"), width=100), ft.Container(ft.Text("PREÇO", text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor=ft.colors.BLACK12, height=60, expand=True)]))
                if products != [[""]]:
                    total = 0.0
                    for i in products:
                        column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text(i[0]), expand=True), ft.Container(ft.Text(i[1], text_align="center"), width=100), ft.Container(ft.Text(i[2], text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor=ft.colors.BLACK12, height=60, expand=True)]))
                        total = total + float(i[2])
                    column.controls.append(ft.Row(controls=[ft.Container(content=ft.Row(controls=[ft.Container(width=10, height=49), ft.Container(ft.Text("TOTAL:"), expand=True), ft.Container(width=100), ft.Container(ft.Text(total, text_align="center"), width=50), ft.Container(width=5, height=49)]), bgcolor=ft.colors.BLACK12, height=60, expand=True)]))
                page.bottom_appbar = ft.BottomAppBar(bgcolor=ft.colors.BLACK12, content=ft.Row(controls=[ft.ElevatedButton("ADICIONAR", on_click=addpage)]))
                page.add(column)
            page.appbar = ft.AppBar(bgcolor="#efefef", actions=[ft.ElevatedButton(text="Recarregar", on_click=initpage)])
            page.scroll = "always"
            limitcommands = (self.sendstr("LIMITCOMMANDS"))
            opencommands = self.sendstr("OPENCOMMANDS")
            page.clean()
            opencommands = opencommands.split(",")
            commands = ft.Row(wrap=True)
            for i in range(int(limitcommands)):
                n = i + 1
                if str(n) in opencommands:
                    commands.controls.append(ft.ElevatedButton(text=str(n), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.RED_700, width=100,height=50))
                else:
                    commands.controls.append(ft.ElevatedButton(text=str(n), on_click=lambda y, x = i + 1: commandpage(x), color=ft.colors.BLACK, bgcolor=ft.colors.GREEN, width=100,height=50))
            main = ft.Column([commands], horizontal_alignment="center")
            page.bottom_appbar = None
            page.add(main)

        def login(event):
            data = ""
            data = self.sendstr("LOGIN," + self.entry_name.value + "," + self.entry_password.value)
            data = data
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
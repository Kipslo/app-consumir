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
        data = self.s.recv(2024)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()
        return data.decode()
    
    def main(self, page: ft.Page):
        def initpage(event = 0):
            def commandpage(number):
                self.command = number
                def reviewpage(event = 0):
                    def send():
                        tem = ""
                        for i in self.products:
                            name, category, unitprice, qtd, texts, tipe = i
                            print(tipe)
                            data = f"INSERT,={self.command},={self.name},={self.password},="
                            if texts == "":
                                data = data + f"{name}.-{category}.-{unitprice}.-{qtd}.-{tipe}"
                            else:
                                data = data + f"{name}.-{category}.-{unitprice}.-{qtd}"
                                n = 0
                                for j in texts:
                                    if n == 0:
                                        data = data + f".-{j}"
                                        n = 1
                                    else:
                                        data = data + f".={j}"
                                data = data + f".-{tipe}"
                                
                        
                            print(data)
                            t = self.sendstr(data)
                            if t != "Y":
                                tem = t
                        del t
                        if tem == "":
                            alert = ft.Banner(bgcolor=ft.colors.RED_300, content=ft.Text("PEDIDO ENVIADO COM SUCESSO", color=ft.colors.BLACK), actions=[ft.TextButton("OK", on_click=lambda x:page.close(alert))])
                        page.open(alert)
                        initpage()
                    def editt(i):
                        self.text = []
                        edit(i)
                    def edit(i):
                        def addtext(event):
                            print(entry.value)
                            temp = entry.value
                            self.text.append(temp)
                            print(self.text)
                            edit(i)
                        def confirm(event):
                            for j in self.text:
                                self.products[i][4].append(j)
                            reviewpage()
                        page.clean()
                        page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("CANCELAR", on_click=reviewpage), ft.Container(expand=True), ft.ElevatedButton("CONFIRMAR", on_click=confirm)]))
                        page.appbar = ft.AppBar()
                        
                        page.add(ft.Row(controls=[ft.Container(ft.Row(controls=[ft.Container(width=10), ft.Container(content=ft.Text(self.products[i][0]), expand=True), ft.Container(content=ft.Text(self.products[i][1]), width=100), ft.Container(ft.Text(self.products[i][2]), width=50)]), expand=True, bgcolor=ft.colors.BLACK12, height=50)]))

                        entry = ft.TextField(expand=True, height=50)
                        buttonadd = ft.CupertinoFilledButton(on_click=addtext, width=75, height=50, text="Add")

                        for j in self.products[i][4]:
                            print(j)
                            page.add(ft.Row(height=5))
                            page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Container(ft.Text(j))]), expand=True, bgcolor=ft.colors.BLACK12)], height=50))
                    
                        for j in self.text:
                            print(j)
                            page.add(ft.Row(height=5))
                            page.add(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(width=10), ft.Container(ft.Text(j))]), expand=True, bgcolor=ft.colors.BLACK12)], height=50))

                        page.add(ft.Row(height=10))
                        page.add(ft.Row(controls=[entry, buttonadd]))

                    def add1(i):
                        self.products[i][3] = self.products[i][3] + 1
                        reviewpage()
                    def remove1(i):
                        if self.products[i][3] > 1:
                            self.products[i][3] = self.products[i][3] - 1
                        reviewpage()
                    def delete(i):
                        del self.products[i]
                        reviewpage()
                    page.clean()
                    rows = []
                    page.spacing = 0
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("Comanda " + str(self.command)))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("ENVIAR", on_click=lambda x:send())]))
                    print(self.products)
                    rows.append(ft.Row(controls=[ft.Container(content=ft.Row([ft.Container(expand=True, width=100, height=49, content=ft.Text("PRODUTO", text_align="center")), ft.Container(expand=True, width=100, height=49, content=ft.Text("CATEGORIA", text_align="center")), ft.Container(expand=True, width=30, height=49, content=ft.Text("QTD.", text_align="center"))]), bgcolor=ft.colors.BLACK12, height=50, expand=True)]))
                    
                    rows.append(ft.Row(height=8))
                    for k, i in enumerate(self.products):
                        rows.append(ft.Row(height=50, controls=[ft.Container(content=ft.Row([ft.Container(width=100, height=50, content=ft.Text(i[0], text_align="center")), ft.Container(expand=True, width=100, height=49, content=ft.Text(i[1], text_align="center")), ft.Container(expand=True, width=30, height=49, content=ft.Text(i[3], text_align="center"))]), bgcolor=ft.colors.BLACK12, height=50, expand=True)]))

                        rows.append(ft.Row(height=50, controls=[ft.Container(content=ft.Row(controls=[ft.Container(content=ft.CupertinoButton(text="-1", on_click=lambda x, y = k:remove1(y)), expand=True), ft.Container(content=ft.CupertinoButton("+1", on_click=lambda x, y = k:add1(y)), expand=True), ft.Container(content=ft.CupertinoButton("EDITAR", on_click=lambda x, y = k:editt(y)), expand=True), ft.Container(content=ft.CupertinoButton("EXCLUIR", on_click=lambda x, y = k:delete(y)), expand=True)], height=50), height=50, bgcolor=ft.colors.BLACK12, expand=True)]))

                        rows.append(ft.Row(height=5))

                    for i in rows:
                        page.add(i)
                def categorypage(category):
                    self.category = category
                    productscategory = self.sendstr(f"PRODUCTSCATEGORY,={category}")
                    page.clean()
                    productscategory = productscategory.split(",=")
                    vcategorypage = ft.Row(wrap=True, spacing=10)
                    for k, i in enumerate(productscategory):
                        productscategory[k] = i.split("|")
                    if productscategory[0][0] != '':
                        for i in productscategory:
                            if i[1] != "SIZE":
                                vcategorypage.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}

                                {i[2]}""", width=150, height=75, on_click=lambda x, y = i[0], z = i[2], a = i[1]:addproductlist(y, z, a)), bgcolor=ft.colors.BLACK12, width=150, height=75))
                            else: 
                                vcategorypage.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}
                            
                                """, width=150, height=75, on_click=lambda x, y = i[0]: sizepage(y)), bgcolor=ft.colors.BLACK12, width=150, height=75))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=addpage), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))                        
                    page.add(vcategorypage)    
                def addproductlist(product, unitprice, tipe):
                    self.products.append([product, self.category, unitprice, 1, [], tipe])
                def addpage(event):
                    pdt = self.sendstr("CATEGORIES")
                    page.clean()
                    pdt = pdt.split(",=")
                    vaddpage = ft.Row(wrap=True, spacing=10)
                    page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.command)))
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = self.command:(commandpage(y))), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                    for i in pdt:
                        vaddpage.controls.append(ft.Container(content=ft.CupertinoButton(i, width=150, height=75, on_click=lambda x, y = i:categorypage(y)), width=150, height=75, bgcolor=ft.colors.BLACK12))
                    page.add(vaddpage)
                def sizepage(product):
                    sizes = self.sendstr(f"SIZESCATEGORY,={product},={self.category}")
                    page.clean()
                    sizes = sizes.split(",=")
                    for k, i in enumerate(sizes):
                        sizes[k] = i.split("|")
                    page.bottom_appbar = ft.BottomAppBar(content=ft.Row(controls=[ft.ElevatedButton("VOLTAR", on_click=lambda x, y = self.category:categorypage(y)), ft.Container(expand=True), ft.ElevatedButton("REVISAR", on_click=reviewpage)]))
                    sizesbutton = ft.Row(wrap=True, spacing=10)
                    for i in sizes:
                        sizesbutton.controls.append(ft.Container(content=ft.TextButton(text=f"""{i[0]}
                        
                        {i[1]}""", width=150, height=75, on_click=lambda x, y = product + f" ({i[0]})", z = i[1], a = "SIZE":addproductlist(y, z, a)), bgcolor=ft.colors.BLACK12, width=150, height=75))

                    page.add(sizesbutton)
                page.scroll = "always"
                self.products = []
                page.appbar = ft.AppBar(bgcolor="#efefef", title=ft.Text("COMANDA " + str(self.command)) ,actions=[ft.ElevatedButton(text="Voltar", on_click=initpage)])
                
                products = self.sendstr("PRODUCTSON,=" + str(self.command))
                page.clean()
                products = products.split(",=")
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
            opencommands = opencommands.split(",=")
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
            data = self.sendstr("LOGIN,=" + self.entry_name.value + ",=" + self.entry_password.value)
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
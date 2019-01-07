from bs4 import BeautifulSoup
import requests
import re

PAGE_LINK = "http://www.softexrecife.org.br/agenda/"

class Eventos():
    def __init__(self,lista=[]):
        self.lista = lista

    def get_all(self):
        try:
            page_response = requests.get(PAGE_LINK, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            body = page_content.find('body')
            section = body.findChildren("section", recursive=False)[0]
            container = section.findChildren('div', attrs={"class": "container-fluid"}, recursive=False)[0]
            div_8 = container.findChildren('div', attrs={"class": "col-md-8"}, recursive=False)[0]
            encontros = div_8.findChildren('div', recursive=False)[1:]
            for i in range(0,len(encontros)-1,2):
                tag1 = encontros[i]
                tag2 = encontros[i+1]
                titulo = self.get_titulo(tag1)
                img, descricao, data, horario, onde = self.get_info(tag2)
                evento = Evento(titulo, data, horario, descricao, onde, img, PAGE_LINK)
                self.lista.append(evento)
            return self
        except Exception as e:
            print(e)
            return None


    def get_titulo(self, tag1):
        span = tag1.findChildren('span', recursive=False)[0]
        titulo_tag = span.findChildren('b', recursive=False)[0]
        titulo = titulo_tag.text
        return titulo


    def get_info(self, tag2):
        div_imagem = tag2.findChildren('div',{ "class" : "col-md-5" }, recursive=False)[0]
        tag_img = div_imagem.findChildren('img', recursive=False)[0]
        img = tag_img["src"]
        div_info = tag2.findChildren('div',{ "class" : "col-md-7" }, recursive=False)[0]
        text = div_info.text.replace("\xa0", " ")
        data, descricao, horario, onde = self.get_details(text)
        return img, descricao, data, horario, onde

    def get_details(self, text):
        # data = re.findall(r"[0-3][0-9]/[0-1][0-9]/[1-2][0-9]{3}", text)[0]
        data = re.findall(r"Quando:.*",text)
        if not data: #para casos em que a palavra Quando nao estiver presente (robotica)
            data = re.findall(r"\nDe .*",text)[0][4:]
        else:
            data = data[0][8:]
        # hora = re.findall(r"[0-2]?[0-9]h[0-5][0-9]", text)[0]
        hora = re.findall(r"Horário:.*",text)[0][9:]
        onde = re.findall(r"Onde:.*",text)
        if not onde:
            onde = re.findall(r"Local:.*",text)[0][7:]
        else:
            onde = onde[0][6:]
        descricao = text.split("Quando:")[0]
        return data, descricao, hora, onde

class Evento:
    def __init__(self, titulo, data, horario, descricao, local, foto, link):
        self.titulo = titulo
        self.data = data
        self.horario = horario
        self.descricao = descricao
        self.local = local
        self.foto = foto
        self.link = link

# ev = Eventos()
# aa = ev.get_all()
# import json
# a = [x.__dict__ for x in aa.lista]
# b = json.dumps(a, ensure_ascii=False).encode('utf8')
# print("a")





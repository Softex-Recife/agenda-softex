from bs4 import BeautifulSoup
import requests
import re
import time
from datetime import datetime, timedelta

PAGE_LINK = "http://www.softexrecife.org.br/agenda/"

class Eventos():
    def __init__(self):
        self.ultima_att = None
        self.lista = []

    
    def request_all_events(self):
        """request all eventos on softex agenda's site and return div cotaining all"""
        encontros = None
        try:
            page_response = requests.get(PAGE_LINK, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            body = page_content.find('body')
            section = body.findChildren("section", recursive=False)[0]
            container = section.findChildren('div', attrs={"class": "container-fluid"}, recursive=False)[0]
            div_8 = container.findChildren('div', attrs={"class": "col-md-8"}, recursive=False)[0]
            encontros = div_8.findChildren('div', recursive=False)[1:]
        except Exception as e:
            print(e)
        return encontros


    def get_all(self):
        now = datetime.utcnow() - timedelta(hours=3)
        actual_month = now.month
        if actual_month is not self.ultima_att:
            try:
                encontros = self.request_all_events()
                for i in range(0,len(encontros)-1,2):
                    tag1 = encontros[i]
                    tag2 = encontros[i+1]
                    titulo = self.get_titulo(tag1)
                    img, descricao, data, horario, onde = self.get_info(tag2)
                    evento = Evento(titulo, data, horario, descricao, onde, img, PAGE_LINK)
                    self.lista.append(evento)
                    self.ultima_att = actual_month
            except Exception as e:
                print(e)
                return None
        return self.lista


    def get_events_from_now(self):
        def filter_from_now(event):
            today = datetime.utcnow() - timedelta(hours=3)
            current_day = today.day
            event_date = event.data
            try:
                even_first_date = re.findall(r"[0-9]{2}/[0-9]{2}/[0-9]{4}",event_date)[0]
                pass
            except:
                even_first_date = re.findall(r"[0-9]{2}/[0-9]{2}",event_date)[0]
                pass
            
            even_day = even_first_date[0:2]
            if int(even_day) >= current_day:
                return event
        events = self.get_all()
        new_list = []
        if events:
            new_list = list(filter(filter_from_now, events))            
        return new_list


    def get_events_today(self):
        def filter_today(event):
            today = datetime.utcnow() - timedelta(hours=3)
            current_day = today.day
            event_date = event.data
            even_first_date = re.findall(r"[0-9]{2}/[0-9]{2}/[0-9]{4}",event_date)[0]
            even_day = even_first_date[0:2]
            if int(even_day) is current_day:
                return event
        events = self.get_all()
        new_list = []
        if events:
            new_list = list(filter(filter_today, events))            
        return new_list


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





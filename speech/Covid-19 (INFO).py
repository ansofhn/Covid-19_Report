import speech_recognition as sr
from bs4 import BeautifulSoup as soup
import requests
from time import sleep as wait
from gtts import gTTS as speech
try: 
	from playsound import playsound
except: pass

# Function untuk mendeklarasikan module playsound
def voice (mp3):
	try: playsound(mp3)
	except: pass

# Variable List yang ada pada program
Table, country, cases, death, recovered = [],[],[],[],[]

# speech recognition program
r = sr.Recognizer()
def speak():
    with sr.Microphone() as source:
        audio = r.listen(source,phrase_time_limit=4)
        try:
            r.adjust_for_ambient_noise(source,duration=0.5)
            text = r.recognize_google(audio,language='id-ID')
            print('command ~~',text)
            return text
        except:
            try:
                text = r.recognize_google(audio,language='id-ID')
                return text
            except:
                print('Saya tidak bisa mendengar Anda ~')
    
while True:
    print('\n<'+'='*17+'>\n'+'|  COVID-19 INFO  |'+'\n<'+'='*17+'>\n\n'+'  > Kami akan memberikan Info mengenai virus corona diseluruh Dunia <\n> Kami telah merangkum Info penting tentang Virus Corona secara Realtime <\n');voice('hallo.mp3');voice('rangkum.mp3')
    print('|>> Total Kasus\n|>> Total Kematian\n|>> Total Diselamatkan\n\n');voice('command.mp3');voice('tanya.mp3')
    print('Apa yang ingin kamu Ketahui? ~')
    command = speak()
    voice('tungu.mp3')
    print('\n>> Sedang mengumpulkan Data..\n')
    
    # mengambil data dari website
    web = requests.get('https://www.worldometers.info/coronavirus/')
    parsing = soup(web.text, 'html.parser')

    # mengambil serta menampilkan data dari element dalam website
    all_data = parsing.find_all('div',id='maincounter-wrap')
    space =[(data.text.strip()) for data in all_data]

    def opening():
        print('<|  Worldwide  |>\n\n<'+'='*27+'>')
        for i in space:
            x=i.replace('\n\n',' ')
            print(' '+x)
        print('<'+'='*27+'>\n');voice('terbaru.mp3');wait(1)

    # mencari dan mengambil data dalam table
    table_body = parsing.find('tbody').find_all('tr')
    for data_table in table_body:
        Table.append(data_table.find_all('td'))

    # mengambil dan memasukan data yang lebih spesifik ke dalam variable list
    country = [columns[0].text.strip() for columns in Table]
    cases = [0 if columns[1].text.strip()=='' else int(columns[1].text.strip().replace(',','')) for columns in Table]
    death = [0 if columns[3].text.strip()=='' else int(columns[3].text.strip().replace(',','')) for columns in Table]
    recovered = [0 if columns[5].text.strip()=='' else int(columns[5].text.strip().replace(',','')) for columns in Table]

    # mengelompokkan data yang sudah diambil
    data = list(zip(country,cases,death,recovered))

    # fungsi unutuk mencari info data seperti kasus, kematian, dan diselamatkan berdasarkan negara
    def commandFor(negara, jenis):
        for i in data:
            if i[0] == negara:
                result = i[jenis]
            else: pass
        return result

    # fungsi untuk mengubah string menjadi sebuah suara
    def spk(arg):
        kata=speech(arg,lang='id')
        kata.save('suara.mp3')
        playsound('suara.mp3')

    if command == 'total kasus':
        voice('kasus.mp3')
        print('\n<'+'='*24+'>\n'+'|  TOTAL KASUS #COVID19  |'+'\n<'+'='*24+'>\n')
        opening()
        print('Negara mana yang ingin kamu Ketahui? ~');voice('negara.mp3')
        negara = speak()
        print('\n>> Mengumpulkan Data Negara',negara+'..');voice('tunggu.mp3');wait(1)
        casesTotal = commandFor(negara,1)
        x='Total kasus virus corona di Negara {} adalah {} kasus'.format(negara,str(casesTotal))
        spk(x)
        print('\nTotal kasus CoronaVirus di Negara {} ='.format(negara),casesTotal);wait(2)
    
    elif command == 'total kematian':
        voice('mati.mp3')
        print('\n<'+'='*27+'>\n'+'|  TOTAL KEMATIAN #COVID19  |'+'\n<'+'='*27+'>\n')
        opening()
        print('Negara mana yang ingin kamu Ketahui? ~');voice('negara.mp3')
        negara = speak()
        print('\n>> Mengumpulkan Data Negara',negara+'..');voice('tunggu.mp3');wait(1)
        deathTotal = commandFor(negara,2)
        x='Total kematian akibat virus corona di Negara {} adalah {} orang'.format(negara,str(deathTotal))
        spk(x)
        print('\nTotal Kematian akibat CoronaVirus di Negara {} ='.format(negara),deathTotal);wait(2)

    elif command == 'total diselamatkan':
        voice('recov.mp3')
        print('\n<'+'='*31+'>\n'+'|  TOTAL DISELAMATKAN #COVID19  |'+'\n<'+'='*31+'>\n')
        opening()
        print('Negara mana yang ingin kamu Ketahui? ~');voice('negara.mp3')
        negara = speak()
        print('\n>> Mengumpulkan Data Negara',negara+'..');voice('tunggu.mp3');wait(1)
        recoveredTotal = commandFor(negara,3)
        x='Total orang yang telah sembuh dari wabah virus corona di Negara {} adalah {} orang'.format(negara,recoveredTotal)
        spk(x)
        print('\nTotal Terselamatkan dari Wabah CoronaVirus di Negara {} ='.format(negara),recoveredTotal);wait(2)

    print('='*43+'>\n>> Apa Kamu mau dapat info lebih lanjut? ~\n')
    pilihan = speak()
    if pilihan == 'tidak':
        print('\n\"Terima Kasih, Kamu sudah mengakses info pada Program ini\"\n  #Staysafe\n  #Salamsehat\n  #Jagadiri')
        break
    elif pilihan == 'ya': continue 
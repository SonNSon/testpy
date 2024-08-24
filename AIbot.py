import os 
import speech_recognition as sr
import time
import ctypes
import wikipedia
import datetime
import webbrowser
import smtplib
import requests
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from youtube_search import YoutubeSearch

r = sr.Recognizer()
wikipedia.set_lang('vi')
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

APPS = {
    'google': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
    'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE'
}

#chuyển văn bản thành giọng nói và phát ra tai nghe
def speak(text):
    print("Bot: {}".format(text))  
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")

    engine.setProperty("voices",voices[1].id)

    engine.say(text)

    engine.runAndWait()

def get_voice():
    with sr.Microphone() as source:
        r.energy_threshold = 500
        r.adjust_for_ambient_noise(source, 1.2)
        r.pause_threshold = 1
        audio = r.listen(source)
        voice_data = ''

        try:
            voice_data = r.recognize_google(
                audio, language="vi-VN")
        except sr.RequestError:
            speak("Xin lỗi, dịch vụ không được kết nối")
        except sr.UnknownValueError:
            speak("Mình không nghe rõ, bạn có thể nói lại được không ?")
        
        if voice_data:
            print(f">> {voice_data.lower()}")
        return voice_data.lower()

def stop():
    speak("Hẹn gặp lại bạn nhé ")
    exit()

def get_text():
    for _ in range(3):
        text = get_voice()
        if text:
            return text.lower()
    time.sleep(3)
    stop()

def send_email():
    recipients = [
        '12a2quynhnhu@gmail.com'
    ]

    sender = 'sonvtthanthanh@gmail.com'
    try:
        speak("Nội dung bạn muốn gửi là gì: ")
        content = get_text()

        mail = smtplib.SMTP('smtp.gmail.com',587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, 'app password')
        mail.sendmail(sender, recipients, content.encode('utf-8'))
        mail.close()
        speak('Email của bạn vừa được gửi. Bạn check lại email nhé hihi')
    except Exception:
        speak('Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?')

def google_search():
    speak("Bạn muốn tìm kiếm gì? ")
    search_for = get_text()

    with webdriver.Chrome() as browser:
        browser.get("https://www.google.com")
        time.sleep(3)
        query = browser.find_element(
            By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea")
        query.send_keys(str(search_for))
        query.send_keys(Keys.RETURN)
        time.sleep(10)

def get_news():
    with webdriver.Chrome(options =options) as browser:
        browser.get("https://baomoi.com/")
        speak("Các tin mới hôm nay là:")
        time.sleep(5)
        first_link = browser.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div[2]/aside/div[1]/div/div/div[2]/div[1]/h3/a").get_attribute("title")
        speak(first_link)
        time.sleep(2)
        links = browser.find_elements(
            By.XPATH, "/html/body/div[2]/div[3]/div/div/div/div[2]/aside/div[2]/div/div/div[2]/div[1]/h3/a")
        
        for link in links:
            speak(link.get_attribute("title"))
            time.sleep(2)

def today():
    now = datetime.datetime.now()
    speak("Hôm nay là ngày %d tháng %d năm %d, %d giờ %d phút %d giây" % (now.day, now.month, now.year, now.hour, now.minute, now.second))

def play_youtube():
    speak("Xin mời bạn chọn bài hát")
    time.sleep(3)
    my_song = get_text()
    while True:
        result = YoutubeSearch(my_song, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com/' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát của bạn đã được mở, hãy thưởng thức nó!")
    
def weather():
    speak ("Bạn muốn xem thời tiết ở đâu ạ!")
    time.sleep(3)
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temp = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        sun_time = data["sys"]
        sun_rise = datetime.datetime. fromtimestamp(sun_time[" sunrise"])
        sun_set = datetime.datetime. fromtimestamp (sun_time[" sunset"])
        wther = data[ "weather"]
        weather_res = wther[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C 
        Áp suất không khí là {pressure} héc to Pascal 
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác một số nơi""".format(day=now.day, month = now.month, year=now.year, hourrise=sun_rise.hour, minrise= sun_rise.minute, hourset=sun_set.hour, minset = sun_set.minute,temp=current_temp, pressure = current_pressure, humidity=current_humidity)

  
        speak (content)
        time. sleep (5)
    else:
        speak("Không tìm thấy thành phố!")

def open_application(text):
    for app in APPS:
        if app == text:
            speak(f"Mở {text}")
            os.startfile(APPS[text])
            break
    else:
        speak("Phần mềm của bạn chưa được cài đặt!")

def tell_me():
    try:
        speak("Bạn muốn nghe về gì ạ!")
        text=get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(3)
        for content in contents[1:]:
            speak("Bạn muốn nghe tiếp hay không ?")
            ans = get_text()
            if"Không" in ans:
                break
            speak(content)
            time.sleep(5)

        speak("Cảm ơn bạn đã lắng nghe!")
    except:
        speak("Mình không định nghĩa được ngôn ngữ của bạn!")

def help():
    speak("""Chức năng phần mềm:
          1. Chào hỏi, giao tiếp
          2. Cho biết thời gian hiện tại
          3. Chạy ứng dụng hệ thống
          4. Gửi mail đến những người quen biết
          5. Phát nhạc trên Youtube
          6. Cho biết tin tức hôm nay
          7. CHo biết thời tiết, nhiệt độ
          8. Tìm kiếm thông tin trên Google
          9. Hiển thị hoặc nói thông tin mình yêu cầu""")
    time.sleep(5)

def greet():
    speak("Xin hỏi tên bạn là gì?")
    name = get_text()
    if not name:
        speak("Bạn cần nói lại tên")
        return
    speak(f"Chào {name}, rất vui được hỗ trợ bạn")

def there_exist(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True
        
def handle_virtual_assistant():
    while True:
        speak("Bạn cần tôi làm gì ?")
        time.sleep(2)
        text = get_text()
        if there_exist(["chào bạn","này","chào"],text):
            greet()
        elif there_exist(["ngày","giờ","thời gian hiện tại"],text):
            today()
        elif there_exist(list(APPS),text):
            open_application(text)
        elif there_exist(["phát nhạc","chơi nhạc","bật nhạc"],text):
            play_youtube()
        elif there_exist(["thời tiết", "nhiệt độ", "thời tiết hôm nay"],text):
            weather()
        elif there_exist(["gửi","mail","gửi mail"],text):
            send_email()
        elif there_exist(["tin tức","tin tức hôm nay","tin mới"],text):
            get_news()
        elif there_exist(["tìm kiếm", "kiếm", "tìm"],text):
            google_search()
        elif there_exist(["hiển thị", "nói","thông tin","yêu cầu"],text):
            tell_me()
        elif "có thể làm gì" in text:
            help()

if __name__ == "__main__":
    handle_virtual_assistant()

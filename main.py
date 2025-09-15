import os
import requests
from plyer import filechooser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

# قم بتغيير هذه القيم بمعلوماتك الخاصة
BOT_TOKEN = "8238373981:AAGWnyIrx5heh1nxBtbaMlLDZkieUtrQFmg"
CHAT_ID = "6911605832"

# هذا الكود يقوم بإنشاء الواجهة من ملف KV
kv_code = """
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10

    Label:
        id: status_label
        text: 'اضغط على الزر لاختيار الصور وإرسالها.'
        text_size: self.size
        halign: 'center'
        valign: 'middle'

    Button:
        text: 'اختيار وإرسال الصور'
        on_press: app.root.send_photos()
"""

class PhotoSenderApp(App):
    def build(self):
        return Builder.load_string(kv_code)

    def send_photos(self):
        # تحديث حالة الواجهة
        self.root.ids.status_label.text = 'جارٍ اختيار الصور...'
        
        # استخدام plyer لفتح معرض الصور
        filechooser.open_file(on_selection=self.on_photos_selected, multiple=True)

    def on_photos_selected(self, selection):
        if not selection:
            self.root.ids.status_label.text = 'لم يتم اختيار أي صور.'
            return

        self.root.ids.status_label.text = f'تم اختيار {len(selection)} صور. جارٍ الإرسال...'
        
        # إرسال كل صورة على حدة
        for photo_path in selection:
            self.send_photo_to_telegram(photo_path)
            
        self.root.ids.status_label.text = 'اكتمل إرسال جميع الصور!'

    def send_photo_to_telegram(self, photo_path):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        # فتح ملف الصورة للقراءة الثنائية
        try:
            with open(photo_path, 'rb') as photo_file:
                files = {'photo': photo_file}
                data = {'chat_id': CHAT_ID}
                
                # إرسال طلب POST إلى تيليجرام
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    print(f"تم إرسال الصورة: {photo_path}")
                else:
                    print(f"فشل إرسال الصورة: {photo_path}, الخطأ: {response.text}")
        except FileNotFoundError:
            print(f"الملف غير موجود: {photo_path}")
        except requests.exceptions.RequestException as e:
            print(f"خطأ في الاتصال: {e}")

if __name__ == '__main__':
    PhotoSenderApp().run()
    

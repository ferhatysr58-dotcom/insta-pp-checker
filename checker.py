import os
import requests
from bs4 import BeautifulSoup

USERNAME = "cansuuayazz35"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def main():
    url = f"https://www.instagram.com/{USERNAME}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        meta = soup.find("meta", property="og:image")
        if not meta or not meta.get("content"):
            print("Profil resmi URL'si çekilemedi.")
            return

        new_img_url = meta["content"]
        
        # Önceki kayıtlı resmi kontrol et
        old_img_url = ""
        if os.path.exists("last_pp.txt"):
            with open("last_pp.txt", "r") as f:
                old_img_url = f.read().strip()

        # İlk çalıştırma veya Değişiklik Kontrolü
        if not old_img_url:
            with open("last_pp.txt", "w") as f:
                f.write(new_img_url)
            print("İlk profil fotoğrafı kaydedildi.")
        elif old_img_url != new_img_url:
            with open("last_pp.txt", "w") as f:
                f.write(new_img_url)
            send_telegram_msg(f"🚨 {USERNAME} profil fotoğrafını değiştirdi!\n\nYeni Fotoğraf Bağlantısı:\n{new_img_url}")
            print("Profil fotoğrafı değişti, Telegram bildirimi gönderildi!")
        else:
            print("Profil fotoğrafında değişiklik yok.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()

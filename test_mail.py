from email_sender import send_email
import os
from dotenv import load_dotenv

# Yapılandırmayı yükle
load_dotenv()

def test_send():
    # Test edilecek mail listesi
    test_listesi = [
       
    ]
    
    cv_dosyasi = ""
    
    for kisi in test_listesi:
        print(f"Test maili gönderiliyor: {kisi['mail']} ({kisi['isim']})...")
        
        if send_email(kisi['mail'], f"{kisi['isim']} Teknoloji (Test)", cv_dosyasi):
            print(f"[+] {kisi['isim']} için test başarılı.")
        else:
            print(f"[-] {kisi['isim']} için gönderilemedi.")

    print("\nİşlem tamamlandı. Lütfen mail kutularınızı (ve spam klasörlerini) kontrol edin.")

if __name__ == "__main__":
    test_send()

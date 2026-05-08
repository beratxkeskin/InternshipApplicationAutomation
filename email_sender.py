import pandas as pd
import smtplib
import ssl
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Yapılandırmayı yükle
load_dotenv()
sender_email = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

# E-posta Konusu
SUBJECT = "Staj Başvurusu - Berat Keskin"

# HTML E-posta Taslağı (Premium Tasarım)
HTML_BODY_TEMPLATE = """
<html>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #2c3e50; max-width: 600px; margin: auto; border: 1px solid #e1e4e8; padding: 20px; border-radius: 10px;">
    <h2 style="color: #2980b9; border-bottom: 2px solid #2980b9; padding-bottom: 10px;">Sayın {company_name} Ekibi,</h2>
    
    <p>Ben <strong>Berat Keskin</strong>, İstanbul Atlas Üniversitesi Yazılım Mühendisliği 3. sınıf öğrencisiyim. Bu yaz gerçekleştireceğim 30 günlük zorunlu stajımı ekibinizde tamamlamak ve sonrasında sizin de uygun gördüğünüz takdirde okul döneminde part-time olarak çalışmaya devam etmek amacıyla size ulaşıyorum.</p>
    
    <p>Sürekli öğrenmeye açık yapım ve takım çalışmasına olan yatkınlığımla ekibinize hızlıca adapte olup süreçlerinize katkı sağlayabileceğime inanıyorum.</p>
    
    <p>Geliştirdiğim projeleri ve teknik yetkinliklerimi ekteki <strong>CV'mden</strong> inceleyebilirsiniz. Uygun gördüğünüz bir zamanda sizinle tanışmayı ve süreci konuşmayı çok isterim.</p>
    
    <p>Vakit ayırdığınız için teşekkür eder, iyi çalışmalar dilerim.</p>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; margin-top: 20px;">
        <p style="font-size: 0.85em; color: #7f8c8d; margin: 0;">
            <em><strong>Mühendislik Notu:</strong> Bu başvuruyu, İstanbul'daki teknoloji ekosistemini analiz ederek geliştirdiğim küçük bir Python otomasyonu ile size ulaştırdım. Teknoloji ile süreçleri hızlandırmayı ve verimli çözümler üretmeyi seviyorum.</em>
        </p>
    </div>

    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
        <span style="font-size: 1.1em; color: #2c3e50;"><strong>Berat Keskin</strong></span><br>
        <span style="color: #7f8c8d;">Yazılım Mühendisliği Öğrencisi</span><br>
        <span style="color: #7f8c8d;">📞 +90 552 687 94 61</span>
    </div>
</body>
</html>
"""

def get_sent_emails(log_file):
    if not os.path.exists(log_file):
        return set()
    with open(log_file, "r") as f:
        return set(line.strip() for line in f)

def log_sent_email(log_file, email):
    with open(log_file, "a") as f:
        f.write(f"{email}\n")

def send_email(target_email, company_name, cv_path):
    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = target_email
        message["Subject"] = SUBJECT
        
        # HTML İçeriği Ekle
        html_content = HTML_BODY_TEMPLATE.format(company_name=company_name)
        message.attach(MIMEText(html_content, "html"))

        # CV Dosyasını ekle
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(cv_path)}")
            message.attach(part)
        else:
            print(f"Hata: {cv_path} bulunamadı!")
            return False

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, target_email, message.as_string())
        
        return True
    except Exception as e:
        print(f"Hata ({company_name}): {e}")
        return False

def main():
    csv_file = "istanbul_staj_listesi_mailli.csv"
    cv_file = "CV - Berat Keskin (ENG).pdf"
    log_file = "gonderilenler.log"
    
    # Bugün kaç tane göndermek istediğin (Güvenli sınır: 200)
    DAILY_LIMIT = 250 
    
    if not os.path.exists(csv_file):
        print("CSV dosyası bulunamadı!")
        return

    df = pd.read_csv(csv_file)
    sent_emails = get_sent_emails(log_file)
    
    current_sent = 0
    print(f"Otomasyon başlatıldı. Daha önce {len(sent_emails)} mail gönderilmiş.\n")

    for index, row in df.iterrows():
        if current_sent >= DAILY_LIMIT:
            print(f"\nGünlük limite ({DAILY_LIMIT}) ulaşıldı. İşlem durduruldu.")
            break
            
        company = row['Şirket Adı']
        email = str(row['E-posta'])
        
        if "@" in email and email not in sent_emails:
            print(f"[{index+1}] Gönderiliyor: {company} ({email})...")
            
            if send_email(email, company, cv_file):
                print(f"  [+] Başarıyla gönderildi.")
                log_sent_email(log_file, email)
                current_sent += 1
                time.sleep(15) # Güvenli bekleme süresi
            else:
                print(f"  [-] Gönderilemedi, atlanıyor.")

    print(f"\nSeans Tamamlandı! Bugün {current_sent} yeni mail gönderildi.")
    print("Kaldığın yerden devam etmek için scripti tekrar çalıştırman yeterli.")

if __name__ == "__main__":
    main()

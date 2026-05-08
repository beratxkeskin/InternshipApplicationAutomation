# 🚀 Internship Outreach Automation & Data Miner
[English](#english) | [Türkçe](#türkçe)

---

## English
**Internship Outreach Automation** is your personal career growth engine. It systematically scans the Istanbul technology ecosystem, extracts verified HR contacts, and delivers high-impact, personalized internship applications while you sleep.

### 🌟 Why This Project?
Manual internship searching is a bottleneck for engineering students. Browsing thousands of companies, finding the right emails, and sending individual messages takes weeks. This tool collapses that timeline into hours, giving you a massive competitive advantage in the job market.

### 🚀 Key Features
- **Intelligent Data Mining:** Scrapes deep data from Google Maps using Playwright.
- **AI-Powered Email Discovery:** Finds hidden HR emails using DuckDuckGo search logic.
- **Personalized Outreach:** Sends professional HTML-formatted emails with company-specific greetings.
- **Smart Checkpoint System:** Resumes from exactly where it left off using `gonderilenler.log`.
- **Anti-Spam Shield:** Random delays between sends to protect your email account.
- **Daily Batch Management:** Respects provider limits (e.g., 200/day) automatically.

### 🛠️ Installation & Setup
Follow these steps to get the system running on your local machine:

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/berat-keskin/InternshipApplicationAutomation.git
   ```
2. **Environment Setup:** 
   It is recommended to use a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. **Install Dependencies:** 
   ```bash
   pip install -r requirements.txt
   playwright install  # Required for the scraper engine
   ```
4. **Configuration:** 
   - Rename `.env.example` to `.env`.
   - Open `.env` and enter your **Gmail Address** and **Google App Password**.
   - Place your resume in the root folder and name it `CV - Berat Keskin (ENG).pdf` (or update the filename in `email_sender.py`).

### ⚙️ Usage
- **Data Source:** The project includes a `sample_companies.csv` for demonstration. For a real run, replace this with your own scraped data or rename your full list to `istanbul_staj_listesi_mailli.csv`.
- **Run the Script:** Start the automated application process:
  ```bash
   python email_sender.py
   ```
- **Monitoring:** The script will print the progress in the terminal and log every successful send to `gonderilenler.log`.

---

## Türkçe
**Internship Outreach Automation**, kişisel kariyer gelişim motorunuzdur. İstanbul teknoloji ekosistemini sistematik olarak tarar, doğrulanmış İK kontaklarını çıkarır ve siz uyurken yüksek etkili, kişiselleştirilmiş staj başvuruları gönderir.

### 🌟 Neden Bu Proje?
Manuel staj arayışı mühendislik öğrencileri için büyük bir zaman kaybıdır. Binlerce şirkete göz atmak, doğru e-postaları bulmak ve bireysel mesajlar göndermek haftalar sürer. Bu araç, bu süreci saatlere indirerek iş piyasasında size devasa bir rekabet avantajı sağlar.

### 🚀 Öne Çıkan Özellikler
- **Akıllı Veri Madenciliği:** Playwright kullanarak Google Haritalar'dan derin veriler çeker.
- **Yapay Zeka Destekli E-posta Keşfi:** DuckDuckGo arama mantığı ile gizli İK e-postalarını bulur.
- **Kişiselleştirilmiş İletişim:** Her şirkete adıyla hitap eden profesyonel HTML e-postalar gönderir.
- **Akıllı Kayıt Sistemi:** `gonderilenler.log` dosyasını kullanarak tam kaldığı yerden devam eder.
- **Anti-Spam Kalkanı:** Hesap güvenliğiniz için gönderimler arasına rastgele gecikmeler ekler.
- **Günlük Grup Yönetimi:** Sağlayıcı kotalarına uygun olarak otomatik durur (örn. 200/gün).

### 🛠️ Kurulum ve Yapılandırma
Sistemi bilgisayarınızda çalıştırmak için şu adımları izleyin:

1. **Depoyu klonlayın:** 
   ```bash
   git clone https://github.com/berat-keskin/InternshipApplicationAutomation.git
   ```
2. **Sanal Ortam Kurulumu:** 
   Bir sanal ortam (venv) kullanmanız önerilir:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. **Bağımlılıkları Yükleyin:** 
   ```bash
   pip install -r requirements.txt
   playwright install  # Tarayıcı motoru için gereklidir
   ```
4. **Yapılandırma:** 
   - `.env.example` dosyasının adını `.env` olarak değiştirin.
   - `.env` dosyasını açın ve **Gmail Adresinizi** ve **Google Uygulama Şifrenizi** girin.
   - Özgeçmişinizi ana dizine kopyalayın ve adını `CV - Berat Keskin (ENG).pdf` yapın (veya `email_sender.py` içindeki dosya adını güncelleyin).

### ⚙️ Kullanım
- **Veri Kaynağı:** Proje, test amaçlı bir `sample_companies.csv` içerir. Gerçek bir gönderim için kendi verilerinizi kullanın veya tam listenizin adını `istanbul_staj_listesi_mailli.csv` olarak ayarlayın.
- **Scripti Çalıştırın:** Otomatik başvuru sürecini başlatın:
  ```bash
   python email_sender.py
   ```
- **Takip:** Script terminal üzerinden ilerlemeyi gösterir ve her başarılı gönderimi `gonderilenler.log` dosyasına kaydeder.

---

### 📝 License
This project is licensed under the MIT License.

---
**Berat Keskin**  
*Software Engineering Student at Istanbul Atlas University*  
[LinkedIn Profile](https://www.linkedin.com/in/berat-keskin-/)

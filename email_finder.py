import pandas as pd
import requests
import re
import asyncio
import os
from playwright.async_api import async_playwright
from urllib.parse import urljoin

class EmailHunter:
    def __init__(self):
        # E-posta yakalama deseni
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    async def find_website(self, company_name):
        """Şirket isminden resmi web sitesini bulur (Çoklu seçici ve dinamik bekleme ile)."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            # Daha gerçekçi bir kimlik
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()
            
            try:
                # Aramayı sadeleştiriyoruz
                query = company_name
                search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}" # HTML (Lite) sürümünü de deneyebiliriz
                
                # Önce standart sürümü deneyelim
                await page.goto(f"https://duckduckgo.com/?q={query.replace(' ', '+')}", timeout=30000)
                
                # Olası tüm seçiciler (Modern, Klasik ve Lite)
                selectors = [
                    'article h2 a', 
                    '[data-testid="result-title-a"]', 
                    'a.result-link', 
                    '.result__a',
                    '#r1-0 a'
                ]
                
                combined_selector = ", ".join(selectors)
                
                # Dinamik olarak bekle
                try:
                    await page.wait_for_selector(combined_selector, timeout=10000)
                except:
                    # Eğer yüklenmediyse bir de HTML sürümüne git (Bot korumasını aşmak için)
                    await page.goto(f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}", timeout=20000)
                    await page.wait_for_timeout(2000)

                # Linki bul
                link_element = await page.query_selector(combined_selector)
                
                if link_element:
                    url = await link_element.get_attribute('href')
                    if url and 'duckduckgo.com' not in url and url.startswith('http'):
                        # DuckDuckGo bazen kendi yönlendirme linkini verir, onu temizle
                        if '/l/?kh=-1&uddg=' in url:
                            from urllib.parse import unquote
                            url = unquote(url.split('uddg=')[1].split('&')[0])
                        return url
                
                return None
            except:
                return None
            finally:
                await browser.close()

    def get_emails_from_site(self, url):
        """Web sitesinden ve iletişim sayfalarından e-postaları çeker."""
        if not url:
            return "Yok"
            
        found_emails = set()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
        
        try:
            # 1. Ana sayfayı tara
            response = requests.get(url, timeout=15, headers=headers, verify=False) # SSL hatalarını yoksay
            content = response.text
            found_emails.update(re.findall(self.email_pattern, content))
            
            # 2. İletişim sayfasını bulmaya çalış (Hiyerarşik arama)
            contact_keywords = ['contact', 'iletisim', 'hakkimizda', 'about', 'career', 'kariyer']
            contact_links = []
            
            for kw in contact_keywords:
                match = re.search(f'href=["\'](.*?{kw}.*?)["\']', content, re.I)
                if match:
                    c_url = match.group(1)
                    if not c_url.startswith('http'):
                        c_url = urljoin(url, c_url)
                    contact_links.append(c_url)
            
            # Bulunan ilk 2 iletişim sayfasını tara
            for c_url in list(set(contact_links))[:2]:
                try:
                    c_res = requests.get(c_url, timeout=10, headers=headers, verify=False)
                    found_emails.update(re.findall(self.email_pattern, c_res.text))
                except:
                    continue
            
            # Temizlik: Görsel dosyalarını ve gereksizleri temizle
            valid_emails = {email.lower() for email in found_emails 
                           if not any(ext in email.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'])}
            
            return ", ".join(valid_emails) if valid_emails else "E-posta bulunamadı"
            
        except Exception:
            return "Erişim Sorunu"

async def process_list():
    input_file = 'istanbul_staj_listesi.csv'
    output_file = 'istanbul_staj_listesi_mailli.csv'
    
    if not os.path.exists(input_file):
        print(f"[!] Hata: {input_file} bulunamadı.")
        return

    hunter = EmailHunter()
    df = pd.read_csv(input_file)
    results = []
    
    print(f"=== E-POSTA BULUCU (DUCKDUCKGO DESTEKLİ) ===")
    print(f"[*] Toplam {len(df)} şirket taranacak...\n")

    for index, row in df.iterrows():
        name = row['Şirket Adı']
        print(f"[{index+1}/{len(df)}] Araştırılıyor: {name}")
        
        site = await hunter.find_website(name)
        if site:
            print(f"      [+] Site: {site}")
            mails = hunter.get_emails_from_site(site)
            print(f"      [+] Mailler: {mails}")
        else:
            print(f"      [-] Site Bulunamadı")
            mails = "Web Sitesi Bulunamadı"
            
        results.append({
            "Şirket Adı": name,
            "Web Sitesi": site or "Bulunamadı",
            "E-posta": mails
        })
        
        # Her 3 kayıtta bir ara kayıt yap
        if (index + 1) % 3 == 0:
            pd.DataFrame(results).to_csv(output_file, index=False, encoding='utf-8-sig')

    # Final kaydı
    pd.DataFrame(results).to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n[+] İşlem Başarıyla Tamamlandı! Dosya: {output_file}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    asyncio.run(process_list())

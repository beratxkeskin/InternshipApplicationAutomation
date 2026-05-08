import asyncio
import csv
import os
from playwright.async_api import async_playwright
from typing import List, Dict

class GoogleMapsFreeScraper:
    """API Key ve kredi kartı gerektirmeyen, tarayıcı tabanlı Google Maps kazıyıcı."""

    def __init__(self):
        self.results = []

    async def fetch_places(self, search_query: str) -> List[Dict]:
        """
        Google Maps üzerinde arama yapar ve şirket bilgilerini çeker.
        """
        async with async_playwright() as p:
            # Tarayıcıyı başlat (Görünmez modda: headless=True)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            print(f"[*] Aranıyor: {search_query}...")
            
            # Google Maps arama URL'si
            url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
            
            try:
                await page.goto(url, timeout=60000)
                # Sayfanın yüklenmesi için bekle
                await page.wait_for_timeout(5000)

                # Google Maps yan panelini (sonuç listesini) bul
                scrollable_selector = 'div[role="feed"]'
                
                try:
                    # Panelin görünmesini bekle
                    await page.wait_for_selector(scrollable_selector, timeout=15000)
                    
                    print("   > Liste kaydırılıyor ve yeni şirketler yükleniyor...")
                    for _ in range(8): # Kaydırma sayısını artırdık
                        # Panel üzerinde mouse wheel kullan
                        await page.hover(scrollable_selector)
                        await page.mouse.wheel(0, 4000)
                        await page.wait_for_timeout(2000) # Yükleme için bekleme süresi
                except:
                    print("   [!] Kaydırılabilir liste paneli bulunamadı, mevcut sayfa taranıyor...")

                # Şirket isimlerini içeren elementleri bul
                # qBF1Pd: Liste görünümündeki başlıklar
                # fontHeadlineSmall: Alternatif başlık sınıfı
                elements = await page.query_selector_all('.qBF1Pd')
                
                local_results = []
                for el in elements:
                    name_text = await el.inner_text()
                    if name_text and len(name_text) > 2:
                        local_results.append({
                            "Şirket Adı": name_text,
                            "Kaynak": "Google Maps (Ücretsiz Tarayıcı)"
                        })
                
                # Tekilleştirme (Bu sorgu içindeki mükerrerleri temizle)
                unique_local = {v['Şirket Adı']: v for v in local_results}.values()
                local_results = list(unique_local)

                print(f"   > {len(local_results)} şirket bulundu.")
                await browser.close()
                return local_results

            except Exception as e:
                print(f"   [!] Hata oluştu: {e}")
                await browser.close()
                return []

    def save_to_csv(self, data: List[Dict], filename: str = "istanbul_staj_listesi.csv"):
        """Verileri CSV olarak kaydeder."""
        if not data:
            print("[!] Kaydedilecek veri bulunamadı.")
            return

        keys = data[0].keys()
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            print(f"\n[+] BAŞARILI: {len(data)} şirket '{filename}' dosyasına kaydedildi.")
        except IOError as e:
            print(f"[!] Dosya yazma hatası: {e}")

async def main():
    print("=== GOOGLE MAPS ÜCRETSİZ ŞİRKET BULUCU (KART GEREKTİRMEZ) ===\n")
    
    scraper = GoogleMapsFreeScraper()
    
    # Kapsamlı ve Detaylı Arama Terimleri
    search_queries = [
        # --- 1. TEKNOPARK VE LOKASYON ODAKLI (Avrupa Yakası Ağırlıklı) ---
        "İTÜ Arı Teknokent yazılım şirketleri",
        "Yıldız Teknopark Davutpaşa teknoloji firmaları",
        "Yıldız Teknopark Maslak Ar-Ge merkezleri",
        "Bilişim Vadisi İstanbul teknoloji firmaları",
        "Maslak yazılım ve inovasyon şirketleri",
        "Levent teknoloji girişimleri",
        "Kağıthane bilişim ve yazılım ofisleri",
        "Şişli yazılım ajansları",
        "Beşiktaş teknoloji girişimleri kuluçka merkezleri",
        
        # --- 2. YAPAY ZEKA VE BİLGİSAYARLI GÖRÜ (Computer Vision) ---
        "Yapay zeka (AI) şirketleri İstanbul",
        "Bilgisayarlı görü (Computer Vision) firmaları İstanbul",
        "Görüntü işleme Ar-Ge şirketleri İstanbul",
        "Makine öğrenmesi (Machine Learning) girişimleri İstanbul",
        "AI startups Istanbul",
        "Yapay zeka araştırma laboratuvarları İstanbul",

        # --- 3. IOT, GÖMÜLÜ SİSTEMLER VE DONANIM ---
        "IoT (Nesnelerin İnterneti) şirketleri İstanbul",
        "Gömülü sistemler (Embedded Systems) yazılım İstanbul",
        "Akıllı güvenlik sistemleri Ar-Ge İstanbul",
        "Elektronik donanım ve yazılım firmaları İstanbul",
        "Akıllı cihaz teknolojileri firmaları İstanbul",

        # --- 4. MOBİL UYGULAMA VE ÜRÜN GELİŞTİRME ---
        "Mobil uygulama geliştirme şirketleri İstanbul",
        "Yazılım ürün geliştirme (Product Studio) firmaları İstanbul",
        "Mobil teknoloji girişimleri İstanbul",

        # --- 5. GENEL VE YENİLİKÇİ EKOSİSTEM ---
        "Teknoloji kuluçka merkezleri İstanbul",
        "Savunma sanayi ve teknoloji şirketleri İstanbul", # Teknofest ekosistemi için
        "Derin teknoloji (Deep Tech) girişimleri İstanbul",
        "Yazılım Ar-Ge merkezleri Avrupa Yakası"

        # --- 6. BANKACILIK VE FİNTEK (FinTech) ---
        "Banka teknoloji şirketleri İstanbul",
        "Fintek (FinTech) firmaları Levent",
        "Ödeme sistemleri yazılım şirketleri Maslak",
        "Banka genel müdürlükleri bilgi teknolojileri Şişli",
        "Kripto para ve blockchain teknolojileri şirketleri İstanbul",
        "Yatırım şirketleri teknoloji departmanları",

        # --- 7. SİGORTA TEKNOLOJİLERİ (InsurTech) ---
        "Sigorta şirketleri genel müdürlükleri Zincirlikuyu",
        "InsurTech (Sigorta Teknolojileri) girişimleri İstanbul",
        "Bireysel emeklilik şirketleri teknoloji merkezleri",
        
        # --- 8. BÜYÜK HOLDİNGLER VE E-TİCARET ---
        "Holding genel müdürlükleri bilgi işlem Levent",
        "E-ticaret şirketleri teknoloji ve Ar-Ge merkezleri İstanbul",
        "Telekomünikasyon şirketleri teknoloji üsleri",
        "Perakende şirketleri yazılım departmanları Maslak",
        "Havayolu şirketleri teknoloji merkezleri",

        # --- 9. DANIŞMANLIK VE SİSTEM ENTEGRATÖRLERİ ---
        "Bilişim danışmanlık firmaları İstanbul",
        "Sistem entegratörü şirketler Avrupa Yakası",
        "Kurumsal yazılım çözümleri şirketleri Şişli"
    ]
    
    all_companies = []
    
    for q in search_queries:
        results = await scraper.fetch_places(q)
        all_companies.extend(results)
    
    # Tekilleştirme (Aynı şirket birden fazla aramada çıkabilir)
    unique_companies = {v['Şirket Adı']: v for v in all_companies}.values()
    
    # Kaydetme
    scraper.save_to_csv(list(unique_companies))
    print("\nİşlem tamamlandı. Listeyi Excel ile açabilirsin.")

if __name__ == "__main__":
    asyncio.run(main())

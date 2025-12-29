# DES Tarzı Anahtar Planlama Algoritması ile Rastgele Sayı Üreteci
# Kriptografi ilhamlı özel algoritma

import time

class AnahtarPlanlamaAlgoritmasi:
    """
    DES (Data Encryption Standard) tarzında tasarlanmış 
    kendi anahtar planlama ve rastgele sayı üreteci algoritmam.
    
    DES'teki gibi:
    - Ana anahtar kullanılır
    - Alt anahtarlar üretilir
    - Permütasyon (yer değiştirme) işlemleri yapılır
    - Kaydırma işlemleri uygulanır
    """
    
    def __init__(self, ana_anahtar=None):
        """
        Anahtar planlama algoritmasını başlatır.
        
        ana_anahtar: 64-bit (8 bayt) ana anahtar
        """
        # Eğer anahtar verilmemişse, zamanı kullanarak oluştur
        if ana_anahtar is None:
            zaman_damgasi = int(time.time() * 1000)
            ana_anahtar = zaman_damgasi % (2**64)  # 64-bit'e sığdır
        
        self.ana_anahtar = ana_anahtar
        self.alt_anahtarlar = []  # Üretilecek alt anahtarlar
        self.mevcut_tur = 0       # Hangi turda olduğumuz
        
        # Algoritma sabitleri
        self.tur_sayisi = 16      # DES gibi 16 tur
        
        # Alt anahtarları üret
        self._alt_anahtarlari_uret()
    
    def _bit_permutasyonu(self, sayi, bit_sayisi):
        """
        Sayının bitlerini karıştırır (permütasyon).
        DES'teki P-Box (Permutation Box) işlemine benzer.
        
        sayi: Karıştırılacak sayı
        bit_sayisi: Kaç bitlik sayı
        """
        # Basit bir permütasyon: bitleri ters çevir ve XOR uygula
        ters = 0
        for i in range(bit_sayisi):
            if sayi & (1 << i):
                ters |= (1 << (bit_sayisi - 1 - i))
        
        # Orijinal ile XOR yaparak karıştır
        sonuc = sayi ^ ters
        return sonuc
    
    def _sol_kaydirma(self, sayi, kayma_miktari, bit_sayisi):
        """
        Sayının bitlerini sola kaydırır (circular shift).
        DES'teki left shift işlemi.
        
        sayi: Kaydırılacak sayı
        kayma_miktari: Kaç bit kaydırılacak
        bit_sayisi: Toplam bit sayısı
        """
        # Taşan bitleri sağa al
        mask = (1 << bit_sayisi) - 1
        sonuc = ((sayi << kayma_miktari) | (sayi >> (bit_sayisi - kayma_miktari))) & mask
        return sonuc
    
    def _alt_anahtarlari_uret(self):
        """
        Ana anahtardan 16 adet alt anahtar üretir.
        DES'teki key schedule algoritmasına benzer.
        """
        # Ana anahtarı ikiye böl (sol ve sağ parça)
        sol_parca = (self.ana_anahtar >> 32) & 0xFFFFFFFF  # Üst 32 bit
        sag_parca = self.ana_anahtar & 0xFFFFFFFF          # Alt 32 bit
        
        # Her tur için bir alt anahtar üret
        for tur in range(self.tur_sayisi):
            # Kaydırma miktarını belirle (DES'teki gibi bazı turlarda 1, bazılarında 2)
            if tur in [0, 1, 8, 15]:
                kayma = 1
            else:
                kayma = 2
            
            # Sol ve sağ parçaları kaydır
            sol_parca = self._sol_kaydirma(sol_parca, kayma, 32)
            sag_parca = self._sol_kaydirma(sag_parca, kayma, 32)
            
            # İki parçayı birleştir
            birlesik = (sol_parca << 32) | sag_parca
            
            # Permütasyon uygula
            alt_anahtar = self._bit_permutasyonu(birlesik, 64)
            
            # Tura özel bir değer ekle (daha fazla karmaşıklık için)
            alt_anahtar = (alt_anahtar + (tur * 12345)) % (2**64)
            
            # Alt anahtarı listeye ekle
            self.alt_anahtarlar.append(alt_anahtar)
    
    def rastgele_sayi_uret(self):
        """
        Alt anahtarları kullanarak rastgele sayı üretir.
        Her çağrıda farklı bir alt anahtar kullanılır.
        """
        # Mevcut turdaki alt anahtarı al
        alt_anahtar = self.alt_anahtarlar[self.mevcut_tur]
        
        # Bir sonraki tura geç (döngüsel olarak)
        self.mevcut_tur = (self.mevcut_tur + 1) % self.tur_sayisi
        
        # Alt anahtara permütasyon uygula
        rastgele_sayi = self._bit_permutasyonu(alt_anahtar, 64)
        
        return rastgele_sayi
    
    def aralik_sayi_uret(self, min_deger, maks_deger):
        """
        Belirtilen aralıkta rastgele sayı üretir.
        
        min_deger: Minimum değer (dahil)
        maks_deger: Maksimum değer (dahil)
        """
        # Rastgele sayı üret
        rastgele = self.rastgele_sayi_uret()
        
        # Belirtilen aralığa sığdır
        aralik = maks_deger - min_deger + 1
        sonuc = min_deger + (rastgele % aralik)
        
        return sonuc
    
    def alt_anahtarlari_goster(self):
        """
        Üretilen tüm alt anahtarları gösterir.
        Eğitim amaçlı - algoritmanın nasıl çalıştığını görmek için.
        """
        print("Üretilen Alt Anahtarlar:")
        print("-" * 70)
        for i, anahtar in enumerate(self.alt_anahtarlar):
            # Anahtarı hex formatında göster (daha okunabilir)
            print(f"Tur {i+1:2d}: {anahtar:016X} (Decimal: {anahtar})")


# Program başlangıcı
if __name__ == "__main__":
    print("=" * 70)
    print("DES Tarzı Anahtar Planlama Algoritması ile Rastgele Sayı Üreteci")
    print("=" * 70)
    print()
    
    # Kullanıcıdan ana anahtar al (isteğe bağlı)
    print("Ana anahtar girmek ister misiniz? (Enter'a basarsanız otomatik üretilir)")
    kullanici_girisi = input("Ana Anahtar (0-18446744073709551615 arası): ").strip()
    
    if kullanici_girisi:
        try:
            ana_anahtar = int(kullanici_girisi)
        except:
            print("Geçersiz giriş! Otomatik anahtar kullanılıyor.")
            ana_anahtar = None
    else:
        ana_anahtar = None
    
    print()
    
    # Algoritma nesnesini oluştur
    algoritma = AnahtarPlanlamaAlgoritmasi(ana_anahtar)
    
    print(f"Kullanılan Ana Anahtar: {algoritma.ana_anahtar}")
    print()
    
    # Alt anahtarları göster
    algoritma.alt_anahtarlari_goster()
    print()
    
    # Test 1: Ham rastgele sayılar
    print("=" * 70)
    print("Test 1: Alt Anahtarlardan Üretilen 5 Rastgele Sayı")
    print("=" * 70)
    for i in range(5):
        sayi = algoritma.rastgele_sayi_uret()
        print(f"{i+1}. Sayı: {sayi:016X} (Decimal: {sayi})")
    print()
    
    # Test 2: 1-100 arası rastgele sayılar
    print("=" * 70)
    print("Test 2: 1-100 Arası 10 Rastgele Sayı")
    print("=" * 70)
    for i in range(10):
        sayi = algoritma.aralik_sayi_uret(1, 100)
        print(f"{i+1}. Sayı: {sayi}")
    print()
    
    # Test 3: Zar atma simülasyonu
    print("=" * 70)
    print("Test 3: Zar Atma Simülasyonu (10 Atış)")
    print("=" * 70)
    zar_sonuclari = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in range(10):
        zar = algoritma.aralik_sayi_uret(1, 6)
        zar_sonuclari[zar] += 1
        print(f"{i+1}. Atış: {zar}")
    print()
    print("Zar Dağılımı:")
    for zar, adet in zar_sonuclari.items():
        print(f"  {zar}: {'█' * adet} ({adet})")
    print()
    
    # Test 4: Şifre üretimi
    print("=" * 70)
    print("Test 4: Rastgele Şifre Üretimi (8 Karakter)")
    print("=" * 70)
    karakterler = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%"
    for i in range(5):
        sifre = ""
        for j in range(8):
            index = algoritma.aralik_sayi_uret(0, len(karakterler) - 1)
            sifre += karakterler[index]
        print(f"{i+1}. Şifre: {sifre}")
    print()
    
    print("=" * 70)
    print("DES Tarzı Anahtar Planlama Algoritması Başarıyla Çalıştı!")
    print("=" * 70)
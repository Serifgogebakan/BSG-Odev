"""
Anahtar Dizisi Üreteci (Key Generator)
Basit Kriptografik Anahtar Üretim Algoritması
"""

import hashlib
import time


class AnahtarUreteci:
    """Basit anahtar üretim sınıfı"""
    
    def __init__(self, tohum=None):
        """Başlatıcı - tohum değeri ile başlar"""
        if tohum is None:
            # Otomatik tohum üret (zaman bazlı)
            self.tohum = int(time.time() * 1000000)
        else:
            self.tohum = tohum
        
        self.sayac = 0
    
    def _hash_uygula(self, veri):
        """SHA-256 hash fonksiyonu"""
        hash_obj = hashlib.sha256(str(veri).encode())
        return int(hash_obj.hexdigest(), 16)
    
    def _karistir(self, deger):
        """Bit kaydırma ve XOR ile karıştırma"""
        # Sağa 13 bit kaydır ve XOR
        adim1 = deger ^ (deger >> 13)
        # Sola 7 bit kaydır ve XOR
        adim2 = adim1 ^ (adim1 << 7)
        # Sağa 17 bit kaydır ve XOR
        adim3 = adim2 ^ (adim2 >> 17)
        return adim3
    
    def anahtar_uret(self, uzunluk=16):
        """
        Anahtar üretir
        
        Args:
            uzunluk: Anahtar uzunluğu (varsayılan 16)
            
        Returns:
            Hexadecimal anahtar dizisi
        """
        # Adım 1: Tohum ve sayacı birleştir
        baslangic = self.tohum ^ (self.sayac * 1000003)
        
        # Adım 2: Hash uygula
        hash_deger = self._hash_uygula(baslangic)
        
        # Adım 3: Karıştır
        karisik = self._karistir(hash_deger)
        
        # Adım 4: Zaman entropisi ekle
        zaman_entropi = int(time.time() * 1000000)
        sonuc = karisik ^ zaman_entropi
        
        # Adım 5: Son hash
        ham_anahtar = self._hash_uygula(sonuc)
        
        # Adım 6: Hexadecimal'e çevir ve uzunluğu ayarla
        hex_anahtar = hex(ham_anahtar)[2:].upper()
        if len(hex_anahtar) < uzunluk:
            hex_anahtar = hex_anahtar * ((uzunluk // len(hex_anahtar)) + 1)
        
        # Sayacı artır
        self.sayac += 1
        
        return hex_anahtar[:uzunluk]


# ÖRNEK KULLANIM
if __name__ == "__main__":
    print("=" * 60)
    print("ANAHTAR DİZİSİ ÜRETECİ")
    print("=" * 60)
    print()
    
    # Örnek 1: Otomatik tohum
    print("Örnek 1: Otomatik Tohum")
    print("-" * 60)
    uretec1 = AnahtarUreteci()
    print(f"Tohum: {uretec1.tohum}")
    print(f"Anahtar 1: {uretec1.anahtar_uret(16)}")
    print(f"Anahtar 2: {uretec1.anahtar_uret(16)}")
    print()
    
    # Örnek 2: Özel tohum
    print("Örnek 2: Özel Tohum (123456)")
    print("-" * 60)
    uretec2 = AnahtarUreteci(tohum=123456)
    print(f"Tohum: {uretec2.tohum}")
    print(f"Anahtar: {uretec2.anahtar_uret(32)}")
    print()
    
    # Örnek 3: Farklı uzunluklar
    print("Örnek 3: Farklı Uzunluklar")
    print("-" * 60)
    uretec3 = AnahtarUreteci()
    print(f"8 karakter:  {uretec3.anahtar_uret(8)}")
    print(f"16 karakter: {uretec3.anahtar_uret(16)}")
    print(f"32 karakter: {uretec3.anahtar_uret(32)}")
    print()
    
    print("=" * 60)

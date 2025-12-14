#  Auto LinkedIn - İş Arama Çilesine Son (BİL403 Projesi)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![PyQt5](https://img.shields.io/badge/Arayüz-PyQt5-green.svg)
![Status](https://img.shields.io/badge/Durum-Tamamlandı-success.svg)

Selamlar!  Bu proje, **İstanbul Medeniyet Üniversitesi - Yazılım Mühendisliği (BİL403)** dersi kapsamında, iş arama sürecini biraz olsun kolaylaştırmak (ve manuel filtrelemeden kurtulmak) için geliştirdiğimiz dönem projesidir.

##  Olayımız Ne?
Biliyorsunuz LinkedIn'de binlerce ilan var ama hangisi bize tam uyuyor bulmak samanlıkta iğne aramak gibi. Biz de dedik ki; **"Biz tek tek aramayalım, kodlar bizim yerimize profille ilanı eşleştirsin."**

**Auto LinkedIn**, senin girdiğin yetenekleri ve tecrübeleri alıyor; elindeki ilan veri setiyle **Doğal Dil İşleme (NLP)** kullanarak kıyaslıyor ve sana "Bak bu ilan tam senlik!" dediği sonuçları getiriyor.

---

##  Neler Yapabiliyor?

* ** CSV ile Çalışır:** LinkedIn'den çektiğin veya elindeki iş ilanı veri setini (CSV) şak diye yüklersin.
* ** Serbest Profil Girişi:** "Python biliyorum, 2 yıl tecrübem var, AWS de kullandım" gibi kendini anlatan metni girersin.
* ** Akıllı Eşleştirme:** Arka planda **TF-IDF** ve **Cosine Similarity** çalıştırıyoruz. Yani sadece kelimeye bakmıyor, metin benzerliği kurup en mantıklı olanları puanlıyor.
* **dark Mode Sevenlere:** Gözümüz yorulmasın diye arayüzü koyu tema (Dark Theme) yaptık.
* ** Tek Tıkla Başvuru:** İlanı beğendiysen program içinden direkt tarayıcıda açıp başvurabilirsin.

---

##  Proje Kapsamı? (Teknik Kısım)

Projeyi geliştirirken **Scrum** taktikleri uyguladık, 3 sprint koştuk ve şu teknolojileri kullandık:

* **Python:** Olmazsa olmazımız 
* **PyQt5:** Masaüstü arayüzünü (GUI) bununla tasarladık.
* **Pandas:** O kadar veriyi, CSV dosyasını evirip çevirmek, temizlemek için.
* **Scikit-learn:** İşin büyüsü burada. Metinleri vektöre çevirip (TF-IDF) benzerlik hesaplamak (Cosine Similarity) için kullandık.

---




## 📸 Ekran Görüntüleri

Uygulamamızdan birkaç kare:
<img width="601" height="377" alt="Ekran görüntüsü 2025-12-15 003450" src="https://github.com/user-attachments/assets/15186540-4180-49ed-8765-3670f22e1cd7" />
<img width="604" height="381" alt="Ekran görüntüsü 2025-12-15 003515" src="https://github.com/user-attachments/assets/cc59cafd-681c-417b-a5f0-ab3f78c97d92" />
<img width="598" height="375" alt="Ekran görüntüsü 2025-12-15 003533" src="https://github.com/user-attachments/assets/370ce132-53ea-4033-859c-02f0e9b0ef11" />
<img width="584" height="366" alt="Ekran görüntüsü 2025-12-15 003550" src="https://github.com/user-attachments/assets/ce967c43-aca0-4545-9abd-04b6b8f24d23" />
<img width="597" height="369" alt="Ekran görüntüsü 2025-12-15 003559" src="https://github.com/user-attachments/assets/fc023a93-a458-4916-b9bd-293ff681e724" />



##  Ekip (Credits)

Bu projeyi BİL403 dersi için şu ekip geliştirdi:

* **Seferhan Kaya**
* **Alper Akpınar**
* **Buğrahan Ata**

**Danışman:** Dr. Öğr. Üyesi Ertürk Erdağı


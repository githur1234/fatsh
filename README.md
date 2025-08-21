# Fatsh

**Fatsh**, port yönlendirme (port forwarding), VPN, NAT geçişi gibi zahmetli adımlara gerek kalmadan hızlıca **bind shell oturumu kazanmanızı** sağlayan bir araçtır. Otomatik ngrok tüneli açar, webhook üzerinden bağlantı bilgilerini gönderir ve tek komutla hedef sistemle etkileşime geçmenizi mümkün kılar.

---

## 🚀 Özellikler

* 🔒 **Ngrok HTTP tüneli** ile güvenli bağlantı sağlar
* 📡 **Webhook URL’sine** otomatik olarak bağlantı URL’sini gönderir
* ⚙️ Kurulum gerektirmez, çalıştır ve kullan
* 🐚 Basit **bind shell komut arayüzü**
* 🔁 Versiyon kontrolü yaparak güncelleme olup olmadığını bildirir

---

##  Nasıl Çalışır?

1. `fatsh`, `ngrok` üzerinden yerel 65534 portunu internete açar.
2. Oluşan ngrok HTTP adresini, sizin belirlediğiniz **webhook URL’sine** POST eder.
3. Bu adres üzerinden HTTP GET parametresiyle (`/?cmd=ls`) bind shell komutları gönderilir.
4. Gelen çıktılar JSON formatında döner (`{"result": "komut çıktısı"}`).

---

## ⚙️ Kurulum ve Kullanım
Eğer Linux yada MacOs kullanıyorsanız:
```bash
git clone https://github.com/githur1234/fatsh.git
cd fatsh
bash ./setup.sh
```

# Not:
kurulumda setup.sh otomatik olarak py dosyasını çalıştırır diğer kullanımlarda ise
```bash
    bash fatsh
```
komutunu çalıştırmanız yeterlidir

### İlk kullanımda:

* Webhook adresiniz sorulur
* Ngrok Auth token’ınız alınır
* Tüm bilgiler `config.json` içerisine kaydedilir

---

## 📡 Webhook Kullanımı

Webhook, genellikle `webhook.site` veya Discord gibi sistemler üzerinden kullanılabilir. Ngrok adresi aşağıdaki gibi bir JSON body ile post edilir:

```json
{
  "ngrok": "http://1a2b3c4d5e.ngrok.io"
}
```

---

## 🐚 Bind Shell Kullanımı

### Shell oluşturmak:

```text
[1] make bind shell
```

Belirttiğiniz yola shell kodu yazılır.

### Shell'e bağlanmak:

```text
[2] connect bind shell
```

Ngrok URL'si girilir ve ardından direkt komut yazıp çalıştırabilirsiniz.

---
### Config ayarları değişimi
Bunun 2 yolu vardır 
#### 1 Manuel(zor yol) 
1. Projenin içinde 'fatsh/fatsh/config.json' 
 Dosyasına gidin.

2. Web hook yazan yere yeni Web hook adresinizi ngrok yerine ngrok authtokenini yazınız

Not:Bu yöntem eğer webhook yada ngrok değişkenlerinden biri değişmediyse ve diğeri değişti ise tek yolunuzdur değişeni yenisi ile değiştirin yeter

#### 2 Otomatik yol
Açıklamaya gerek yok eğer gui kullanıyorsanız change Config ve yeni değerler, Eğer cli kullanıyorsanız 3. Seçenek ve yeni değerler

Ve Config ayarlarınızı başarıyla değiştirdiniz 
## 🛡️ Uyarı

> **Yasal uyarı**: Bu araç sadece eğitim ve test amaçlıdır. Yalnızca **izinli** sistemlerde kullanın. Geliştirici hiçbir illegal kullanımda sorumluluk kabul etmez.

---

## 🧪 Örnek Kullanım

```bash
fatsh@user>> 2
ngrok url: http://1a2b3c4d5e.ngrok.io
shell>> whoami
shell>> uname -a
```

---

## 📦 Bağımlılıklar

* Python 3.8+
* `requests`
* `colorama`
* `ngrok` (Python paketi)
* `shell.py` (proje içinde)

---

## 📁 Yapı

```
fatsh/
├── fatsh/
    ├── fatsh.py
    ├── shell.py
    ├── config.json
    ├── requirements.txt
├── README.md
|__ vs.txt
```

---

## 📌 Yol Haritası (TODO)

* [*] Gui Desteği
* [ ] Çoklu shell yönetimi
* [ ] Reverse shell modülü
* [ ] Güncelleme otomasyonu
* [ ] bluezero otomasyonu
---

## 🧑‍💻 Geliştirici

* [githur1234](https://github.com/githur1234)

---

Eğer bu anlatıcı ile alaklı mantık hatası bulduysanız yada eksiklikler varsa  bize bildirmekten çekinmeyin

[ffurkanbatum@gmail.com](mailto:furkan@gmail.com) 

## Not:
Yakında çoklu shell yönetimi ile fatsh esneteceğiz takip de kalın

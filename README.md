# TimeBTC

Bu proje, Yahoo Finance ve CoinGecko kaynaklarından Bitcoin fiyat verilerini toplayarak tek bir CSV dosyasında (combined_bitcoin_data.csv) depolamayı amaçlamaktadır. Proje, **Selenium** ve **requests** kütüphanelerini kullanarak iki farklı kaynaktan veri çekmektedir.

## Gereksinimler

Projeyi çalıştırmadan önce aşağıdaki gereksinimlerin yüklü olduğundan emin olun:

1. **request**: Phyton kütüphanesi
2. **Selenium**: Phyton kütüphanesi

## Projeyi Klonlayın

Öncelikle projeyi kendi bilgisayarınıza klonlayın. Git yüklü değilse, [Git'i buradan](https://git-scm.com/) indirip kurabilirsiniz.
```bash
git clone https://github.com/kullaniciadi/proje-adi.git
cd proje-adi
```
>Bu adım, proje dosyalarını yerel makinenize indirir ve proje dizinine geçiş yapar.

## PHYTON Kurulumu

Projeyi çalıştırmak için **PHYTON'IN** bilgisayarınızda yüklü olması gerekir. Aşağıdaki adımları izleyerek kurulumu tamamlayın:

1. [PHYTON'I](https://www.python.org/downloads/) indirin ve indirilen dosyayı çalıştırarak ekrandaki talimatları izleyin.

>Bu adım, Phyton'ın doğru şekilde yüklendiğini kontrol etmek için önemlidir.

## Kütüphane Yüklemeleri

Projede kullanılan kütüphaneleri yüklemek için, aşağıdaki adımları izleyerek her birini doğru şekilde kurduğunuzdan emin olun:

### 1. Selenium ve Request Kütüphaneleri

Bilgisayarınızda terminal açın ve aşağıdaki komutları kullanarak kütüphaneleri kurun.

```bash
pip install selenium
pip install request
```

#### 1.1. ChromeDriver Kurulumu

[ChoremeDriver'ı](https://medium.com/@melisacevik13/chromedriver-kurulumu-ve-selenium-kullanımı-fb75da2a9ca3) bu medium yazısını takip ederek indirin.

## Projeyi Çalıştırma

Artık projeyi çalıştırabilmek için tek yapmanız gereken dosyalardaki **driver_path** değişkenine ChromeDriver'ı indirdiğiniz yolu vermektir.

## Hazırlayanlar

- 221307020 - Sude Deniz SUVAR
- 221307007 - Şevval Zeynep Ayar

## Teşekkürler
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)
- [Medium](https://medium.com/@melisacevik13/chromedriver-kurulumu-ve-selenium-kullanımı-fb75da2a9ca3)
- [W3docs](https://www.w3schools.com/python/module_requests.asp)


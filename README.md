# El Hareketleriyle Çizim Uygulaması

Bu proje, OpenCV ve MediaPipe kullanarak el hareketleriyle etkileşimli bir çizim uygulaması geliştirmeyi amaçlamaktadır. Uygulama, işaret parmağının hareketini takip ederek çizim yapmanıza olanak tanır ve beş parmağın tamamı açık olduğunda çizimi durdurur. Ayrıca, ekranda "Kalem" ve "Silgi" butonları aracılığıyla çizim modları arasında geçiş yapabilirsiniz.

## Özellikler

- **Gerçek Zamanlı El Takibi:** MediaPipe sayesinde el ve parmaklar anlık olarak takip edilir.
- **Çizim Modu:** Sadece işaret parmağınız uzatılmış (baş parmak kapalıyken) olduğunda çizim yapabilirsiniz.
- **Silgi Modu:** Ekrandaki "Silgi" butonuna dokunulduğunda tüm çizimler temizlenir.
- **Kullanıcı Dostu Arayüz:** Ekranın sol üst köşesinde bulunan butonlar ile modlar arasında geçiş yapabilirsiniz.

## Gereksinimler

- Python 3.x
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [NumPy](https://pypi.org/project/numpy/)

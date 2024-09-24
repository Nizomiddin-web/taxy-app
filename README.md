# Loyihani Nomi: Taxy-app

## Loyihaning Tavsifi
Taxy-app loyihasi, taksilarni onlayn tarzda buyurtma qilish va boshqarish imkonini beruvchi mobil ilova yoki veb ilovadir. Loyihada to'lov tizimlari integratsiyalangan bo'ladi, bu foydalanuvchilarga oson va qulay to'lov imkoniyatlarini taqdim etadi.

---

## Talablar
- **Django**: Veb ilovangizning backend qismida ishlash uchun.
- **Django REST Framework**: RESTful API yaratish uchun.
- **PostgreSQL**: Ma'lumotlar bazasi sifatida.
- **Redis**: Kesh uchun.
- **Stripe / Payme**: To'lov tizimi sifatida (tanlovga qarab).
- **Python**: Backend dasturlash tili.
- **JavaScript / HTML / CSS**: Frontend dasturlash uchun (agar frontend ham ishlab chiqilsa).

---

## Ishga Tushirish Ko'rsatmalari
1. **Loyihani Klonlash**
     ```bash
   git clone <repo_url>
   cd taxy-app

   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
2. **Kerakli kutubxonalarni o'rnatish**
      ```bash 
      pip install -r requirements.txt
3. **Ma'lumotlar Bazasi Sozlamalari** settings.py faylini oching va ma'lumotlar bazasi sozlamalarini o'zgartiring.

4. **Ma'lumotlar bazasini yaratish:**
      ```bash 
      python manage.py migrate

5. **Superuser Yaratish**
      ```bash 
      python manage.py createsuperuser
6. **Ilovani Ishga Tushirish**
      ```bash 
      python manage.py runserver




  

 




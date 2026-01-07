# tvheadend-epg-backend-260103
EPG backend integration to download TVHeadend EPG datas

# TVHeadend EPG – Home Assistant Integration + Timeline Card

Ez a projekt egy **Home Assistant custom integrációt** és egy hozzá tartozó
**idősávos (timeline) EPG Lovelace kártyát** valósít meg **TVHeadend** szerverhez.

A megoldás célja egy **gyors, modern, scrollozható műsorújság**, amely:
- nem szenzorban tárolja az EPG adatokat,
- WebSocketen keresztül szolgálja ki a UI-t,
- és teljesen elkülöníti az adatlekérést a megjelenítéstől.

---

## ✨ Funkciók

### Backend (Home Assistant integráció)
- TVHeadend EPG lekérés HTTP API-n keresztül
- 15 percenkénti automatikus frissítés
- Kézi frissítés szolgáltatáson keresztül
- EPG adatok tárolása HA Store-ban (nem szenzorban)
- WebSocket API a frontend számára
- Felvétel indítása műsorra kattintva
- Teljesen eltávolítható integráció

### Frontend (Lovelace custom card)
- Idősávos (timeline) EPG nézet
- Vízszintes és függőleges scroll
- Fix csatornaoszlop
- Aktuális időt jelző „now-line”
- Csatorna és cím szerinti szűrés
- Kártya megnyitásakor azonnali EPG frissítés

---

## 📁 Repository struktúra


---

## 🚀 Telepítés

### 1️⃣ HACS (ajánlott)

1. HACS → Integrations → Custom repositories
2. Add hozzá ezt a repositoryt:
   - Type: `Integration`
3. Telepítsd a **TVHeadend EPG** integrációt
4. HACS → Frontend → Telepítsd a kártyát
5. Home Assistant újraindítás

---

### 2️⃣ Manuális telepítés

#### Backend

Másold a `custom_components/tvheadend_epg` könyvtárat ide:

config/custom_components/


#### Frontend

Használd a TVHeadend-EPG-Card tárolót az EPG kártya hozzáadásához:

https://github.com/rhetesi/tvheadend-epg-card
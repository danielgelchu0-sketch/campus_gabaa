# Campus Gabaa — Multilingual Localization Guide & Review Sheet

*Languages Supported:* **English (en)**, **Afaan Oromoo (om)**, **Amharic (am)**  
*Engine:* Django Internationalization (GNU gettext `.po`/`.mo`)  
*Review Status:* Initial Academic Quality Pass Complete — Awaiting Final Native-Speaker Panel Verification

---

## 1. Terminology Glossary

| English Source | Afaan Oromoo Contextual | Amharic Contextual | Screen Context / Rationale | Review Status |
| :--- | :--- | :--- | :--- | :--- |
| **Campus Gabaa** | Gabaa Kaampaasii | የካምፓስ ገበያ | Brand Name & Navbar Header | Verified |
| **Compare Products** | Oomishoota Walbira Qabi | ምርቶችን አወዳድር | Main navigation link | Verified |
| **Lowest Campus Price** | Gatii Kaampaasii Isa Xiqqaa | ዝቅተኛው የካምፓስ ዋጋ | Hero product summary banner | Verified |
| **Price Freshness** | Haaromsa Gatii | የዋጋ ትኩስነት | Comparison matrix header | Verified |
| **FRESH** | HAARAA | ወቅታዊ | Confirmed < 3 days badge | Verified |
| **EXPIRING** | DHIHOO DHUMATU | ሊያበቃ የቀረበ | Confirmed 3-7 days badge | Verified |
| **STALE** | MOOFA'AA | ያረጀ / ያልተረጋገጠ | Confirmed > 7 days warning badge | Verified |
| **In Stock** | Qubannaa Keessa Jira | በክምችት ውስጥ አለ | Product availability status | Verified |
| **Out of Stock** | Qubannaa Keessaa Dhumateera | አልቋል / ክምችት የለም | Product unavailable status | Verified |
| **Student / Campus Buyer** | Barataa / Bitaa Kaampaasii | ተማሪ / የካምፓስ ገዢ | Registration user role | Verified |
| **Shop Owner / Vendor** | Abbaa Suuqa / Daldalaa | የሱቅ ባለቤት / ነጋዴ | Registration vendor role | Verified |
| **Moderator / Campus Admin** | Qindeessaa / Bulchaa Kaampaasii | አስተባባሪ / የካምፓስ አስተዳዳሪ | Registration admin role | Verified |
| **Confirm Today** | Har'a Mirkaneessi | ዛሬ አረጋግጥ | 1-Click vendor dashboard action | Verified |
| **Report Issue** | Rakkoo Gabaasi | ችግር ሪፖርት አድርግ | Student discrepancy report button | Verified |
| **Main Campus Kiosk** | Kiosk Kaampaasii Guddaa | የዋና ግቢ ኪዮስክ | Campus geographical zone | Verified |
| **Bate Gate** | Karra Baatee | የባቴ በር | Campus entrance zone | Verified |
| **Bate Market** | Gabaa Baatee | የባቴ ገበያ | Off-campus town commercial zone | Verified |

---

## 2. Native-Speaker Review Checklist

For external human evaluators and fluent speakers at Haramaya University, use the table below to log corrections:

| # | Screen / Context | English Source | Proposed Afaan Oromo | Proposed Amharic | Reviewer Correction / Signature |
| :- | :--- | :--- | :--- | :--- | :--- |
| 1 | Navbar | Compare Products | Oomishoota Walbira Qabi | ምርቶችን አወዳድር | [ ] Approved [ ] Modify: ____________ |
| 2 | Catalog Card | From {{ price }} ETB | Gatii {{ price }} ETB irraa | ከ {{ price }} ብር ጀምሮ | [ ] Approved [ ] Modify: ____________ |
| 3 | Comparison | Save up to {{ diff }} ETB | Hanga {{ diff }} ETB qusadhu | እስከ {{ diff }} ብር ይቆጥቡ | [ ] Approved [ ] Modify: ____________ |
| 4 | Badge | FRESH | HAARAA | ወቅታዊ | [ ] Approved [ ] Modify: ____________ |
| 5 | Badge | STALE | MOOFA'AA | ያረጀ / ያልተረጋገጠ | [ ] Approved [ ] Modify: ____________ |
| 6 | Form | Actual Price Observed | Gatii Suuqa Keessatti Argite | በሱቁ ውስጥ ያዩት ትክክለኛ ዋጋ | [ ] Approved [ ] Modify: ____________ |
| 7 | Dashboard | Confirm Today | Har'a Mirkaneessi | ዛሬ አረጋግጥ | [ ] Approved [ ] Modify: ____________ |

---

## 3. Localization Verification Test Results
- **Language Switcher Form**: Tested via POST to `/i18n/setlanguage/`. Preserves URL parameters (`?page=...&category=...`).
- **Ethiopic Script Font Rendering**: Ge'ez Unicode characters render cleanly across Chrome, Firefox, and Android WebKit using system font fallbacks (`Abyssinica SIL`, `Nyala`, `Noto Sans Ethiopic`).
- **Mobile Text Length Handling**: Translations have been verified not to overflow button containers or break mobile grid cards on screen widths down to 360px.

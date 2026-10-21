"""
Campus Gabaa Localization Pipeline
Populates authentic Afaan Oromo and Amharic translations into Django .po files
and compiles them into binary .mo catalogs.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Contextual Dictionary for Afaan Oromo (om)
TRANSLATIONS_OM = {
    # Navigation & Actions
    "Compare Products": "Oomishoota Walbira Qabi",
    "Campus Shops": "Suuqota Kaampaasii",
    "About & Methodology": "Waa'ee fi Akkaataa Hojii",
    "FAQ": "Gaaffiilee fi Deebii",
    "Frequently Asked Questions": "Gaaffiilee Yeroo Baay'ee Gaafataman",
    "Sign In": "Seeni",
    "Sign Out": "Ba'i",
    "Register": "Galmaa'i",
    "Create Account": "Herrega Bani",
    "Profile & Settings": "Piroofayilii fi Qindaa'ina",
    "Catalog": "Kataloogii",
    "Shops Directory": "Tarree Suuqotaa",
    "Academic Capstone": "Pirojektii Eebbaa",
    "FAQ & Pricing Rules": "Gaaffiilee fi Qajeelfama Gatii",
    "System Health": "Fayyaa Sirnichaa",
    "Signed in as": "Akka kanaatti seente:",
    "Vendor": "Daldalaa",
    "Admin": "Bulchaa",
    "Shop Dashboard": "Gabatee To'annoo Suuqa",
    "Moderation Queue": "Tarree Qorannoo fi Mirkaneessa",
    "Suggest Product": "Oomisha Dhiyeessi",
    "Django Admin": "Bulchiinsa Diiyaangoo",

    # Homepage & Discovery
    "Home": "Fuula Duraa",
    "Haramaya University & Bate Community Platform": "Sirna Hawaasa Yuunivarsiitii Haramayaa fi Baatee",
    "Compare Campus Prices & Discover Everyday Essentials": "Gatii Kaampaasii Walbira Qabi, Meeshaalee Barbaachisoo Argadhu",
    "Don't overpay or wander between kiosks. Discover stationery, electronics, toiletries, snacks, and print services across Main Campus and Bate with transparent freshness indicators.": "Gatii dabalataa hin kaffalin, kiosks gidduu hin dadhabin. Meeshaalee barnootaa, elektirooniksii, qulqullinaa, nyaata fi tajaajila maxxansaa Kaampaasii Guddaa fi Baatee keessaa mallattoo haaromsa gatii ifaa waliin argadhu.",
    "Search exercise books, flash drives, soap, biscuits, printing...": "Daftara, filaashii, saamunaa, biskutii, maxxansa barbaadi...",
    "Compare": "Walbira Qabi",
    "Popular:": "Beekamoo:",
    "Exercise Books": "Daftaroota",
    "USB Flash Drives": "Filaashii USB",
    "Lifebuoy / Soap": "Saamunaa",
    "Printing Services": "Tajaajila Maxxansaa",
    "Catalog Products": "Oomishoota Kataloogii",
    "Campus & Bate Shops": "Suuqota Kaampaasii fi Baatee",
    "Price Verifications This Week": "Gatii Torban Kana Mirkanaa'e",
    "Consumer Protection for Students": "Eegumsa Barattootaa",
    "Never Rely on Outdated Prices Again": "Lammata Gatii Moofa'etti Hin Amanamin",
    "Campus Gabaa eliminates guesswork. Every listing features an automated freshness timestamp so students know whether a price is current before walking across campus or taking a bajaj to town.": "Gabaan Kaampaasii tilmaama dhabamsiisa. Tokkoon tokkoon gatii mallattoo haaromsaa waan qabuuf barattoonni gara suuqa deemuu ykn baajaajii kireeffachuu dura gatiin sun ammayyaa ta'uu beeku.",
    "FRESH": "HAARAA",
    "EXPIRING": "DHIHOO DHUMATU",
    "STALE": "MOOFA'AA",
    "Verified by shop owner within the last 3 days.": "Abbaa suuqaatiin guyyoota 3 darban keessatti mirkanaa'e.",
    "Confirmed 3 to 7 days ago. Price may shift.": "Guyyoota 3 hanga 7 dura mirkanaa'e. Gatiin jijjiiramuu danda'a.",
    "Unconfirmed for over 7 days. Report if incorrect!": "Guyyoota 7 oliif hin mirkanoofne. Dogoggora yoo ta'e gabaasi!",
    "Crowd-Sourced Accuracy Verification": "Qulqullina Hawaasaan Mirkanaa'u",
    "If a kiosk owner charges more than listed or an item is out of stock, any student can submit an instant report. Our moderation queue contacts the merchant or updates the record.": "Abbaan suuqaa gatii caalu yoo gaafate ykn meeshaan yoo dhumate, barataan kamiyyuu battalumatti gabaasuu danda'a. Koreen qorannoo daldalaa waliin dubbachuun sirreessa.",
    "Built specifically for Haramaya University's decentralized kiosk layout across Main Campus, Agriculture Campus, and Bate Market.": "Addatti Kaampaasii Guddaa, Kaampaasii Qonnaa fi Gabaa Baatee Yuunivarsiitii Haramayaatiif qophaa'e.",
    "Browse by Campus Need": "Akka Fedhii Kaampaasiitti Filadhu",
    "Filter products tailored to daily student life and study requirements": "Meeshaalee jireenya barattootaa fi barnootaaf barbaachisan calali",
    "View All Products": "Oomishoota Hunda Ilaali",
    "items": "meeshaalee",
    "Top Comparisons": "Oomishoota Irra Deddeebiin Walbira Qabaman",
    "Compare Across Multiple Shops": "Suuqota Hedduu Keessatti Walbira Qabi",
    "Products with verified listings in 2 or more campus shops": "Oomishoota suuqota lamaa fi isaa ol keessatti gatiin isaanii mirkanaa'e",
    "Full Catalog": "Kataloogii Guutuu",
    "From": "Jalqabee",
    "shops": "suuqota",
    "Are You a Campus Merchant or Kiosk Owner?": "Ati Daldalaa Kaampaasii Yookiin Abbaa Suuqaatii?",
    "List your store on Campus Gabaa for free. Connect with thousands of Haramaya University students, increase your sales, and keep your prices transparent and verified.": "Suuqa kee bilisaan Gabaa Kaampaasii irratti galmeessi. Barattoota Yuunivarsiitii Haramayaa kumaatama waliin walqunnami, gurgurtaa kee guddisi, gatii kees ifa godhi.",
    "Manage My Shop": "Suuqa Koo To'adhu",
    "Register Your Shop": "Suuqa Kee Galmeessi",

    # Forms & Inputs
    "Search Term": "Jecha Barbaadaa",
    "Category": "Ramaddii",
    "All Categories": "Ramaddii Hunda",
    "Campus Zone": "Naannoo Kaampaasii",
    "All Campus Zones": "Naannoo Kaampaasii Hunda",
    "Sort By": "Akka kanaan Qindeessi",
    "Price: Lowest First": "Gatii: Xiqqaa Irraa Kaasi",
    "Price: Highest First": "Gatii: Guddaa Irraa Kaasi",
    "Name: A to Z": "Maqaa: A hanga Z",
    "Recently Updated": "Dhiheenya Kan Haarome",
    "In Stock Only": "Qubannaa Keessa Qofa",
    "In Stock": "Qubannaa Keessa Jira",
    "Out of Stock": "Qubannaa Keessaa Dhumateera",
    "Fresh Prices Only (< 7 days)": "Gatiiwwan Haaraa Qofa (< guyyoota 7)",
    "Reset": "Haquu / Deebisi",
    "Apply Filters": "Calaltuu Hojiirra Oolchi",
    "Suggest New Product": "Oomisha Haaraa Dhiyeessi",

    # Product Detail & Comparison Table
    "Price Comparison": "Gatii Walbira Qabuu",
    "Lowest Campus Price": "Gatii Kaampaasii Isa Xiqqaa",
    "Price Range Across Shops": "Giddu-galeessa Gatii Suuqotaa",
    "Save up to": "Hanga kana qusadhu:",
    "Where to Buy Near Haramaya Campus": "Yuunivarsiitii Haramayaa Naannotti Eessaa Bitanna",
    "Ranked by lowest price. Check the freshness badge before visiting the shop.": "Gatii xiqqaa irraa eegalee tartiibeffame. Suuqa deemuu dura mallattoo haaromsaa ilaali.",
    "Sell This at My Shop": "Kanas Suuqa Kootti Nan Gurgura",
    "Shop & Campus Zone": "Suuqa fi Naannoo Kaampaasii",
    "Exact Landmark": "Bakka Qabatamaa fi Mallattoo",
    "Price": "Gatii",
    "Price Freshness": "Haaromsa Gatii",
    "Contact & Actions": "Qunnamsiisa fi Tarkaanfii",
    "Confirmed today": "Har'a mirkanaa'e",
    "Report Issue": "Rakkoo Gabaasi",
    "Recent Price Verification History": "Seenaa Mirkaneessa Gatii Dhiheenyaa",
    "Previous Price (ETB)": "Gatii Duraanii (ETB)",
    "Updated Price (ETB)": "Gatii Haarome (ETB)",
    "Modified By": "Kan Fooyyesse",
    "Change Notes": "Yaada Jijjiiramaa",

    # Account & Profile
    "Choose Your Campus Role": "Gahee Kaampaasii Kee Filadhu",
    "Student / Campus Buyer": "Barataa / Bitaa Kaampaasii",
    "Shop Owner / Vendor": "Abbaa Suuqa / Daldalaa",
    "Moderator / Campus Admin": "Qindeessaa / Bulchaa Kaampaasii",
    "First Name": "Maqaa",
    "Father / Last Name": "Maqaa Abbaa",
    "Email Address": "Teessoo Imeelii",
    "Phone Number": "Lakkoofsa Bilbilaa",
    "Campus ID / Dorm or Department": "Eenyummaa Kaampaasii / Kutaa Ciisichaa",
    "Preferred Language": "Afaan Filatame",
    "Password": "Jecha Iccitii",
    "Confirm Password": "Jecha Iccitii Mirkaneessi",
    "Complete Registration": "Galmee Xumuri",
    "Already registered?": "Kanaan dura galmoofteettaa?",
    "Welcome Back": "Baga Nagaan Deebite",
    "Sign in to manage your campus kiosk or submit price reports": "Kiosk kee to'achuuf ykn gabaasa dhiyeessuuf seeni",
    "Enter your username": "Maqaa fayyadamaa galchi",
    "Enter password": "Jecha iccitii galchi",
    "Don't have an account yet?": "Herrega hin qabduu?",
    "Create Free Account": "Herrega Bilisaa Bani",
    "Save Profile Changes": "Jijjiirama Galmeessi",

    # Moderation & Vendor Dashboard
    "Shop Inventory & Price Freshness Controls": "Meeshaalee Suuqa fi Haaromsa Gatii",
    "Confirm Today": "Har'a Mirkaneessi",
    "Edit Price": "Gatii Fooyyessi",
    "Add Product Listing": "Oomisha Dabaladhu",
    "Edit Shop Profile": "Suuqa Fooyyessi",
    "View Public Storefront": "Fuula Suuqa Uummataa Ilaali",
    "Total Inventory Items": "Oomishoota Suuqa Hunda",
    "Currently In Stock": "Amma Qubannaa Keessa Jira",
    "Requires Price Confirmation": "Gatii Mirkaneessuu Barbaada",
    "Pending Price Reports": "Gabaasaalee Eegamaa Jiran",
    "Shops Pending Verification": "Suuqota Mirkaneessa Eegan",
    "Reports Resolved": "Gabaasaalee Furmaata Argatan",
    "User-Submitted Listing Reports": "Gabaasaalee Barattoonni Dhiyeessan",
    "Pending": "Eegamaa",
    "Resolved": "Furmaata Argate",
    "Dismissed": "Kan Haqame",
    "All": "Hunda",
    "Inspect": "Qoradhu",
    "Approve": "Mirkaneessi",
    "Reject": "Didi",
    "Report Listing Discrepancy": "Garaagarummaa Gatii Gabaasi",
    "Submit Report": "Gabaasa Ergi",
    "Actual Price Observed in Shop (ETB)": "Gatii Suuqa Keessatti Argite (ETB)",
    "Details & Description": "Ibsa fi Bal'ina",
    "Optional Receipt or Storefront Photo": "Suuraa Nagahee ykn Suuqa (Filannoodha)",
    "Take Moderation Action": "Tarkaanfii Qorannoo Fudhadhu",
    "Submit Moderation Decision": "Murtee Galchi",
    "Unit of Measure": "Safartuu Oomishaa",
    "Piece / Item": "Kudhaama / Qeenxee",
    "Pack / Bundle": "Paakkii / Hidhaa",
    "Box / Carton": "Saanduqa / Kaartoonii",
    "Kilogram (kg)": "Kiiloogiraama (kg)",
    "Liter (L)": "Liitira (L)",
    "Page (Printing)": "Fuula (Maxxansa)",
    "Set": "Kite",
    "Haramaya Main Campus (Dorm / Admin Kiosks)": "Kaampaasii Guddaa Haramayaa (Kiosk Ciisichaa)",
    "Bate Gate / Campus Entrance": "Karra Baatee / Balbala Kaampaasii",
    "Bate Town Center & Market": "Giddugala Magaalaa fi Gabaa Baatee",
    "Haramaya Town Commercial Area": "Naannoo Daldalaa Magaalaa Haramayaa",
    "Agriculture & Veterinary Campus Zone": "Naannoo Kaampaasii Qonnaa fi Fayyaa Beeyladaa",
}

# Contextual Dictionary for Amharic (am)
TRANSLATIONS_AM = {
    # Navigation & Actions
    "Compare Products": "ምርቶችን አወዳድር",
    "Campus Shops": "የካምፓስ ሱቆች",
    "About & Methodology": "ስለ እኛ እና የአሠራር ዘዴ",
    "FAQ": "ተደጋጋሚ ጥያቄዎች",
    "Frequently Asked Questions": "በተደጋጋሚ የሚጠየቁ ጥያቄዎች",
    "Sign In": "ግባ",
    "Sign Out": "ውጣ",
    "Register": "ተመዝገብ",
    "Create Account": "አካውንት ፍጠር",
    "Profile & Settings": "መገለጫ እና ቅንብሮች",
    "Catalog": "ካታሎግ",
    "Shops Directory": "የሱቆች ማውጫ",
    "Academic Capstone": "የምረቃ ጥናት ፕሮጀክት",
    "FAQ & Pricing Rules": "ጥያቄዎችና የዋጋ ደንቦች",
    "System Health": "የስርዓቱ ጤና",
    "Signed in as": "በዚህ ስም ገብተዋል:",
    "Vendor": "ነጋዴ",
    "Admin": "አስተዳዳሪ",
    "Shop Dashboard": "የሱቅ መቆጣጠሪያ ሰሌዳ",
    "Moderation Queue": "የቁጥጥር እና ማረጋገጫ ዝርዝር",
    "Suggest Product": "አዲስ ምርት ጠቁም",
    "Django Admin": "የጃንጎ አስተዳዳሪ",

    # Homepage & Discovery
    "Home": "ዋና ገጽ",
    "Haramaya University & Bate Community Platform": "የሐረማያ ዩኒቨርሲቲ እና የባቴ ማህበረሰብ መድረክ",
    "Compare Campus Prices & Discover Everyday Essentials": "የካምፓስ ዋጋዎችን ያወዳድሩ፣ የዕለት ተዕለት ፍላጎቶችን ያግኙ",
    "Don't overpay or wander between kiosks. Discover stationery, electronics, toiletries, snacks, and print services across Main Campus and Bate with transparent freshness indicators.": "ተጨማሪ ዋጋ አይክፈሉ ወይም በኪዮስኮች መካከል አይድከሙ። የጽህፈት መሳሪያዎችን፣ ኤሌክትሮኒክስን፣ የንጽህና መጠበቂያዎችን፣ መክሰሶችን እና የህትመት አገልግሎቶችን በዋናው ግቢ እና በባቴ ውስጥ ግልጽ በሆነ የዋጋ ትኩስነት መረጃ ያግኙ።",
    "Search exercise books, flash drives, soap, biscuits, printing...": "ደብተር፣ ፍላሽ፣ ሳሙና፣ ብስኩት፣ ህትመት ይፈልጉ...",
    "Compare": "አወዳድር",
    "Popular:": "ተወዳጅ ፍለጋዎች:",
    "Exercise Books": "ደብተሮች",
    "USB Flash Drives": "የዩኤስቢ ፍላሽ ዲስኮች",
    "Lifebuoy / Soap": "ላይፍቦይ / ሳሙና",
    "Printing Services": "የህትመት አገልግሎት",
    "Catalog Products": "በካታሎግ ያሉ ምርቶች",
    "Campus & Bate Shops": "የካምፓስ እና የባቴ ሱቆች",
    "Price Verifications This Week": "በዚህ ሳምንት የተረጋገጡ ዋጋዎች",
    "Consumer Protection for Students": "የተማሪዎች የሸማች ጥበቃ",
    "Never Rely on Outdated Prices Again": "ዳግመኛ ጊዜ ባለፈባቸው ዋጋዎች አይታለሉ",
    "Campus Gabaa eliminates guesswork. Every listing features an automated freshness timestamp so students know whether a price is current before walking across campus or taking a bajaj to town.": "ካምፓስ ገበያ ግምትን ያስቀራል። እያንዳንዱ ዋጋ ወቅታዊነቱ የተረጋገጠበት ቀን ስላለው ተማሪዎች በግቢው ውስጥ ከመዘዋወራቸው ወይም ወደ ከተማ ባጃጅ ከመያዛቸው በፊት ዋጋው ትክክለኛ መሆኑን ያውቃሉ።",
    "FRESH": "ወቅታዊ",
    "EXPIRING": "ሊያበቃ የቀረበ",
    "STALE": "ያረጀ / ያልተረጋገጠ",
    "Verified by shop owner within the last 3 days.": "በባለቤቱ ባለፉት 3 ቀናት ውስጥ የተረጋገጠ።",
    "Confirmed 3 to 7 days ago. Price may shift.": "ከ 3 እስከ 7 ቀናት በፊት የተረጋገጠ። ዋጋው ሊቀየር ይችላል።",
    "Unconfirmed for over 7 days. Report if incorrect!": "ከ 7 ቀናት በላይ ያልተረጋገጠ። ስህተት ከሆነ ሪፖርት ያድርጉ!",
    "Crowd-Sourced Accuracy Verification": "በማህበረሰብ የሚረጋገጥ ትክክለኛነት",
    "If a kiosk owner charges more than listed or an item is out of stock, any student can submit an instant report. Our moderation queue contacts the merchant or updates the record.": "የኪዮስክ ባለቤት ከተዘረዘረው በላይ ዋጋ ከጠየቀ ወይም እቃው ካለቀ ማንኛውም ተማሪ ፈጣን ሪፖርት ማቅረብ ይችላል። የቁጥጥር ክፍሉ ነጋዴውን በማነጋገር መረጃውን ያስተካክላል።",
    "Built specifically for Haramaya University's decentralized kiosk layout across Main Campus, Agriculture Campus, and Bate Market.": "በተለይ ለሐረማያ ዩኒቨርሲቲ ዋናው ግቢ፣ ግብርና ግቢ እና ባቴ ገበያ ኪዮስኮች የተዘጋጀ።",
    "Browse by Campus Need": "በካምፓስ ፍላጎት ምድብ ይፈልጉ",
    "Filter products tailored to daily student life and study requirements": "ለተማሪዎች የዕለት ተዕለት ኑሮና ትምህርት የሚያስፈልጉ ምርቶችን ይምረጡ",
    "View All Products": "ሁሉንም ምርቶች ይመልከቱ",
    "items": "ዕቃዎች",
    "Top Comparisons": "ተደጋጋሚ የንጽጽር ምርቶች",
    "Compare Across Multiple Shops": "በተለያዩ ሱቆች መካከል ያወዳድሩ",
    "Products with verified listings in 2 or more campus shops": "በ2 እና ከዚያ በላይ የካምፓስ ሱቆች የተረጋገጠ ዋጋ ያላቸው ምርቶች",
    "Full Catalog": "ሙሉ ካታሎግ",
    "From": "ከ",
    "shops": "ሱቆች",
    "Are You a Campus Merchant or Kiosk Owner?": "የካምፓስ ነጋዴ ወይም የኪዮስክ ባለቤት ነዎት?",
    "List your store on Campus Gabaa for free. Connect with thousands of Haramaya University students, increase your sales, and keep your prices transparent and verified.": "ሱቅዎን በካምፓስ ገበያ በነጻ ይመዝግቡ። በሺዎች ከሚቆጠሩ የሐረማያ ዩኒቨርሲቲ ተማሪዎች ጋር ይገናኙ፣ ሽያጭዎን ያሳድጉ፣ ዋጋዎን ግልጽ እና አስተማማኝ ያድርጉ።",
    "Manage My Shop": "ሱቄን አስተዳድር",
    "Register Your Shop": "ሱቅዎን ይመዝግቡ",

    # Forms & Inputs
    "Search Term": "የመፈለጊያ ቃል",
    "Category": "ምድብ",
    "All Categories": "ሁሉም ምድቦች",
    "Campus Zone": "የካምፓስ ዞን",
    "All Campus Zones": "ሁሉም የካምፓስ ዞኖች",
    "Sort By": "ቅደም ተከተል",
    "Price: Lowest First": "ዋጋ፡ ከዝቅተኛ ወደ ከፍተኛ",
    "Price: Highest First": "ዋጋ፡ ከከፍተኛ ወደ ዝቅተኛ",
    "Name: A to Z": "ስም፡ ከአ ወደ ፐ",
    "Recently Updated": "በቅርቡ የተሻሻሉ",
    "In Stock Only": "በክምችት ውስጥ ያለ ብቻ",
    "In Stock": "በክምችት ውስጥ አለ",
    "Out of Stock": "አልቋል / ክምችት የለም",
    "Fresh Prices Only (< 7 days)": "ትኩስ ዋጋዎች ብቻ (< 7 ቀናት)",
    "Reset": "ዳግም ጀምር",
    "Apply Filters": "ማጣሪያዎችን ተግብር",
    "Suggest New Product": "አዲስ ምርት ጠቁም",

    # Product Detail & Comparison Table
    "Price Comparison": "የዋጋ ንጽጽር",
    "Lowest Campus Price": "ዝቅተኛው የካምፓስ ዋጋ",
    "Price Range Across Shops": "የዋጋ ክልል በሱቆች መካከል",
    "Save up to": "እስከዚህ ድረስ ይቆጥቡ:",
    "Where to Buy Near Haramaya Campus": "ሐረማያ ዩኒቨርሲቲ አቅራቢያ ከየት እንደሚገዛ",
    "Ranked by lowest price. Check the freshness badge before visiting the shop.": "በዝቅተኛ ዋጋ የተደረደሩ። ወደ ሱቁ ከመሄድዎ በፊት የትኩስነት ምልክቱን ያረጋግጡ።",
    "Sell This at My Shop": "ይህንን በኔ ሱቅ መሸጥ እፈልጋለሁ",
    "Shop & Campus Zone": "ሱቅ እና የካምፓስ ዞን",
    "Exact Landmark": "ትክክለኛ መለያ ምልክት",
    "Price": "ዋጋ",
    "Price Freshness": "የዋጋ ትኩስነት",
    "Contact & Actions": "ግንኙነት እና እርምጃዎች",
    "Confirmed today": "ዛሬ የተረጋገጠ",
    "Report Issue": "ችግር ሪፖርት አድርግ",
    "Recent Price Verification History": "የቅርብ ጊዜ የዋጋ ማረጋገጫ ታሪክ",
    "Previous Price (ETB)": "የቀድሞ ዋጋ (ብር)",
    "Updated Price (ETB)": "የተሻሻለ ዋጋ (ብር)",
    "Modified By": "ያሻሻለው አካል",
    "Change Notes": "የለውጥ ማስታወሻ",

    # Account & Profile
    "Choose Your Campus Role": "የካምፓስ ሚናዎን ይምረጡ",
    "Student / Campus Buyer": "ተማሪ / የካምፓስ ገዢ",
    "Shop Owner / Vendor": "የሱቅ ባለቤት / ነጋዴ",
    "Moderator / Campus Admin": "አስተባባሪ / የካምፓስ አስተዳዳሪ",
    "First Name": "ስም",
    "Father / Last Name": "የአባት ስም",
    "Email Address": "የኢሜይል አድራሻ",
    "Phone Number": "የስልክ ቁጥር",
    "Campus ID / Dorm or Department": "የካምፓስ መታወቂያ / ዶርም ወይም ትምህርት ክፍል",
    "Preferred Language": "ተመራጭ ቋንቋ",
    "Password": "የይለፍ ቃል",
    "Confirm Password": "የይለፍ ቃል አረጋግጥ",
    "Complete Registration": "ምዝገባን አጠናቅቅ",
    "Already registered?": "ቀድመው ተመዝግበዋል?",
    "Welcome Back": "እንኳን ደህና መጡ",
    "Sign in to manage your campus kiosk or submit price reports": "ኪዮስክዎን ለማስተዳደር ወይም ሪፖርት ለማቅረብ ይግቡ",
    "Enter your username": "የተጠቃሚ ስምዎን ያስገቡ",
    "Enter password": "የይለፍ ቃልዎን ያስገቡ",
    "Don't have an account yet?": "አካውንት የለዎትም?",
    "Create Free Account": "ነጻ አካውንት ይክፈቱ",
    "Save Profile Changes": "ለውጦችን መዝግብ",

    # Moderation & Vendor Dashboard
    "Shop Inventory & Price Freshness Controls": "የሱቅ ክምችት እና የዋጋ ትኩስነት መቆጣጠሪያ",
    "Confirm Today": "ዛሬ አረጋግጥ",
    "Edit Price": "ዋጋ አስተካክል",
    "Add Product Listing": "አዲስ ምርት ዝርዝር አክል",
    "Edit Shop Profile": "የሱቅ መረጃን አድስ",
    "View Public Storefront": "የህዝብ መደብር ገጽን እይ",
    "Total Inventory Items": "ጠቅላላ የክምችት እቃዎች",
    "Currently In Stock": "አሁን በክምችት ላይ ያለ",
    "Requires Price Confirmation": "የዋጋ ማረጋገጫ የሚፈልግ",
    "Pending Price Reports": "በመጠባበቅ ላይ ያሉ የዋጋ ሪፖርቶች",
    "Shops Pending Verification": "ማረጋገጫ የሚጠብቁ ሱቆች",
    "Reports Resolved": "እልባት ያገኙ ሪፖርቶች",
    "User-Submitted Listing Reports": "በተጠቃሚ የቀረቡ የዋጋ ሪፖርቶች",
    "Pending": "በመጠባበቅ ላይ",
    "Resolved": "እልባት ያገኘ",
    "Dismissed": "ውድቅ የተደረገ",
    "All": "ሁሉም",
    "Inspect": "መርምር",
    "Approve": "አጽድቅ",
    "Reject": "ውድቅ አድርግ",
    "Report Listing Discrepancy": "የዋጋ ልዩነት ሪፖርት አድርግ",
    "Submit Report": "ሪፖርቱን ላክ",
    "Actual Price Observed in Shop (ETB)": "በሱቁ ውስጥ ያዩት ትክክለኛ ዋጋ (ብር)",
    "Details & Description": "ዝርዝር መግለጫ",
    "Optional Receipt or Storefront Photo": "የደረሰኝ ወይም የሱቅ ፎቶ (አማራጭ)",
    "Take Moderation Action": "የቁጥጥር እርምጃ ውሰድ",
    "Submit Moderation Decision": "ውሳኔውን አረጋግጥ",
    "Unit of Measure": "የመለኪያ አሃድ",
    "Piece / Item": "በፍሬ / በቁጥር",
    "Pack / Bundle": "በጥቅል / በፓኬት",
    "Box / Carton": "በካርቶን / በሳጥን",
    "Kilogram (kg)": "በኪሎግራም (ኪ.ግ)",
    "Liter (L)": "በሊትር (ሊ)",
    "Page (Printing)": "በገጽ (ህትመት)",
    "Set": "በስብስብ",
    "Haramaya Main Campus (Dorm / Admin Kiosks)": "ሐረማያ ዋና ግቢ (የዶርም ኪዮስክ)",
    "Bate Gate / Campus Entrance": "የባቴ በር / የካምፓስ መግቢያ",
    "Bate Town Center & Market": "የባቴ ከተማ መሃል እና ገበያ",
    "Haramaya Town Commercial Area": "የሐረማያ ከተማ የንግድ አካባቢ",
    "Agriculture & Veterinary Campus Zone": "የግብርና እና የእንስሳት ህክምና ግቢ ዞን",
}


def update_po_file(po_path: Path, translations: dict, lang_name: str):
    print(f"Updating {lang_name} catalog at {po_path}...")
    if not po_path.exists():
        print(f"Error: {po_path} does not exist.")
        return

    content = po_path.read_text(encoding='utf-8')
    # Fix invalid Plural-Forms placeholder generated by makemessages
    content = re.sub(
        r'"Plural-Forms:\s*nplurals=[^;]+;\s*plural=[^;]+;\\n"',
        r'"Plural-Forms: nplurals=2; plural=(n > 1);\\n"',
        content
    )
    pattern = re.compile(
        r'(msgid\s+("(?:[^"\\]|\\.)*"\s*)+)\n(msgstr\s+("(?:[^"\\]|\\.)*"\s*)+)',
        re.MULTILINE
    )

    updated_count = 0

    def replace_func(match):
        nonlocal updated_count
        msgid_block = match.group(1)
        msgstr_block = match.group(3)

        # Extract text from msgid
        id_lines = re.findall(r'"((?:[^"\\]|\\.)*)"', msgid_block)
        msgid_text = "".join(id_lines).replace('\\"', '"').replace('\\n', '\n')

        if msgid_text in translations:
            translated_text = translations[msgid_text]
            escaped_text = translated_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            updated_count += 1
            return f'{msgid_block}\nmsgstr "{escaped_text}"'

        return match.group(0)

    new_content = pattern.sub(replace_func, content)
    po_path.write_text(new_content, encoding='utf-8')
    print(f"Successfully populated {updated_count} {lang_name} translations in {po_path.name}")


def main():
    po_om = BASE_DIR / 'locale' / 'om' / 'LC_MESSAGES' / 'django.po'
    po_am = BASE_DIR / 'locale' / 'am' / 'LC_MESSAGES' / 'django.po'

    update_po_file(po_om, TRANSLATIONS_OM, "Afaan Oromoo")
    update_po_file(po_am, TRANSLATIONS_AM, "Amharic")


if __name__ == '__main__':
    main()

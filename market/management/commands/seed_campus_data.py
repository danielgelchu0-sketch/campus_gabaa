"""
Seed command to populate realistic Haramaya University campus data for development,
testing, evaluation, and demonstration purposes.
"""

from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from market.models import Category, CampusZone, Product, Shop, Listing, PriceHistory
from moderation.models import PriceReport


class Command(BaseCommand):
    help = 'Seeds realistic demonstration data for Haramaya University & Bate community'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning Campus Gabaa data seeding...'))

        # 1. Create Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@campusgabaa.hu.edu.et',
                'first_name': 'Dr. Dawit',
                'last_name': 'Tadesse',
                'role': User.ROLE_MODERATOR,
                'phone_number': '0911000001',
                'campus_id_or_dorm': 'Department of Computing, Faculty Office',
                'is_staff': True,
                'is_superuser': True,
                'preferred_language': 'en',
            }
        )
        admin_user.set_password('CampusAdmin2026!')
        admin_user.save()

        # Shop Owner 1
        aman_owner, _ = User.objects.get_or_create(
            username='aman_stationery',
            defaults={
                'email': 'aman@kiosk.hu.edu.et',
                'first_name': 'Aman',
                'last_name': 'Kedir',
                'role': User.ROLE_SHOP_OWNER,
                'phone_number': '0911223344',
                'campus_id_or_dorm': 'Main Campus Kiosk Area',
                'is_verified_vendor': True,
                'preferred_language': 'om',
            }
        )
        aman_owner.set_password('VendorPass2026!')
        aman_owner.save()

        # Shop Owner 2
        gemechu_owner, _ = User.objects.get_or_create(
            username='bate_tech',
            defaults={
                'email': 'gemechu@bate.com',
                'first_name': 'Gemechu',
                'last_name': 'Tadesse',
                'role': User.ROLE_SHOP_OWNER,
                'phone_number': '0922334455',
                'campus_id_or_dorm': 'Bate Market Main Road',
                'is_verified_vendor': True,
                'preferred_language': 'om',
            }
        )
        gemechu_owner.set_password('VendorPass2026!')
        gemechu_owner.save()

        # Shop Owner 3
        fatuma_owner, _ = User.objects.get_or_create(
            username='kiosk_fatuma',
            defaults={
                'email': 'fatuma@campusgabaa.com',
                'first_name': 'Fatuma',
                'last_name': 'Ibrahim',
                'role': User.ROLE_SHOP_OWNER,
                'phone_number': '0933445566',
                'campus_id_or_dorm': 'Bate Gate Row #4',
                'is_verified_vendor': True,
                'preferred_language': 'am',
            }
        )
        fatuma_owner.set_password('VendorPass2026!')
        fatuma_owner.save()

        # Student Buyer
        student_user, _ = User.objects.get_or_create(
            username='student_solomon',
            defaults={
                'email': 'solomon.bekele@student.hu.edu.et',
                'first_name': 'Solomon',
                'last_name': 'Bekele',
                'role': User.ROLE_STUDENT,
                'phone_number': '0944112233',
                'campus_id_or_dorm': 'Block 42, Room 14 (Computer Science 4th Year)',
                'preferred_language': 'am',
            }
        )
        student_user.set_password('StudentPass2026!')
        student_user.save()

        self.stdout.write(self.style.SUCCESS('Created 5 core demonstration user accounts.'))

        # 2. Categories
        categories_data = [
            {
                'name': 'Stationery & Academic Supplies',
                'name_om': "Waraqaa fi Meeshaalee Barnootaa",
                'name_am': "የጽሕፈት መሣሪያዎችና የትምህርት ቁሳቁሶች",
                'slug': 'stationery-academic-supplies',
                'icon': 'bi-journal-bookmark-fill',
                'order': 1,
            },
            {
                'name': 'Electronics & Mobile Tech',
                'name_om': "Elektirooniksii fi Bilbilaa",
                'name_am': "ኤሌክትሮኒክስ እና የሞባይል ዕቃዎች",
                'slug': 'electronics-mobile-tech',
                'icon': 'bi-laptop',
                'order': 2,
            },
            {
                'name': 'Personal Care & Toiletries',
                'name_om': "Qulqullina Dhuunfaa fi Fayyaa",
                'name_am': "የግል ንጽሕና መጠበቂያዎች",
                'slug': 'personal-care-toiletries',
                'icon': 'bi-heart-pulse-fill',
                'order': 3,
            },
            {
                'name': 'Snacks, Coffee & Beverages',
                'name_om': "Nyaata Salphaa fi Buna",
                'name_am': "ቀላል ምግቦች፣ ቡናና መጠጦች",
                'slug': 'snacks-coffee-beverages',
                'icon': 'bi-cup-hot-fill',
                'order': 4,
            },
            {
                'name': 'Printing, Binding & Copy Services',
                'name_om': "Maxxansa fi Baay'isuu Qorannoo",
                'name_am': "የማተም፣ የፎቶኮፒና ጥራዝ አገልግሎት",
                'slug': 'printing-binding-copy-services',
                'icon': 'bi-printer-fill',
                'order': 5,
            },
        ]

        cats = {}
        for cdata in categories_data:
            cat, _ = Category.objects.update_or_create(
                slug=cdata['slug'],
                defaults=cdata
            )
            cats[cat.slug] = cat

        self.stdout.write(self.style.SUCCESS(f'Configured {len(cats)} campus categories.'))

        # 2b. Campus Zones
        zones_data = [
            {
                'code': 'MAIN_CAMPUS_KIOSK',
                'name': 'Haramaya Main Campus (Dorm Blocks 1–60)',
                'name_om': 'Mooraa Guddaa HU (Kiyooskii Ciisaa 1–60)',
                'name_am': 'ሀረማያ ዋና ግቢ (ዶርም 1–60 ኪዮስኮች)',
                'description': 'Student residential dorm kiosks (Blocks 1–60), post office row, and campus perimeter shops.',
                'order': 1,
            },
            {
                'code': 'CAMPUS_CENTRAL',
                'name': 'Main Campus Central (Admin, Library & Cafeteria)',
                'name_om': 'Wiirtuu Mooraa (Bulchiinsa, Mana Kitaabaa fi Kaafteeriyaa)',
                'name_am': 'ዋና ግቢ ማዕከል (አስተዳደር፣ ቤተ-መጽሐፍት እና ካፌ)',
                'description': 'Central campus services, student union building, main library print centers, and central cafeteria area.',
                'order': 2,
            },
            {
                'code': 'BATE_GATE',
                'name': 'Bate Gate (Campus Entrance Shops & Services)',
                'name_om': 'Balbala Baatee (Dukaanota Seensa Mooraa)',
                'name_am': 'ባቴ በር (የግቢው መግቢያ ሱቆች እና አገልግሎቶች)',
                'description': 'Commercial kiosks, mobile accessory shops, and copy centers directly at Haramaya University Main Gate.',
                'order': 3,
            },
            {
                'code': 'AGRICULTURE_CAMPUS',
                'name': 'Agriculture & Veterinary Campus Zone',
                'name_om': 'Mooraa Qonnaa fi Fayyaa Beeyladaa',
                'name_am': 'ግብርና እና የእንስሳት ሕክምና ግቢ',
                'description': 'College of Agriculture and Veterinary Medicine campus area kiosks and student stationery shops.',
                'order': 4,
            },
        ]

        for zdata in zones_data:
            CampusZone.objects.update_or_create(
                code=zdata['code'],
                defaults=zdata
            )
        self.stdout.write(self.style.SUCCESS(f'Configured {len(zones_data)} verified campus zones.'))

        # 3. Shops
        shops_data = [
            {
                'name': 'Aman Stationery & Student Essentials',
                'slug': 'aman-stationery-hu',
                'owner': aman_owner,
                'campus_zone': 'MAIN_CAMPUS_KIOSK',
                'specific_location': 'Opposite Male Dorm Block 42, Kiosk #3',
                'phone_number': '0911223344',
                'opening_hours': '7:30 AM - 9:00 PM',
                'description': 'Serving HU students with pens, spiral notebooks, calculators, flash drives, and print paper.',
                'status': Shop.STATUS_APPROVED,
                'is_verified': True,
            },
            {
                'name': 'Bate High-Tech Mobile & Accessories',
                'slug': 'bate-high-tech-mobile',
                'owner': gemechu_owner,
                'campus_zone': 'BATE_GATE',
                'specific_location': 'Bate Gate Entrance, East Row Kiosk #2',
                'phone_number': '0922334455',
                'opening_hours': '8:00 AM - 8:00 PM',
                'description': 'Direct retailer of phone chargers, memory cards, flash drives, earphones, and laptop cables.',
                'status': Shop.STATUS_APPROVED,
                'is_verified': True,
            },
            {
                'name': 'Fatuma Campus Convenience & Mart',
                'slug': 'fatuma-campus-mart',
                'owner': fatuma_owner,
                'campus_zone': 'BATE_GATE',
                'specific_location': 'Directly outside HU Main Gate 1, Row 2',
                'phone_number': '0933445566',
                'opening_hours': '7:00 AM - 10:00 PM',
                'description': 'Fast snack kiosk, mineral water, toiletries, soaps, biscuits, and daily student necessities.',
                'status': Shop.STATUS_APPROVED,
                'is_verified': True,
            },
            {
                'name': 'Central Library Digital Print & Copy Service',
                'slug': 'central-library-print-service',
                'owner': aman_owner,
                'campus_zone': 'CAMPUS_CENTRAL',
                'specific_location': 'HU Central Library Ground Floor, North Wing',
                'phone_number': '0944556677',
                'opening_hours': '8:00 AM - 8:30 PM',
                'description': 'Official fast document printing, thesis spiral and hard cover binding, color scanning.',
                'status': Shop.STATUS_APPROVED,
                'is_verified': True,
            },
            {
                'name': 'Finfinne Bookshop & Stationery',
                'slug': 'finfinne-bookshop-bate',
                'owner': gemechu_owner,
                'campus_zone': 'BATE_GATE',
                'specific_location': 'Bate Gate Entrance, West Row Kiosk #5',
                'phone_number': '0955667788',
                'opening_hours': '8:30 AM - 7:30 PM',
                'description': 'Academic textbooks, engineering drawing supplies, scientific calculators, and notebooks.',
                'status': Shop.STATUS_APPROVED,
                'is_verified': True,
            },
        ]

        shops = {}
        for sdata in shops_data:
            shop, _ = Shop.objects.update_or_create(
                slug=sdata['slug'],
                defaults=sdata
            )
            shops[shop.slug] = shop

        self.stdout.write(self.style.SUCCESS(f'Created {len(shops)} campus and Bate shops.'))

        # 4. Products
        products_data = [
            {
                'name': '100-Sheet Ruled Exercise Book (A4)',
                'name_om': "Daftara Fuula 100 Sararame (A4)",
                'name_am': "የ100 ቅጠል ባለመስመር ደብተር (A4)",
                'slug': '100-sheet-ruled-exercise-book-a4',
                'category': cats['stationery-academic-supplies'],
                'brand_or_model': 'Deli / Picasso',
                'unit': 'piece',
                'description': 'High quality 70gsm white ruled paper, ideal for university lecture note-taking.',
            },
            {
                'name': '50-Sheet Exercise Book',
                'name_om': "Daftara Fuula 50",
                'name_am': "የ50 ቅጠል ደብተር",
                'slug': '50-sheet-exercise-book',
                'category': cats['stationery-academic-supplies'],
                'brand_or_model': 'Standard Campus',
                'unit': 'piece',
                'description': 'Compact standard exercise book for lab work, quizzes, and short assignments.',
            },
            {
                'name': 'Blue 0.5mm Gel Pen',
                'name_om': "Qalama Jelii Cuquliisaa 0.5mm",
                'name_am': "ሰማያዊ ጄል እስክሪብቶ 0.5ሚሜ",
                'slug': 'blue-05mm-gel-pen',
                'category': cats['stationery-academic-supplies'],
                'brand_or_model': 'Bic / Deli',
                'unit': 'piece',
                'description': 'Smooth flowing blue gel pen with comfortable grip for fast exam and lecture writing.',
            },
            {
                'name': 'SanDisk Cruzer Blade 32GB USB Flash Drive',
                'name_om': "Filaashii SanDisk 32GB",
                'name_am': "ሳንዲስክ 32 ጊጋባይት ፍላሽ ዲስክ",
                'slug': 'sandisk-cruzer-blade-32gb-usb',
                'category': cats['electronics-mobile-tech'],
                'brand_or_model': 'SanDisk 32GB',
                'unit': 'piece',
                'description': 'Compact USB 2.0 flash memory drive for transferring assignments, lecture videos, and software.',
            },
            {
                'name': 'Fast Charging USB Type-C Cable (1M)',
                'name_om': "Keobilii Chaarjii Tayip-Sii (1M)",
                'name_am': "ፈጣን ቻርጅ የሚያደርግ ታይፕ-ሲ ገመድ (1 ሜትር)",
                'slug': 'fast-charging-usb-type-c-cable',
                'category': cats['electronics-mobile-tech'],
                'brand_or_model': 'Oraimo / Remax',
                'unit': 'piece',
                'description': 'Durable braided nylon Type-C data and fast-charging cable with reinforced stress points.',
            },
            {
                'name': 'Lifebuoy Antibacterial Soap (150g)',
                'name_om': "Saamunaa Qulqullinaa Lifebuoy (150g)",
                'name_am': "ላይፍቦይ የገላ ሳሙና (150 ግራም)",
                'slug': 'lifebuoy-antibacterial-soap-150g',
                'category': cats['personal-care-toiletries'],
                'brand_or_model': 'Lifebuoy Red',
                'unit': 'piece',
                'description': 'Antibacterial bar soap for daily student hygiene in campus dormitories.',
            },
            {
                'name': 'Colgate Herbal Toothpaste (100ml)',
                'name_om': "Qulqulleessaa Ilkaan Colgate (100ml)",
                'name_am': "ኮልጌት የጥርስ ሳሙና (100 ሚሊ)",
                'slug': 'colgate-herbal-toothpaste-100ml',
                'category': cats['personal-care-toiletries'],
                'brand_or_model': 'Colgate',
                'unit': 'piece',
                'description': 'Herbal extract fluoride toothpaste with cavity protection.',
            },
            {
                'name': 'Original Harar Roasted Coffee Beans (250g)',
                'name_om': "Buna Harargee Wakkilame (250g)",
                'name_am': "የሐረር ቆሎ ቡና (250 ግራም)",
                'slug': 'original-harar-roasted-coffee-beans-250g',
                'category': cats['snacks-coffee-beverages'],
                'brand_or_model': 'Harar Specialty',
                'unit': 'pack',
                'description': 'Aromatic Arabica medium-roasted Harar coffee beans for dorm study sessions.',
            },
            {
                'name': 'A4 Thesis / Senior Project Hardcover Binding',
                'name_om': "Qo'annoo Qabsiisuu Qola Jabaa (A4)",
                'name_am': "የምረቃ ጥናት ጠንካራ ጥራዝ ማሰሪያ (A4)",
                'slug': 'a4-thesis-hardcover-binding',
                'category': cats['printing-binding-copy-services'],
                'brand_or_model': 'Gold Foil Embossed',
                'unit': 'piece',
                'description': 'Official university blue/green hardcover binding with gold lettering for thesis defense.',
            },
            {
                'name': 'Black & White Document Printing (Per Page)',
                'name_om': "Maxxansa Waraqaa Gurraacha fi Adii (Fuula 1)",
                'name_am': "ነጭና ጥቁር ማተም (በአንድ ገጽ)",
                'slug': 'bw-document-printing-per-page',
                'category': cats['printing-binding-copy-services'],
                'brand_or_model': 'LaserJet 80gsm',
                'unit': 'page',
                'description': 'Crisp laser printing for handouts, lab reports, and lecture slides.',
            },
        ]

        products = {}
        for pdata in products_data:
            prod, _ = Product.objects.update_or_create(
                slug=pdata['slug'],
                defaults=pdata
            )
            products[prod.slug] = prod

        self.stdout.write(self.style.SUCCESS(f'Populated {len(products)} campus products.'))

        # 5. Listings with real price comparisons & freshness variance
        now = timezone.now()

        listings_plan = [
            # Product 1: 100-Sheet Ruled Book (Classic variance between campus kiosk & Bate market)
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['100-sheet-ruled-exercise-book-a4'],
                'price': Decimal('115.00'),
                'is_in_stock': True,
                'stock_notes': 'Blue and Red covers in stock',
                'confirmed_at': now - timedelta(hours=6),  # FRESH
            },
            {
                'shop': shops['finfinne-bookshop-bate'],
                'product': products['100-sheet-ruled-exercise-book-a4'],
                'price': Decimal('95.00'),
                'is_in_stock': True,
                'stock_notes': 'Special student batch discount',
                'confirmed_at': now - timedelta(days=1),  # FRESH
            },
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['100-sheet-ruled-exercise-book-a4'],
                'price': Decimal('125.00'),
                'is_in_stock': True,
                'stock_notes': 'Only 12 pieces remaining',
                'confirmed_at': now - timedelta(days=9),  # STALE (> 7 days)
            },

            # Product 2: 50-Sheet Book
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['50-sheet-exercise-book'],
                'price': Decimal('60.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(days=2),  # FRESH
            },
            {
                'shop': shops['finfinne-bookshop-bate'],
                'product': products['50-sheet-exercise-book'],
                'price': Decimal('50.00'),
                'is_in_stock': True,
                'stock_notes': 'Bulk boxes available',
                'confirmed_at': now - timedelta(days=4),  # EXPIRING
            },

            # Product 3: Blue Gel Pen
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['blue-05mm-gel-pen'],
                'price': Decimal('30.00'),
                'is_in_stock': True,
                'stock_notes': 'Smooth 0.5mm tip',
                'confirmed_at': now - timedelta(hours=12),  # FRESH
            },
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['blue-05mm-gel-pen'],
                'price': Decimal('35.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(days=10),  # STALE
            },
            {
                'shop': shops['finfinne-bookshop-bate'],
                'product': products['blue-05mm-gel-pen'],
                'price': Decimal('25.00'),
                'is_in_stock': False,
                'stock_notes': 'Sold out yesterday, new stock arriving Monday',
                'confirmed_at': now - timedelta(days=2),  # FRESH, but OUT OF STOCK
            },

            # Product 4: SanDisk 32GB Flash
            {
                'shop': shops['bate-high-tech-mobile'],
                'product': products['sandisk-cruzer-blade-32gb-usb'],
                'price': Decimal('420.00'),
                'is_in_stock': True,
                'stock_notes': 'Original with 1-year replacement warranty',
                'confirmed_at': now - timedelta(hours=8),  # FRESH
            },
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['sandisk-cruzer-blade-32gb-usb'],
                'price': Decimal('490.00'),
                'is_in_stock': True,
                'stock_notes': 'Limited stock in Block 42',
                'confirmed_at': now - timedelta(days=5),  # EXPIRING
            },

            # Product 5: Type-C Cable
            {
                'shop': shops['bate-high-tech-mobile'],
                'product': products['fast-charging-usb-type-c-cable'],
                'price': Decimal('180.00'),
                'is_in_stock': True,
                'stock_notes': '3A fast charging certified',
                'confirmed_at': now - timedelta(days=1),  # FRESH
            },
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['fast-charging-usb-type-c-cable'],
                'price': Decimal('230.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(days=8),  # STALE
            },

            # Product 6: Lifebuoy Soap
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['lifebuoy-antibacterial-soap-150g'],
                'price': Decimal('75.00'),
                'is_in_stock': True,
                'stock_notes': 'Red Total bar',
                'confirmed_at': now - timedelta(days=1),  # FRESH
            },
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['lifebuoy-antibacterial-soap-150g'],
                'price': Decimal('85.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(days=4),  # EXPIRING
            },

            # Product 7: Colgate Toothpaste
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['colgate-herbal-toothpaste-100ml'],
                'price': Decimal('140.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(hours=20),  # FRESH
            },
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['colgate-herbal-toothpaste-100ml'],
                'price': Decimal('155.00'),
                'is_in_stock': True,
                'stock_notes': '',
                'confirmed_at': now - timedelta(days=9),  # STALE
            },

            # Product 8: Harar Coffee
            {
                'shop': shops['fatuma-campus-mart'],
                'product': products['original-harar-roasted-coffee-beans-250g'],
                'price': Decimal('320.00'),
                'is_in_stock': True,
                'stock_notes': 'Fresh roast from Aweday/Harar',
                'confirmed_at': now - timedelta(days=2),  # FRESH
            },

            # Product 9: Hardcover Thesis Binding
            {
                'shop': shops['central-library-print-service'],
                'product': products['a4-thesis-hardcover-binding'],
                'price': Decimal('380.00'),
                'is_in_stock': True,
                'stock_notes': 'Standard HU dark green cover, 24-hr turnaround',
                'confirmed_at': now - timedelta(hours=4),  # FRESH
            },
            {
                'shop': shops['finfinne-bookshop-bate'],
                'product': products['a4-thesis-hardcover-binding'],
                'price': Decimal('320.00'),
                'is_in_stock': True,
                'stock_notes': 'Located in Bate, 48-hr turnaround',
                'confirmed_at': now - timedelta(days=3),  # EXPIRING
            },

            # Product 10: B&W Printing Per Page
            {
                'shop': shops['central-library-print-service'],
                'product': products['bw-document-printing-per-page'],
                'price': Decimal('4.00'),
                'is_in_stock': True,
                'stock_notes': 'Single page laser print',
                'confirmed_at': now - timedelta(hours=3),  # FRESH
            },
            {
                'shop': shops['aman-stationery-hu'],
                'product': products['bw-document-printing-per-page'],
                'price': Decimal('5.00'),
                'is_in_stock': True,
                'stock_notes': 'Block 42 print kiosk',
                'confirmed_at': now - timedelta(days=1),  # FRESH
            },
            {
                'shop': shops['finfinne-bookshop-bate'],
                'product': products['bw-document-printing-per-page'],
                'price': Decimal('3.50'),
                'is_in_stock': True,
                'stock_notes': 'Discount for > 50 pages',
                'confirmed_at': now - timedelta(days=6),  # EXPIRING
            },
        ]

        created_listings = []
        for lplan in listings_plan:
            listing, created = Listing.objects.update_or_create(
                shop=lplan['shop'],
                product=lplan['product'],
                defaults={
                    'price': lplan['price'],
                    'is_in_stock': lplan['is_in_stock'],
                    'stock_notes': lplan['stock_notes'],
                    'last_price_confirmed_at': lplan['confirmed_at'],
                }
            )
            created_listings.append(listing)

            # Create price history
            PriceHistory.objects.get_or_create(
                listing=listing,
                new_price=lplan['price'],
                defaults={
                    'old_price': lplan['price'] - Decimal('10.00') if lplan['price'] > 20 else None,
                    'changed_by': lplan['shop'].owner,
                    'notes': 'Verified vendor price log',
                    'created_at': lplan['confirmed_at'],
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(created_listings)} listings across campus kiosks.'))

        # 6. Sample Community Price Report
        stale_sample_listing = Listing.objects.filter(shop__slug='fatuma-campus-mart', product__slug='100-sheet-ruled-exercise-book-a4').first()
        if stale_sample_listing:
            PriceReport.objects.get_or_create(
                listing=stale_sample_listing,
                reported_by=student_user,
                defaults={
                    'report_type': PriceReport.TYPE_WRONG_PRICE,
                    'observed_price': Decimal('135.00'),
                    'comment': 'I visited the kiosk outside Gate 1 today and the shopkeeper requested 135 ETB instead of the listed 125 ETB. Please verify with vendor.',
                    'status': PriceReport.STATUS_PENDING,
                }
            )
            self.stdout.write(self.style.SUCCESS('Created sample student price discrepancy report for moderation testing.'))

        self.stdout.write(self.style.SUCCESS('\n========================================='))
        self.stdout.write(self.style.SUCCESS('Campus Gabaa seed data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('Demo Credentials:'))
        self.stdout.write(self.style.SUCCESS('  Admin:   admin / CampusAdmin2026!'))
        self.stdout.write(self.style.SUCCESS('  Vendor:  aman_stationery / VendorPass2026!'))
        self.stdout.write(self.style.SUCCESS('  Student: student_solomon / StudentPass2026!'))
        self.stdout.write(self.style.SUCCESS('=========================================\n'))

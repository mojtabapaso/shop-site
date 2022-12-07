from django.db import models
from django_jalali.db import models as jmodels
from pages.models import Category
from ckeditor.fields import RichTextField


class Brand(models.Model):
    category = models.ManyToManyField(Category, related_name='brand')
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "نام تجاری"


class Laptop(models.Model):
    category = models.ManyToManyField(Category, related_name='laptop_category', verbose_name='طبقه بندی ')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_laptop', verbose_name='نام تجاری ')
    name = models.IntegerField(verbose_name='نام ')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ ')
    image = models.ImageField(verbose_name='عکس ')
    description = RichTextField(verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    available = models.BooleanField(verbose_name='وجود ')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ اولین ساخت ')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ آپدیت')

    # Appearance characteristics
    weight = models.CharField(max_length=200, verbose_name='وزن')
    dimensions = models.CharField(max_length=200, verbose_name='ابعاد')

    # CPU features
    cpu = models.CharField(max_length=200, verbose_name="پردازنده")

    Manufacturer_for_CPU = [('INTEL', 'INTEL'), ('ADM', 'ADM'), ('APPLE', 'APPLE')]

    Manufacturer = models.CharField(max_length=200, choices=Manufacturer_for_CPU, verbose_name='سازنده')

    CPU_series_choices = [('Athlon', 'Athlon'), ('3000', '3000'), ('E1', 'E1'), ('E2', 'E2'), ('A4', 'A4'),
                          ('A6', 'A6'), ('A9', 'A9'), ('A12', 'A12'), ('FX', 'FX'), ('Ry-zen 3', 'Ry-zen 3'),
                          ('Ry_zen_5', 'Ry-zen 5'), ('Ry_zen_7', 'Ry-zen 7'), ('Ry_zen_9', 'Ry-zen 9'),
                          ('Celeron', 'Celeron'), ('Pentium', 'Pentium'), ('Pentium_Gold', 'Pentium_Gold'),
                          ('Core_i3', 'Core i3'),
                          ('Core i5', 'Core i5'), ('Core i7', 'Core i7'), ('Core i9', 'Core i9'), ('Xeon', 'Xeon')]

    processor_series = models.CharField(max_length=20, choices=CPU_series_choices, verbose_name='سری پردازنده')
    model = models.CharField(max_length=200, verbose_name='مدل پردازنده')
    number_core = models.CharField(max_length=200, verbose_name='تعداد هسته')
    number_threads = models.CharField(max_length=200, verbose_name='تعداد رشته')
    cache_memory = models.CharField(max_length=200, verbose_name='مقدار حافظه کش')
    base_frequency = models.CharField(max_length=200, verbose_name='فرکانس پایه')
    increasing_frequency = models.CharField(max_length=200, verbose_name='فرکانس افزایشی')

    # Ram features
    ram_memory = models.CharField(max_length=200, verbose_name='مقدار رم')
    ram_type = models.CharField(max_length=200, verbose_name='نوع رم')
    frequency_ram = [('1600MHz', '1600MHz'), ('1866MHz', '1866MHz'), ('2133MHz', '2133MHz'), ('2400MHz', '2400MHz'),
                     ('2666MHz', '2666MHz'), ('2933MHz', '2933MHz'), ('3200MHz', '3200MHz'), ('3733MHz', '3733MHz'),
                     ('4266MHz', '4266MHz'), ('4267MHz', '4267MHz'), ('4800MHz', '4800MHz'), ('5200MHz', '5200MHz'),
                     ('6400MHz', '6400MHz')]
    boss_ram = models.CharField(max_length=10, choices=frequency_ram, verbose_name='باس رم')
    ability_upgrade_ram = models.BooleanField(default=False, verbose_name='قابلیت  افزایش رم')

    # Memory features
    HDD_choices = [('500GB', '500GB'), ('1T', '1T'), ('2T', '2T'), ('ندارد', None)]
    capacity_of_HDD = models.CharField(max_length=20, choices=HDD_choices, verbose_name='مقدار H.D.D')
    SDD_choices = [('64GB', '64GB'), ('120GB', '120GB'), ('128GB', '128GB'), ('240GB', '240GB'), ('250GB', '250GB'),
                   ('256GB', '256GB'), ('500GB', '500GB'), ('512GB', '512GB'), ('512GB+512GB', '512GB+512GB'),
                   ('1T', '1T'),
                   ('1T+1T', '1T+1T'), ('2T', '2T'), ('ندارد', None), ]
    capacity_of_SSD = models.CharField(max_length=20, choices=SDD_choices, verbose_name='مقدار S.S.D')
    connection_type = models.CharField(max_length=120, verbose_name='نوع ارتباط')
    ability_upgrade_memory = models.BooleanField(default=False, verbose_name='قابلیت افزایش حافظه')

    # Graphics card features
    graphics_volume = models.CharField(max_length=200, verbose_name='حجم گرافیک')
    manufacturer_graphics = models.CharField(max_length=200, verbose_name='سری گرافیک')
    graphics_type = models.CharField(max_length=200)
    model_graphic = models.CharField(max_length=200)
    ram_graphic = models.CharField(max_length=150)
    graphics_power = models.CharField(max_length=150)
    increased_graphics_power = models.CharField(max_length=120)
    memory_interface = models.CharField(max_length=150)

    # Screen features
    choices_rate = [('60Hz', '60Hz'), ('90Hz', '90Hz'), ('120Hz', '120Hz'), ('144Hz', '144Hz'), ('165Hz', '165Hz'),
                    ('240Hz', '240Hz'), ('244Hz', '244Hz'),
                    ('300Hz', '300Hz'), ('360Hz', '360Hz')]
    image_rate = models.CharField(max_length=200, choices=choices_rate, verbose_name='نرخ تصویر')
    screen_size = models.CharField(max_length=200, verbose_name='سایز صفحه نمایش (اینچ)')
    image_panel = models.CharField(max_length=200, verbose_name='پنل تصویر')
    resolution_choices = [('WQ2', 'WQ2'), ('2.8K', '2.8k'), ('QHD', 'QHD'), ('HD', 'HD'), ('FULL_HD', 'Full HD'),
                          ('FHD+', 'FHD+'), ('2K', '2K'), ('4K', '4K')]
    resolution = models.CharField(max_length=200, choices=resolution_choices, verbose_name='وضوح تصویر')
    matte_screen = models.BooleanField(verbose_name='صفحه نمایش مات')
    Touch_screen = models.BooleanField(verbose_name='صفحه نمایش لمسی')

    # Main camera
    resolution_main_camera = models.CharField(max_length=150, verbose_name='رزولوشن دوربین اصلی')

    # Front camera
    selfie_camera_resolution = models.CharField(max_length=150, verbose_name='رزولوشن دوربین سلفی')
    # connections
    bluetooth = models.CharField(max_length=200, verbose_name='بلوتوث')
    Wi_Fi = models.BooleanField(default=False, verbose_name='وای فای ')

    # Ports
    type_C = models.CharField(max_length=200, verbose_name='تایپ C')
    USB_3 = models.CharField(max_length=200, verbose_name=' USB 3.0')
    USB_2 = models.CharField(max_length=200, verbose_name=' USB 2.0')
    display_port = models.BooleanField(default=False)
    HDMI = models.BooleanField(default=False)
    VGA = models.BooleanField(default=False)
    jack_35_mm = models.BooleanField(default=False, verbose_name='جک 3.5 میلیمتری ')
    Lan_choices = [('mini RJ-45', 'mini_RJ_45'), ('دارد', True), ('ندارد', False)]
    LAN = models.BooleanField(default=False, choices=Lan_choices, verbose_name='پورت Lan')
    memory_port = models.BooleanField(default=False, verbose_name=' درگاه حافظه')

    # battery
    capacity = models.CharField(max_length=20, verbose_name='ظرفیت باتری')
    type = models.CharField(max_length=20, verbose_name='نوع باتری ')
    charging_rate = models.CharField(max_length=20, verbose_name='میزان شارژدهی باتری')
    detachable_battery = models.BooleanField(default=False, verbose_name=' قابلیت جدا شدن باتری ')

    # Possibilities امکانات
    optical_drive = models.BooleanField(default=False, verbose_name='درایو نوری')
    keyboard_light_choices = [('ندارد', False), ('دارد', True)]
    keyboard_light = models.BooleanField(default=False, verbose_name='نور صفحه کلید ')
    fingerprint_scanner_choices = [('ندارد', False), ('دارد', True)]
    fingerprint_scanner = models.BooleanField(default=False, choices=fingerprint_scanner_choices,
                                              verbose_name='حسگر انگشت')
    operating_system = models.CharField(max_length=200, verbose_name='سیستم عامل')
    webcam = models.BooleanField(default=False, verbose_name='وب کم')
    Multi_touch_touchpad = models.BooleanField(default=False, verbose_name='قابلت لمس ')

    # Included
    included_items = models.CharField(max_length=200, verbose_name='لوازم جانبی')

    # Status Product
    status_choices = [('CTO', 'CTO'), ('ORIGINAL', 'ORIGINAL')]
    hardware = models.CharField(max_length=200, choices=status_choices, verbose_name='وضعیت محصول')

    class Meta:
        verbose_name_plural = "لپ تاب"

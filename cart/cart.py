from shop.models import Product, Profile

# برای مدیریت سبد خرید کاربران طراحی شده است. این کلاس شامل متدهایی برای اضافه کردن محصولات به سبد خرید، به‌روزرسانی تعداد محصولات، حذف محصولات، محاسبه مجموع قیمت و بازیابی اطلاعات محصولات می‌باشد Cart کلاس
class Cart:
    # این متد سازنده، سبد خرید را از سشن کاربر بازیابی می‌کند. اگر سبدی موجود نباشد، یک سبد جدید در سشن ایجاد می‌شود
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart 

    # متدی برای اضافه کردن محصولات و تعداد مشخصی از آن‌ها به دیتابیس و همچنین ذخیره‌سازی آن در سبد خرید سشن
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # اگر کاربر وارد حساب شده باشد، سبد خرید او در دیتابیس ذخیره می‌شود.
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

    # متدی برای اضافه کردن محصولات جدید به سبد خرید و همچنین ذخیره‌سازی آن‌ها در دیتابیس در صورت ورود کاربر
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id) 
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

    # متدی برای بازگرداندن تعداد آیتم‌های موجود در سبد خرید
    def __len__(self):
        return len(self.cart)

    # متدی برای دریافت اطلاعات محصولات موجود در سبد خرید از دیتابیس
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    # متدی برای بازگرداندن تعداد محصولات در سبد خرید
    def get_quants(self):
        return self.cart

    # متدی برای محاسبه مجموع قیمت محصولات در سبد خرید، با توجه به قیمت عادی یا قیمت فروش
    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0

        for key, value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total

    # متدی برای به‌روزرسانی تعداد یک محصول مشخص در سبد خرید و ذخیره تغییرات در دیتابیس در صورت ورود کاربر
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        self.cart[product_id] = product_qty
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            db_cart = str(self.cart).replace('\'', '\"')
            current_user.update(old_cart=str(db_cart))

        return self.cart

    # متدی برای حذف یک محصول از سبد خرید و همچنین به‌روزرسانی دیتابیس در صورت ورود کاربر
    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id) 
            db_cart = str(self.cart).replace('\'', '\"')  
            current_user.update(old_cart=str(db_cart))

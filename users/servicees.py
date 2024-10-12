import stripe
from config import settings


stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(product):
    """ Создает продукт в Stripe и возвращает его ID """
    stripe_product = stripe.Product.create(name=product.title)
    return stripe_product.id


def create_stripe_price(amount, product_id):
    """ Создает цену в Stripe, используя ID продукта """
    return stripe.Price.create(
        unit_amount=amount * 100,
        currency="rub",
        product=product_id,
    )


def create_stripe_sessions(price):
    """ Создает сессию на оплату в страйпе """
    sessions = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return sessions.get("id"), sessions.get("url")

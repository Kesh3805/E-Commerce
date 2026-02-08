from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.coupon import Coupon
from app.models.address import Address
import json


class OrderService:

    @staticmethod
    def place_order(user_id, address_id=None, coupon_code=None, payment_method="COD"):
        """Place an order from user's cart with stock validation, address, and coupon support."""
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return None, "Cart is empty"

        # Resolve shipping address
        shipping_address_json = None
        if address_id:
            address = Address.query.filter_by(id=address_id, user_id=user_id).first()
            if not address:
                return None, "Shipping address not found"
            shipping_address_json = json.dumps(address.to_dict())
        else:
            default_addr = Address.query.filter_by(user_id=user_id, is_default=True).first()
            if default_addr:
                shipping_address_json = json.dumps(default_addr.to_dict())

        subtotal = 0
        order_items = []

        # Validate all items and calculate subtotal
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if not product:
                return None, f"Product ID {item.product_id} not found"
            if not product.is_available:
                return None, f"'{product.name}' is out of stock"
            if product.stock < item.quantity:
                return None, f"Insufficient stock for '{product.name}'. Only {product.stock} available"

            if product.price <= 0:
                return None, f"Invalid price for '{product.name}'"

            line_total = product.price * item.quantity
            subtotal += line_total

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price,
                )
            )
            product.stock -= item.quantity

        # Apply coupon if provided
        discount_amount = 0
        if coupon_code:
            coupon = Coupon.query.filter_by(code=coupon_code.upper()).first()
            if coupon and coupon.is_valid:
                discount_amount = coupon.calculate_discount(subtotal)
                coupon.times_used += 1
            else:
                return None, "Invalid or expired coupon"

        total_price = round(max(0, subtotal - discount_amount), 2)

        order = Order(
            user_id=user_id,
            subtotal=round(subtotal, 2),
            total_price=total_price,
            discount_amount=round(discount_amount, 2),
            coupon_code=coupon_code.upper() if coupon_code else None,
            shipping_address=shipping_address_json,
            payment_method=payment_method,
            status="PLACED",
        )
        order.items = order_items
        db.session.add(order)

        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return order, None

    @staticmethod
    def get_user_orders(user_id):
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        return orders

    @staticmethod
    def get_order_by_id(order_id, user_id=None, is_admin=False):
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"
        if not is_admin and order.user_id != int(user_id):
            return None, "Access denied"
        return order, None

    @staticmethod
    def update_status(order_id, status):
        valid_statuses = ("PLACED", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED")
        if status not in valid_statuses:
            return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"

        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"

        order.status = status
        db.session.commit()
        return order, None

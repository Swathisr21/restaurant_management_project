from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from products.models import MenuItem
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# ---------------------------
# HOME + MENU
# ---------------------------
def home_page(request):
    return render(request, 'home.html')

def menu_page(request):
    items = MenuItem.objects.all()
    return render(request, 'menu.html', {"items": items})

# ---------------------------
# ORDER PAGE (create order)
# ---------------------------
@login_required
def order_page(request):
    items = MenuItem.objects.all()

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        table_number = request.POST.get("table_number")
        selected_items = request.POST.getlist("item_ids")

        if not selected_items:
            return redirect("/order/")

        total = 0
        order_items_data = []

        for item_id in selected_items:
            qty = int(request.POST.get(f"qty_{item_id}", 0))
            if qty <= 0:
                continue

            item = MenuItem.objects.get(id=item_id)
            total += item.item_price * qty
            order_items_data.append((item, qty))

        if not order_items_data:
            return redirect("/order/")

        # 🔥 Save owner = logged in user
        order = Order.objects.create(
            owner=request.user,
            customer_name=customer_name,
            table_number=table_number,
            total_amount=total
        )

        for item, qty in order_items_data:
            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=qty,
                price=item.item_price
            )

        return redirect("/my-orders/")

    return render(request, "order.html", {"items": items})

# ---------------------------
# MY ORDERS
# ---------------------------
@login_required
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    # 🔥 Show only orders that belong to the logged-in user
    orders = Order.objects.filter(owner=request.user).order_by('-created_at')

    return render(request, "my_orders.html", {"orders": orders})


# ---------------------------
# CANCEL (mark cancelled)
# ---------------------------
@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect("/my-orders/")

    order.status = "cancelled"
    order.save()
    return redirect("/my-orders/")


# ---------------------------
# COMPLETE (mark completed)
# ---------------------------
@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # we allow completing only if not cancelled
    if order.status != 'cancelled':
        order.status = 'completed'
        order.save()
    return redirect('my_orders')

# ---------------------------
# DELETE (permanent) — allow only if pending or owner
# ---------------------------
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_name=request.user.username)
    # allow delete only when pending (optional)
    if order.status == 'pending':
        order.delete()
    return redirect('my_orders')

# ---------------------------
# EDIT ORDER (only pending)
# ---------------------------
@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_name=request.user.username)
    if order.status != 'pending':
        return redirect('my_orders')

    items = MenuItem.objects.all()

    if request.method == "POST":
        # rebuild order from posted data
        selected_items = request.POST.getlist("item_ids")
        total = Decimal('0')
        order_items_data = []

        for item_id in selected_items:
            qty = int(request.POST.get(f"qty_{item_id}", 0))
            if qty <= 0:
                continue
            item = get_object_or_404(MenuItem, id=item_id)
            total += item.item_price * qty
            order_items_data.append((item, qty))

        if order_items_data:
            # delete previous items then recreate
            order.items.all().delete()
            for item, qty in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.item_price
                )
            order.total_amount = total
            order.save()
        return redirect('my_orders')

    # build a map of existing quantities for template pre-fill
    existing = {str(it.menu_item.id): it.quantity for it in order.items.all()}
    return render(request, "edit_order.html", {"order": order, "items": items, "existing": existing})

# ---------------------------
# INVOICE / PDF (basic)
# ---------------------------
@login_required
def invoice_page(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect("my_orders")

    return render(request, "invoice.html", {"order": order})


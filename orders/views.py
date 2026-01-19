from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import MenuItem
from .serializers import OrderSerializer


# ----------------------------------------------------
# API ViewSet
# ----------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


# ----------------------------------------------------
# CANCEL ORDER
# ----------------------------------------------------
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = "cancelled"
    order.save()
    return redirect('my_orders')


# ----------------------------------------------------
# COMPLETE ORDER
# ----------------------------------------------------
@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # only pending orders can be completed
    if order.status == "pending":
        order.status = "completed"
        order.save()

    return redirect('my_orders')


# ----------------------------------------------------
# INVOICE PAGE
# ----------------------------------------------------
@login_required
def invoice_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "invoice.html", {"order": order})

# ----------------------------------------------------
# EDIT ORDER
# ----------------------------------------------------


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    items = MenuItem.objects.all()

    if request.method == "POST":
        # Update name + table number
        order.customer_name = request.POST.get("customer_name")
        order.table_number = request.POST.get("table_number")

        # Remove old items
        order.items.all().delete()

        total = 0
        for item in items:
            qty = int(request.POST.get(f"qty_{item.id}", 0))
            if qty > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.item_price
                )
                total += item.item_price * qty

        order.total_amount = total
        order.save()

        return redirect("my_orders")

    return render(request, "edit_order.html", {
        "order": order,
        "items": items,
    })

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect("my_orders")

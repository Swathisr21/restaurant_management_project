from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from decimal import Decimal
from home.models import MenuItem
from orders.models import Order, OrderItem

# Create your views here.

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import MenuCategory, MenuItem, Table
from .serializers import MenuCategorySerializer, MenuItemSerializer, TableSerializer

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
    from orders.models import PaymentMethod
    payment_methods = PaymentMethod.objects.filter(is_active=True)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        selected_items = request.POST.getlist("item_ids")
        payment_method_id = request.POST.get("payment_method")

        if not selected_items:
            messages.error(request, "Please select at least one item.")
            return redirect("/order/")

        if not payment_method_id:
            messages.error(request, "Please select a payment method.")
            return redirect("/order/")

        order_items_data = []

        for item_id in selected_items:
            qty = int(request.POST.get(f"qty_{item_id}", 0))
            if qty <= 0:
                continue

            item = MenuItem.objects.get(id=item_id)
            order_items_data.append((item, qty))

        if not order_items_data:
            messages.error(request, "Please select valid quantities for items.")
            return redirect("/order/")

        #  Save user = logged in user with default status
        from orders.models import OrderStatus
        pending_status = OrderStatus.objects.get(name='pending')
        payment_method = PaymentMethod.objects.get(id=payment_method_id)

        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            status=pending_status
        )

        for item, qty in order_items_data:
            OrderItem.objects.create(
                order=order,
                menu_item=item,
                quantity=qty,
                price=item.price
            )

        messages.success(request, f"Order placed successfully! Payment method: {payment_method.name}")
        return redirect("/my-orders/")

    return render(request, "order.html", {
        "items": items,
        "payment_methods": payment_methods
    })

# ---------------------------
# MY ORDERS
# ---------------------------
@login_required
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')

    # 🔥 Show only orders that belong to the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "my_orders.html", {"orders": orders})


# ---------------------------
# CANCEL (mark cancelled)
# ---------------------------
@login_required
def cancel_order(request, order_id):
    from orders.models import OrderStatus
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect("/my-orders/")

    cancelled_status = OrderStatus.objects.get(name='cancelled')
    order.status = cancelled_status
    order.save()
    return redirect("/my-orders/")


# ---------------------------
# COMPLETE (mark completed)
# ---------------------------
@login_required
def complete_order(request, order_id):
    from orders.models import OrderStatus
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # we allow completing only if not cancelled
    if order.status and order.status.name != 'cancelled':
        completed_status = OrderStatus.objects.get(name='completed')
        order.status = completed_status
        order.save()
    return redirect('my_orders')

# ---------------------------
# DELETE (permanent) — allow only if pending or owner
# ---------------------------
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # allow delete only when pending
    if order.status and order.status.name == 'pending':
        order.delete()
    return redirect('my_orders')

# ---------------------------
# ORDER DETAILS (view order)
# ---------------------------
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})


# ---------------------------
# EDIT ORDER (only pending)
# ---------------------------
@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status and order.status.name != 'pending':
        return redirect('my_orders')

    items = MenuItem.objects.all()

    if request.method == "POST":
        # rebuild order from posted data
        selected_items = request.POST.getlist("item_ids")
        order_items_data = []

        for item_id in selected_items:
            qty = int(request.POST.get(f"qty_{item_id}", 0))
            if qty <= 0:
                continue
            item = get_object_or_404(MenuItem, id=item_id)
            order_items_data.append((item, qty))

        if order_items_data:
            # delete previous items then recreate
            order.orderitem_set.all().delete()
            for item, qty in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.price
                )
            order.save()
        return redirect('my_orders')

    # build a map of existing quantities for template pre-fill
    existing = {str(it.menu_item.id): it.quantity for it in order.orderitem_set.all()}
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


class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class FeaturedMenuItemView(ListAPIView):
    """
    API endpoint to list only the menu items
    """
    queryset = MenuItem.objects.filter(is_featured=True)
    serializer_class = MenuItemSerializer

class MenuItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MenuItemSearchViewSet(viewsets.ViewSet):
    pagination_class = MenuItemPagination

    def list(self, request):
        search_query = request.GET.get('q', '')

        #search by name
        queryset = MenuItem.objects.filter(name__icontains=search_query)

        #paginate results
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = MenuItemSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class MenuItemByCategoryView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category', None)

        if category_name:
            return MenuItem.objects.filter(category__name__iexact=category_name)

        return MenuItem.objects.all()

class TableDetailView(RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class AvailableTablesAPIView(ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(is_available=True)


# ---------------------------
# TABLE AVAILABILITY PAGE
# ---------------------------
def table_availability(request):
    tables = Table.objects.all().order_by('table_number')
    available_tables = Table.objects.filter(is_available=True).order_by('table_number')

    context = {
        'tables': tables,
        'available_tables': available_tables,
        'total_tables': tables.count(),
        'available_count': available_tables.count(),
        'occupied_count': tables.count() - available_tables.count()
    }

    return render(request, 'table_availability.html', context)


# ---------------------------
# RESERVE TABLE
# ---------------------------
@login_required
def reserve_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if not table.is_available:
        messages.error(request, f"Table {table.table_number} is already occupied.")
        return redirect('table_availability')

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        party_size = int(request.POST.get("party_size", 1))

        # Check if table capacity is sufficient
        if party_size > table.capacity:
            messages.error(request, f"Table {table.table_number} only accommodates {table.capacity} people.")
            return redirect('table_availability')

        # Mark table as occupied
        table.is_available = False
        table.save()

        messages.success(request, f"Table {table.table_number} reserved successfully for {customer_name}!")
        return redirect('table_availability')

    return render(request, 'reserve_table.html', {'table': table})


# ---------------------------
# RELEASE TABLE (for staff/admin)
# ---------------------------
@login_required
def release_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.user.is_staff or request.user.is_superuser:
        table.is_available = True
        table.save()
        messages.success(request, f"Table {table.table_number} is now available.")
    else:
        messages.error(request, "You don't have permission to release tables.")

    return redirect('table_availability')

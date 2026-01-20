from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Coupon, PaymentMethod, LoyaltyProgram, NutritionalInfo, Ingredient, Contact, CustomerReview, InventoryItem
from django.db import models
from home.models import MenuItem
from .serializers import OrderSerializer, CouponSerializer, PaymentMethodSerializer, LoyaltyProgramSerializer, NutritionalInfoSerializer, IngredientSerializer, ContactSerializer

# ----------------------------------------------------
# API ViewSet
# ----------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Filter orders by user if not staff
        if not self.request.user.is_staff:
            return Order.objects.filter(user=self.request.user).order_by('-created_at')
        return Order.objects.all().order_by('-created_at')

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get order history for the authenticated user with pagination and filtering.
        """
        queryset = self.get_queryset()

        # Filter by status if provided
        status_filter = request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status__name=status_filter)

        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# ----------------------------------------------------
# CANCEL ORDER
# ----------------------------------------------------
@login_required
def cancel_order(request, order_id):
    from .models import OrderStatus
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cancelled_status = OrderStatus.objects.get(name='cancelled')
    order.status = cancelled_status
    order.save()
    return redirect('my_orders')


# ----------------------------------------------------
# COMPLETE ORDER
# ----------------------------------------------------
@login_required
def complete_order(request, order_id):
    from .models import OrderStatus
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # only pending orders can be completed
    if order.status and order.status.name == "pending":
        completed_status = OrderStatus.objects.get(name='completed')
        order.status = completed_status
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
    order = get_object_or_404(Order, id=order_id, user=request.user)

    items = MenuItem.objects.all()

    if request.method == "POST":
        # Update name
        order.customer_name = request.POST.get("customer_name")

        # Remove old items
        order.orderitem_set.all().delete()

        for item in items:
            qty = int(request.POST.get(f"qty_{item.id}", 0))
            if qty > 0:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    quantity=qty,
                    price=item.price
                )

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


# ----------------------------------------------------
# COUPON VIEWS
# ----------------------------------------------------
class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        coupon = self.get_object()
        # Add validation logic here
        return Response({"valid": coupon.is_active, "discount": coupon.discount_percentage})


# ----------------------------------------------------
# PAYMENT METHOD VIEWS
# ----------------------------------------------------
class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer


# ----------------------------------------------------
# LOYALTY PROGRAM VIEWS
# ----------------------------------------------------
class LoyaltyProgramViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyProgram.objects.all()
    serializer_class = LoyaltyProgramSerializer


# ----------------------------------------------------
# NUTRITIONAL INFO VIEWS
# ----------------------------------------------------
class NutritionalInfoViewSet(viewsets.ModelViewSet):
    queryset = NutritionalInfo.objects.all()
    serializer_class = NutritionalInfoSerializer


# ----------------------------------------------------
# INGREDIENT VIEWS
# ----------------------------------------------------
class IngredientListView(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        menu_item_id = self.request.query_params.get('menu_item', None)
        if menu_item_id:
            return Ingredient.objects.filter(menu_item_id=menu_item_id)
        return Ingredient.objects.all()


# ----------------------------------------------------
# CONTACT VIEWS
# ----------------------------------------------------
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Regular users can only see their own contacts, staff can see all
        if not self.request.user.is_staff:
            return Contact.objects.filter(email=self.request.user.email).order_by('-created_at')
        return Contact.objects.all().order_by('-created_at')


# ----------------------------------------------------
# KITCHEN ORDER DISPLAY (for chefs/staff)
# ----------------------------------------------------
@login_required
def kitchen_orders(request):
    # Only staff can access kitchen orders
    if not request.user.is_staff and not hasattr(request.user, 'staff'):
        messages.error(request, "You don't have permission to access kitchen orders.")
        return redirect('home')

    # Get orders that need kitchen attention
    kitchen_orders = Order.objects.filter(
        status__name__in=['pending', 'processing']
    ).order_by('created_at')

    context = {
        'kitchen_orders': kitchen_orders,
        'pending_count': kitchen_orders.filter(status__name='pending').count(),
        'processing_count': kitchen_orders.filter(status__name='processing').count(),
    }

    return render(request, 'kitchen_orders.html', context)


# ----------------------------------------------------
# UPDATE ORDER STATUS (for kitchen staff)
# ----------------------------------------------------
@login_required
def update_order_status(request, order_id, new_status):
    # Only staff can update order status
    if not request.user.is_staff and not hasattr(request.user, 'staff'):
        messages.error(request, "You don't have permission to update orders.")
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    status_obj = get_object_or_404(OrderStatus, name=new_status)

    order.status = status_obj
    order.save()

    messages.success(request, f"Order {order.order_id} status updated to {new_status}.")
    return redirect('kitchen_orders')


# ----------------------------------------------------
# CUSTOMER REVIEWS MANAGEMENT
# ----------------------------------------------------
@login_required
def submit_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Check if order is completed and review doesn't exist
    if order.status.name != 'completed':
        messages.error(request, "You can only review completed orders.")
        return redirect('my_orders')

    if hasattr(order, 'customerreview'):
        messages.info(request, "You have already reviewed this order.")
        return redirect('my_orders')

    if request.method == "POST":
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text', '')

        CustomerReview.objects.create(
            order=order,
            customer=request.user,
            rating=rating,
            review_text=review_text
        )

        messages.success(request, "Thank you for your review!")
        return redirect('my_orders')

    return render(request, 'submit_review.html', {'order': order})


# ----------------------------------------------------
# VIEW ALL REVIEWS (public)
# ----------------------------------------------------
def customer_reviews(request):
    reviews = CustomerReview.objects.filter(is_approved=True).select_related('order', 'customer').order_by('-created_at')

    # Calculate average rating
    avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg__avg'] or 0

    context = {
        'reviews': reviews,
        'average_rating': round(avg_rating, 1),
        'total_reviews': reviews.count(),
    }

    return render(request, 'customer_reviews.html', context)


# ----------------------------------------------------
# INVENTORY MANAGEMENT
# ----------------------------------------------------
@login_required
def inventory_management(request):
    # Only staff can access inventory
    if not request.user.is_staff and not hasattr(request.user, 'staff'):
        messages.error(request, "You don't have permission to access inventory.")
        return redirect('home')

    inventory_items = InventoryItem.objects.all().order_by('category', 'name')
    low_stock_items = inventory_items.filter(quantity__lte=models.F('minimum_threshold'))

    context = {
        'inventory_items': inventory_items,
        'low_stock_items': low_stock_items,
        'total_items': inventory_items.count(),
        'low_stock_count': low_stock_items.count(),
    }

    return render(request, 'inventory_management.html', context)


# ----------------------------------------------------
# UPDATE INVENTORY ITEM
# ----------------------------------------------------
@login_required
def update_inventory(request, item_id):
    # Only staff can update inventory
    if not request.user.is_staff and not hasattr(request.user, 'staff'):
        messages.error(request, "You don't have permission to update inventory.")
        return redirect('home')

    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == "POST":
        new_quantity = request.POST.get('quantity')
        if new_quantity:
            item.quantity = float(new_quantity)
            item.save()
            messages.success(request, f"{item.name} quantity updated to {item.quantity} {item.unit}.")
        return redirect('inventory_management')

    return render(request, 'update_inventory.html', {'item': item})

import random
from datetime import timedelta, date
from decimal import Decimal
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse

import cart
from ShoppingApp.models import Product
from .models import Cart, CartItem, Order, Orderitem, Profile, ProductReview
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import razorpay
import xhtml2pdf.pisa as pisa

# import cv2
# import dlib
# import numpy as np

################## image preparation ####################
# loading the mpdel image
from numpy import empty
razorpay_client = razorpay.Client(auth=("rzp_test_V8XRJjy8oeI9IU", "EL7Brk6dgnCTR7Jzgd7UgmVB"))
razorpay_client.set_app_details({"key_id": "rzp_test_V8XRJjy8oeI9IU"})
# Create your views here.

def _cart_id(request):
    if request.user.is_authenticated:
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart
    return redirect('login')


def add_cart(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                user=request.user,
                cart_id=_cart_id(request)
            )
            cart.save(),
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=request.user)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=1,
                cart=cart
            )
            cart_item.save()
        return redirect('cart:cart_detail')
    return redirect('login')


def cart_detail(request, total=0, counter=0, cart_items=None, price=None):
    original_price=0
    saving=0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(user=request.user, cart=cart, active=True)

            print(cart_items)
            carts = CartItem.objects.filter(user=request.user)
            for cart_item in cart_items:
                cart_item.discounted_price = cart_item.product.price * (Decimal(1 - cart_item.product.discount / 100))
                total += (cart_item.discounted_price * cart_item.quantity)
                counter += cart_item.quantity
                cart_item.save()
            pricee = sum(item.discounted_price * item.quantity for item in cart_items)
            price = round(pricee)
            original_pricee = sum(item.product.price * item.quantity for item in cart_items)
            original_price = round(original_pricee)
            saving = original_price-price
        except ObjectDoesNotExist:
            pass
        return render(request, 'shopping/cart.html',
                      dict(user=request.user, cart_items=cart_items, total=total, counter=counter, price=price,original_price=original_price,saving=saving))
    return redirect('login')


from django.conf import settings
def checkout(request, total=0, counter=0, cart_items=None):
    userprofile = None  # Initialize with default value
    price = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(user=request.user, cart=cart, active=True)
            for cart_item in cart_items:
                cart_item.discounted_price = cart_item.product.price * (Decimal(1 - cart_item.product.discount / 100))
                total += (cart_item.discounted_price * cart_item.quantity)
                counter += cart_item.quantity
            price = sum(item.discounted_price * item.quantity for item in cart_items) + 40
            carts = CartItem.objects.filter(user=request.user)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                counter += cart_item.quantity
                cart_item.save()
            userprofile = Profile.objects.filter(user=request.user).first()
        except ObjectDoesNotExist:
            pass
        return render(request, 'shopping/checkout.html',
                      dict(user=request.user, cart_items=cart_items, total=total, counter=counter, price=price, userprofile=userprofile))
    return redirect('login')

def cart_remove(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart:cart_detail')
    return redirect('login')


def full_remove(request, product_id):
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart:cart_detail')
    return redirect('login')


def razorpaycheck(request):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(user=request.user, cart=cart, active=True)
    for cart_item in cart_items:
        cart_item.discounted_price = cart_item.product.price * (Decimal(1 - cart_item.product.discount / 100))
    cart_total_price = sum(item.discounted_price * item.quantity for item in cart_items) + 40
    price_int=round(cart_total_price) * 100  # Convert to paise
    response_data = {'price_int':str(price_int)}
    return JsonResponse(response_data)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(user=request.user,cart=cart, active=True)
        for cart_item in cart_items:
            cart_item.discounted_price = cart_item.product.price * (Decimal(1 - cart_item.product.discount / 100))
        cart_total_price = sum(item.discounted_price * item.quantity for item in cart_items) + 40
        neworder.total_price = cart_total_price
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        price_int = int(cart_total_price) * 100  # Convert to paise
        payment = client.order.create({'amount': price_int, 'currency': 'INR', 'payment_capture': 1})
        print('********************')
        print(payment)
        print('********************')
        for cart_item in cart_items:
            cart_item.razorpay_order_id = payment['id']
            cart_item.status = payment['status']
            cart_item.is_paid = True
            cart_item.save()

        trackno = 'beauty' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'beauty' + str(random.randint(1111111, 9999999))
        neworder.order_id = payment['id']
        neworder.tracking_no = trackno
        neworder.save()

        cart = Cart.objects.get(cart_id=_cart_id(request))
        neworderitems = CartItem.objects.filter(cart=cart)
        print(neworderitems)
        for item in neworderitems:
            price = round(item.product.discounted_price * item.quantity)
            Orderitem.objects.create(
                order=neworder,
                product=item.product,
                price=round(item.product.discounted_price),
                quantity=item.quantity,
                total_price=price,
            )

            # To decrease the product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            item.save()
            orderproduct.save()


        # To clear the cart
        # Clear the cart by deleting all cart items
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(user=request.user, cart=cart, active=True)
        cart_items.delete()
        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed successfully"})
    return redirect('/')


def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders':orders}
    return render(request,"shopping/my_orders.html",context)

def orderview(request, t_no):
    order= Order.objects.filter(tracking_no = t_no).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    for item in orderitems:
        price = item.quantity*item.price
    context = {'order':order,'orderitems':orderitems,'price':price}
    return render(request,"shopping/orderview.html",context)


def generate_payment_receipt(request, payment_id):
    order = Order.objects.filter(payment_id=payment_id).filter(user=request.user).first()
    orderitems = Orderitem.objects.filter(order=order)
    today = date.today()
    savings = 0
    for item in orderitems:
        original_price = round(item.product.price)
        discounted_price = round(item.product.discounted_price)
        result = original_price-discounted_price
        savings +=result
    # Fetch payment details from Razorpay
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.payment.fetch(payment_id)
    payment_amount = payment['amount']
    payment_date = payment['created_at']
    payment_status = payment['status']

    # Create a PDF template using xhtml2pdf
    template_path = 'shopping/receipt.html'
    context = {
        'order': order,
        'savings':savings,
        'today':today,
        'orderitems':orderitems,
        'payment_id': payment_id,
        'payment_amount': payment_amount,
        'payment_date': payment_date,
        'payment_status': payment_status
    }
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF document using xhtml2pdf
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=payment_receipt_{payment_id}.pdf'
        return response
    else:
        return HttpResponse('Error generating receipt.')

def track_order(request):
    return render(request, "shopping/track_order.html")

def Review_rate(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            prod_slug = request.GET.get('prod_slug')
            product = Product.objects.get(slug=prod_slug)
            opinion = request.GET.get('opinion')
            rating = request.GET.get('rating')
            user = request.user
            ProductReview(user=user,product=product,review_text=opinion,rating=rating).save()
            return redirect('ShoppingApp:proDetail',c_slug=product.category.slug, product_slug=prod_slug)
    return redirect('login')

def success(request, razorpay_payment_id):
    order_id = request.GET.get('order_id')
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(razorpay_order_id=order_id,user=request.user,cart=cart, active=True)
    price = sum(item.product.price * item.quantity for item in cart_items) + 40
    price_int = int(price) * 100  # Convert to paise
    for cart_item in cart_items:
        cart_item.razorpay_payment_id = razorpay_payment_id
        cart_item.is_paid = True
        cart_item.save()
        if cart_item.status == 'created':
            order = Order.objects.create(
                user=request.user,
                razorpay_order_id=cart_item.razorpay_order_id,
                total_price=price_int / 100,

            )
            order.save()

    # Clear the cart by deleting all cart items
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(user=request.user, cart=cart, active=True)
    cart_items.delete()
    return HttpResponse('Payment success')

#
# def tryon(request):
#     if request.user.is_authenticated:
#         c_page = None
#         # Load the face detector and facial landmark detector
#         face_detector = dlib.get_frontal_face_detector()
#         landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#         # Load the lipstick color image
#         lipstick = cv2.imread("static/images/maroon.jpeg")
#         # Initialize the camera capture object
#         cap = cv2.VideoCapture(0)
#
#         while True:
#             # Capture a frame from the camera
#             ret, frame = cap.read()
#             # Detect the face in the frame
#             faces = face_detector(frame)
#             # Loop over each detected face
#             for face in faces:
#                 # Detect the facial landmarks
#                 landmarks = landmark_detector(frame, face)
#                 # Extract the lip coordinates
#                 lip_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]
#                 # Draw a mask over the lips
#                 mask = np.zeros(frame.shape[:2], dtype=np.uint8)
#                 cv2.fillPoly(mask, [np.array(lip_coords)], (255, 255, 255))
#                 # Extract the lip region from the frame
#                 lip_region = cv2.bitwise_and(frame, frame, mask=mask)
#                 # Resize the lipstick image to match the lip region
#                 lipstick_resized = cv2.resize(lipstick, (lip_region.shape[1], lip_region.shape[0]))
#                 # Use the lipstick color from the center pixel of the lipstick image
#                 lipstick_color = lipstick_resized[
#                     round(lipstick_resized.shape[0] / 2), round(lipstick_resized.shape[1] / 2)]
#
#                 # Apply the lipstick color to the lip region
#                 result = np.zeros_like(lip_region)
#                 result[:, :, 0] = lipstick_color[0]
#                 result[:, :, 1] = lipstick_color[1]
#                 result[:, :, 2] = lipstick_color[2]
#
#                 # Draw the lip region with lipstick overlay on the original frame
#                 frame[mask != 0] = result[mask != 0]
#
#             # Show the resulting frame
#             cv2.imshow("Virtual try-on", frame)
#
#             # Check for key press
#             key = cv2.waitKey(5) & 0xFF
#             if key == ord('q'):
#                 break
#
#         # Release the camera capture object and close all windows
#         cap.release()
#         cv2.destroyAllWindows()
#         return redirect('ShoppingApp:allProdCat')
#
#
#     return redirect('login')
#
# def tryon_pink(request):
#     if request.user.is_authenticated:
#         c_page = None
#         # Load the face detector and facial landmark detector
#         face_detector = dlib.get_frontal_face_detector()
#         landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#
#         # Load the lipstick color image
#         lipstick = cv2.imread("static/images/rani_pink.jpeg")
#
#         # Extract the color of the center pixel in the lipstick image
#         lipstick_color = lipstick[round(lipstick.shape[0] / 2), round(lipstick.shape[1] / 2)]
#
#         # Initialize the camera capture object
#         cap = cv2.VideoCapture(0)
#
#         while True:
#             # Capture a frame from the camera
#             ret, frame = cap.read()
#
#             # Detect the face in the frame
#             faces = face_detector(frame)
#
#             # Loop over each detected face
#             for face in faces:
#                 # Detect the facial landmarks
#                 landmarks = landmark_detector(frame, face)
#
#                 # Extract the lip coordinates
#                 lip_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]
#
#                 # Draw a mask over the lips
#                 mask = np.zeros(frame.shape[:2], dtype=np.uint8)
#                 cv2.fillPoly(mask, [np.array(lip_coords)], (255, 255, 255))
#
#                 # Extract the lip region from the frame
#                 lip_region = cv2.bitwise_and(frame, frame, mask=mask)
#
#                 # Resize the lipstick image to match the lip region
#                 lipstick_resized = cv2.resize(lipstick, (lip_region.shape[1], lip_region.shape[0]))
#
#                 # Use the lipstick color from the center pixel of the lipstick image
#                 lipstick_color = lipstick_resized[
#                     round(lipstick_resized.shape[0] / 2), round(lipstick_resized.shape[1] / 2)]
#
#                 # Apply the lipstick color to the lip region
#                 result = np.zeros_like(lip_region)
#                 result[:, :, 0] = lipstick_color[0]
#                 result[:, :, 1] = lipstick_color[1]
#                 result[:, :, 2] = lipstick_color[2]
#
#                 # Draw the lip region with lipstick overlay on the original frame
#                 frame[mask != 0] = result[mask != 0]
#
#             # Show the resulting frame
#             cv2.imshow("Virtual try-on", frame)
#
#             # Check for key press
#             key = cv2.waitKey(5) & 0xFF
#             if key == ord('q'):
#                 break
#
#         # Release the camera capture object and close all windows
#         cap.release()
#         cv2.destroyAllWindows()
#         return redirect('ShoppingApp:allProdCat')
#
#     return redirect('login')
#
#
# def tryon_red(request):
#     if request.user.is_authenticated:
#         c_page = None
#         # Load the face detector and facial landmark detector
#         face_detector = dlib.get_frontal_face_detector()
#         landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#
#         # Load the lipstick color image
#         lipstick = cv2.imread("static/images/red.jpeg")
#
#         # Extract the color of the center pixel in the lipstick image
#         lipstick_color = lipstick[round(lipstick.shape[0] / 2), round(lipstick.shape[1] / 2)]
#
#         # Initialize the camera capture object
#         cap = cv2.VideoCapture(0)
#
#         while True:
#             # Capture a frame from the camera
#             ret, frame = cap.read()
#
#             # Detect the face in the frame
#             faces = face_detector(frame)
#
#             # Loop over each detected face
#             for face in faces:
#                 # Detect the facial landmarks
#                 landmarks = landmark_detector(frame, face)
#
#                 # Extract the lip coordinates
#                 lip_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]
#
#                 # Draw a mask over the lips
#                 mask = np.zeros(frame.shape[:2], dtype=np.uint8)
#                 cv2.fillPoly(mask, [np.array(lip_coords)], (255, 255, 255))
#
#                 # Extract the lip region from the frame
#                 lip_region = cv2.bitwise_and(frame, frame, mask=mask)
#
#                 # Resize the lipstick image to match the lip region
#                 lipstick_resized = cv2.resize(lipstick, (lip_region.shape[1], lip_region.shape[0]))
#
#                 # Use the lipstick color from the center pixel of the lipstick image
#                 lipstick_color = lipstick_resized[
#                     round(lipstick_resized.shape[0] / 2), round(lipstick_resized.shape[1] / 2)]
#
#                 # Apply the lipstick color to the lip region
#                 result = np.zeros_like(lip_region)
#                 result[:, :, 0] = lipstick_color[0]
#                 result[:, :, 1] = lipstick_color[1]
#                 result[:, :, 2] = lipstick_color[2]
#
#                 # Draw the lip region with lipstick overlay on the original frame
#                 frame[mask != 0] = result[mask != 0]
#
#             # Show the resulting frame
#             cv2.imshow("Virtual try-on", frame)
#
#             # Check for key press
#             key = cv2.waitKey(5) & 0xFF
#             if key == ord('q'):
#                 break
#
#         # Release the camera capture object and close all windows
#         cap.release()
#         cv2.destroyAllWindows()
#         return redirect('ShoppingApp:allProdCat')
#
#     return redirect('login')
#
# def tryon_nude_pink(request):
#     if request.user.is_authenticated:
#         # Load the face detector and facial landmark detector
#         face_detector = dlib.get_frontal_face_detector()
#         landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#
#         # Load the lipstick color image
#         lipstick = cv2.imread("static/images/nude_pink.png")
#
#         # Extract the color of the center pixel in the lipstick image
#         lipstick_color = lipstick[round(lipstick.shape[0] / 2), round(lipstick.shape[1] / 2)]
#
#         # Initialize the camera capture object
#         cap = cv2.VideoCapture(0)
#
#         while True:
#             # Capture a frame from the camera
#             ret, frame = cap.read()
#
#             # Detect the face in the frame
#             faces = face_detector(frame)
#
#             # Loop over each detected face
#             for face in faces:
#                 # Detect the facial landmarks
#                 landmarks = landmark_detector(frame, face)
#
#                 # Extract the lip coordinates
#                 lip_coords = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)]
#
#                 # Draw a mask over the lips
#                 mask = np.zeros(frame.shape[:2], dtype=np.uint8)
#                 cv2.fillPoly(mask, [np.array(lip_coords)], (255, 255, 255))
#
#                 # Extract the lip region from the frame
#                 lip_region = cv2.bitwise_and(frame, frame, mask=mask)
#
#                 # Resize the lipstick image to match the lip region
#                 lipstick_resized = cv2.resize(lipstick, (lip_region.shape[1], lip_region.shape[0]))
#
#                 # Use the lipstick color from the center pixel of the lipstick image
#                 lipstick_color = lipstick_resized[
#                     round(lipstick_resized.shape[0] / 2), round(lipstick_resized.shape[1] / 2)]
#
#                 # Apply the lipstick color to the lip region
#                 result = np.zeros_like(lip_region)
#                 result[:, :, 0] = lipstick_color[0]
#                 result[:, :, 1] = lipstick_color[1]
#                 result[:, :, 2] = lipstick_color[2]
#
#                 # Draw the lip region with lipstick overlay on the original frame
#                 frame[mask != 0] = result[mask != 0]
#
#             # Show the resulting frame
#             cv2.imshow("Virtual try-on", frame)
#
#             # Check for key press
#             key = cv2.waitKey(5) & 0xFF
#             if key == ord('q'):
#                 break
#
#         # Release the camera capture object and close all windows
#         cap.release()
#         cv2.destroyAllWindows()
#         return redirect('ShoppingApp:allProdCat')
#
#     return redirect('login')
#
# def virtual_try_on(request):
#     # Load the lipstick color images using OpenCV
#     lipstick_colors = [
#         cv2.imread('static/images/maroon.jpeg'),
#         cv2.imread('static/images/maroon.jpeg'),
#         cv2.imread('static/images/maroon.jpeg'),
#         # add more lipstick colors here
#     ]
#
#     # Initialize the webcam
#     cap = cv2.VideoCapture(0)
#
#     # Set the window size
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
#     while True:
#         if request.method == 'POST':
#             # Get the selected lipstick color from the request
#             color_index = int(request.POST.get('color_index'))
#
#             # Capture a frame from the webcam
#             _, frame = cap.read()
#
#             # Detect the user's lips using Dlib
#             detector = dlib.get_frontal_face_detector()
#             predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             rects = detector(gray, 1)
#             landmarks = predictor(gray, rects[0])
#             lips_coords = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)])
#
#             # Load the selected lipstick color image using OpenCV
#             lipstick_color = lipstick_colors[color_index]
#
#             # Resize the lipstick color image to fit the user's lips
#             lips_width = lips_coords[:, 0].max() - lips_coords[:, 0].min()
#             lips_height = lips_coords[:, 1].max() - lips_coords[:, 1].min()
#             lipstick_color_resized = cv2.resize(lipstick_color, (lips_width, lips_height))
#
#             # Apply Gaussian blur to the mask
#             mask = np.zeros_like(frame)
#             cv2.fillPoly(mask, [lips_coords], (255, 255, 255))
#             mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#             mask = cv2.GaussianBlur(mask, (11, 11), 0)
#
#             # Apply Gaussian blur to the resized lipstick color image
#             lipstick_color_resized = cv2.GaussianBlur(lipstick_color_resized, (11, 11), 0)
#
#             # Combine the mask and the lipstick color image using bitwise operations
#             mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)[1]
#             lipstick_applied = cv2.bitwise_and(frame, frame, mask=mask)
#             lipstick_applied = cv2.addWeighted(lipstick_applied, 1, lipstick_color_resized, 0.7, 0)
#
#             # Display the final image on the screen
#             cv2.imshow("Virtual Try-On", lipstick_applied)
#
#         # Check if the user presses the 'q' key to quit the program
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the webcam and close the window
#     cap.release()
#     cv2.destroyAllWindows()
#
#     # Render the virtual try-on template
#     return redirect('ShoppingApp:allProdCat')

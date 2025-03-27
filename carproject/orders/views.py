from itertools import product

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView,View, DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Reserv, ReservItem, Order, OrderItem
from newapp.models import MyCars
from django.contrib import messages







class ReservView(LoginRequiredMixin, ListView):
    template_name = 'reserv/reserv.html'
    context_object_name = 'reserv_items' #get_queryset დან მიღებულ დაჯავშნილ ReservItem ელემენტებს იღებს.
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        reserv, created = Reserv.objects.get_or_create(user=self.request.user) #აბრუნებს ან ქმნის რეზერვს self.request.user არის http მოთხოვნის გამომგზავნელი ავტორიზირებული პირი. მარცხენა არის Reserv ის ელემენტი, მარჯვენა ავტომატურად მოწოდებული იუზერი. ამით ხდება ჯავშნის კონკრეტულ მომხმარებელთან დაკავშირება.
        return ReservItem.objects.filter(reserv=reserv) #აბრუნებს მხოლოდ დარეზერვებულ მანქანებს (Reserv დაკავშირებული წინა ლოგიკის შედეგად მიღებულს) reserv=reserv მარცხენა რეზერვი ReservItem ის ელემენტია მარჯვენა წინა ლოგიკის დრო მიღეული შედეგი, ამით ხდება იუზერის დარეზერვებულის რეზერვაითემ კლასში გაფილტვრა.

    def get_context_data(self, *, object_list=None, **kwargs): #გამოიყენება შაბლონისთვი გადასაცემი კონტექსტის გასაფართოვებლად
        context = super().get_context_data(**kwargs)  #სუპერ მეთოდი გამოიყენება ListView-დან get_context_data-ს გამოსაძახებლად
        reserv_items = self.get_queryset()  #იღებს get_queryset ანუ ReservItem დან წამოღებულ დაჯავშნილ მანქანებს

        # ითვლის სრულ თანხას მანქანის ფასისა და რეზერვაციის დღეების მიხედვით
        total_amount = 0
        for item in reserv_items:
            # ითვლის რეზერვაციის დღეების ოდენობას
            reservation_days = (item.end_date - item.start_date).days
            if reservation_days > 0:
                total_amount += item.car.price * reservation_days  # ამრავლებსფასს დღეების მიხედვით

        context['total_amount'] = total_amount
        return context




class AddReservItemView(LoginRequiredMixin, View):
    def post(self, request, pk):  # Use POST instead of GET
        car = get_object_or_404(MyCars, pk=pk)

        # Get start and end dates from request.POST
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Validate start_date and end_date
        if not start_date or not end_date:
            messages.error(request, "Please provide both start and end dates.")
            return redirect(request.META.get('HTTP_REFERER', 'orders:reserv'))

        try:
            reserv, _ = Reserv.objects.get_or_create(user=request.user)

            if car.stock > 0:
                # შექმნის ან მიიღებს არსებულ reservationitem-ს
                reserv_item, reserv_item_created = ReservItem.objects.get_or_create(
                    reserv=reserv, car=car, defaults={'start_date': start_date, 'end_date': end_date}
                )

                if not reserv_item_created:
                    # Update existing reservation dates
                    reserv_item.start_date = start_date
                    reserv_item.end_date = end_date
                    reserv_item.save()

                messages.success(request, f'{car.model} was added to your reservation.')
            else:
                messages.error(request, f'Sorry, {car.model} is out of stock')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect(request.META.get('HTTP_REFERER', 'orders:reserv'))




# შლის რეზერვაციას მითითებული pk გასაღების მიღედვით
class DeleteReservItemView(LoginRequiredMixin, DeleteView):
    model = ReservItem
    success_url = reverse_lazy('orders:reserv')




class UpdateReservItemView(View):
    def post(self, request, pk):
        try:
            # Fetch the reservation item
            reserv_item = ReservItem.objects.get(pk=pk, reserv__user=request.user)

            # Get new start and end dates from the request
            new_start_date = request.POST.get('start_date')
            new_end_date = request.POST.get('end_date')

            # Validate start and end dates
            if not new_start_date or not new_end_date:
                messages.error(request, "Please provide both start and end dates.")
                return redirect('orders:reserv')

            # Update the reservation item dates
            reserv_item.start_date = new_start_date
            reserv_item.end_date = new_end_date

            # Save the changes to the reservation item
            reserv_item.save()

            messages.success(request, "Reservation dates updated successfully.")

        except ReservItem.DoesNotExist:
            messages.error(request, "Reservation item not found or you are not authorized to update it.")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('orders:reserv')


#აჩვენებს იუზერის მიერ ყველა განთავსებულ რეზერვაციას.
class OrderConfirmationView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users:login')
    template_name = 'orders/order_confirmation.html'
    context_object_name = 'reserv_items'
    success_url = reverse_lazy('orders:add_order')

    def get_queryset(self):
        reserv = Reserv.objects.get(user=self.request.user) #იღებს  Reserv ობიექტს, რომელიც დაკავშირებულია ამჟამად შესულ მომხმარებელთან.
        return ReservItem.objects.filter(reserv=reserv) # Reserv თან დაკავშირებულ ReservItem-ის დაჯავშნის ელემენტებს ფილტრავს.

    def get_context_data(self, *, object_list=None, **kwargs):  #როგორც აღინიშნა get_context_data არის ListView-ს შვილობილი ფუქნცია რომელიც გამოიყენება ობიექტების ჩამონათვლის საჩვენებლად. ამ შემთხვევაში იგი იღებს მონაცემბს get_queryset()-დან რაც თავის მხრივ მონაცემებს ირებს ReservItem-დან.
        context = super().get_context_data(**kwargs)
        reserv_items = self.get_queryset()

        total_amount = sum(item.car.price * item.rental_duration for item in reserv_items)  # Updated to calculate based on rental duration
        context['total_amount'] = total_amount

        return context



class AddOrderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def post(self, request):
        user = request.user  #მოთხოვნის ობიექტიდან ვიღებთ ამჟამინდელ ავტორიზებულ მომხმარებელს
        reserv = get_object_or_404(Reserv, user=user)  #ვიღებთ დაჯავშნის ობიექტს (Reserv) მიმდინარე მომხმარებლისთვის ან ამოაგდებს 404 შეცდომას, თუ დაჯავშნა ვერ მოიძებნა.
        reserv_items = ReservItem.objects.filter(reserv=reserv)  #ვიღებთ ამ მომხმარებლთან დაკავშირებულ დაჯავშნის ყველა ელემენტს (ReservItem)

        if not reserv_items:
            return redirect('orders:reserv')  #თუ მომხმარებელს არაფერი დაუმატებია და დაჯავშნაში ელემენტები არ არის, მომხმარებელი გადამისამართებულია დაჯავშნის გვერდზე, რათა მათ შეძლონ ნივთების დამატება ჯავშანში.

        order = Order.objects.create(user=user, total_amount=0)
        total_amount = 0

        for item in reserv_items:
            OrderItem.objects.create(order=order, car=item.car, start_date=item.start_date, end_date=item.end_date)  #თითოეული დაჯავშნილი ნივთისთვის იქმნება OrderItem ობიექტი, რომელიც აკავშირებს მანქანას შეკვეთასთან და უთითებს მის რაოდენობას.
            total_amount += item.car.price * item.rental_duration

            # Update the car's stock
            car = item.car
            if car.stock > 0:
                car.stock -= 1
                car.save()

            #შეკვეთაში ნივთის დამატების შემდეგ მას ვაშორებთ დაჯავშნიდან.
            item.delete()

        order.total_amount = total_amount
        order.save()  #ვინახავთ შეკვეთას მონაცემთა ბაზაში განახლებული სრული თანხით.

        return redirect('orders:reserv')



class ListOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')  #ეს მეთოდი კლებადობით ახარისხებს მიღებულ შეკვეთებს create_at ველის მიხედვით  (პირველი იქნება უახლესი შეკვეთა). რაც განპირობებულია - ნიშანით create_at-მდე.


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items']=OrderItem.objects.filter(order=self.object)
        return context
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import MyCars, Category
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class CarsView(TemplateView):
    template_name = 'cars/index.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')  # იღებს საძიებო მოთხოვნას
        selected_categories = request.GET.getlist('category')  # იღებს შერჩეულ კატეგორიებს URL-დან

        cars = MyCars.objects.all()

        if query:
            cars = cars.filter(
                Q(model__icontains=query) | Q(firm__icontains=query) | Q(category__category__icontains=query)
            ).distinct()  # ფილტრავს მანქანებს სახელის, ფირმის ან კატეგორიის მიხედვით

        if selected_categories:
            cars = cars.filter(category__in=selected_categories).distinct()  # ფილტრავს მანქანებს შერჩეული კატეგორიების მიხედვით

        paginator = Paginator(cars, 6)

        page_number = request.GET.get('page')  # მიმდინარე გვერდის ნომერს იღბს მოთხოვნიდან

        try:
            cars = paginator.page(page_number)  # იღებს მანქანების სწორ გვერდს
        except PageNotAnInteger:
            cars = paginator.page(1)  # თუ არ არის რიცხვი აჩვენებს პირველ გვერდს
        except EmptyPage:
            cars = paginator.page(paginator.num_pages)  # თუ მითითებული რიცხვი არ არის ხელმისაწვდომი აჩვენებს ბოლო გვერდს

        # აჯგუფებს მანქანებს კატეგორიების მიხედვით შაბლონში გამოსატანად
        categories = Category.objects.all().order_by('category')

        return render(request, self.template_name, {
            'cars': cars,
            'categories': categories,
            'selected_categories': selected_categories
        })



class MyCarsDetailView(DetailView):
    model = MyCars
    template_name = 'cars/detail_cars.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        related_cars = MyCars.objects.filter(
            category__in=car.category.all()
        ).exclude(id=car.id).distinct()[:4] #ამოიღებს მანქანებს იმავე კატეგორიებიდან, როგორიცაა ამჟამინდელი, მაგრამ გამორიცხავს თავად ამ მანქანას. ზღუდავს დაკავშირებული მანქანების რაოდენობას 4-მდე.
        context['related_cars'] = related_cars #ამატებს დაკავშირებულ მანქანებს კონტექსტში, რათა მათი გამოყენება შეიძლებოდეს შაბლონში.
        return context


class AboutUs(TemplateView):
    template_name = 'cars/about.html'
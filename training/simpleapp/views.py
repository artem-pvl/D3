# from django.shortcuts import render
from django.views.generic import ListView, DetailView  # импортируем класс, который говорит нам о том, что в этом
# представлении мы будем выводить список объектов из БД
from .models import Product, Category
from .filters import ProductFilter
from .forms import ProductForm


class ProductsList(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'products.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут
    # все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо
    # указать, чтобы обратиться к самому списку объектов через html-шаблон
    ordering = ['-price']
    paginate_by = 1  # поставим постраничный вывод в один элемент
    form_class = ProductForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя
        # метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET,
                                          queryset=self.get_queryset())  # вписываем наш фильтр в контекст

        context['categories'] = Category.objects.all()
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


# создаём представление в котором будет детали конкретного отдельного товара
class ProductDetail(DetailView):
    model = Product  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'product.html'  # название шаблона будет product.html
    context_object_name = 'product'  # название объекта. в нём будет

# Create your views here.

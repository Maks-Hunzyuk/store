from django.forms.models import BaseModelForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from orders.forms import OrderForm
from common.views import TitleMixin


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформление заказа'

    def form_valid(self, form: BaseModelForm):
        form.instance.initiator =self.request.user
        return super(OrderCreateView, self).form_valid(form)

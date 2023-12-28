from models import Basket


def baskets(request):
    user = request.user
    basket = Basket.objects.filter(user=user) if user.is_authenticated else []
    return {
        "baskets": basket
    }

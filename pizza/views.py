from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

def home(request):
    return render(request, "pizza/home.html", {})

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza  = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = "Thanks for ordering! Your %s %s and %s pizza is on its way!" %(
                filled_form.cleaned_data["size"],
                filled_form.cleaned_data["topping1"],
                filled_form.cleaned_data["topping2"]
            )
            filled_form = PizzaForm()
        else:
            created_pizza_pk = None
            note = "Failed! Please try again."
        return render(request, "pizza/order.html", {
            "pizzaform": filled_form, "note": note,
            "multiple_form": multiple_form,
            "created_pizza_pk": created_pizza_pk
        })
    else:
        form = PizzaForm()
        return render(request, "pizza/order.html", {"pizzaform": form, "multiple_form": multiple_form})

def pizzas(request):
    number_of_pizzas = 6
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            created_pizza_pks = []
            for form in filled_formset:
                created_pizza = form.save()
                created_pizza_pk = created_pizza.id
                created_pizza_pks.append(created_pizza_pk)
                print(form.cleaned_data['topping1'])
            note = "Pizzas have been ordered!"
        else:
            note = "Order wasn't created, please try again."
        return render(request, "pizza/pizzas.html", {"note": note, "formset": formset, "created_pizza_pks": created_pizza_pks})
    else:
        return render(request, "pizza/pizzas.html", {"formset": formset})

def edit_order(request, pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = "Updated!"
            return render(request, "pizza/edit_order.html", {"pizzaform": form, "pizza": pizza, "note": note})
    return render(request, "pizza/edit_order.html", {"pizzaform": form, "pizza": pizza})

        



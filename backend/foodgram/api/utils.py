from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
# from rest_framework.response import Response
from django.http import HttpResponse


def generate_pdf(recipe_info):
    pdfmetrics.registerFont(TTFont('TNR', 'times.ttf'))
    response = HttpResponse(content_type='application/pdf')

    p = canvas.Canvas(response)
    p.setFont("TNR", 20)
    text_object = p.beginText(100, 750)

    text_object.textLine('Список ингредиентов для блюд из корзины')
    counter = 1
    for ingredient, unit, amount in recipe_info:
        text_object.textLine(
            f'{counter}. {ingredient} ({unit}) - {amount}'
        )
        counter += 1
    p.drawText(text_object)
    p.showPage()
    p.save()
    return response
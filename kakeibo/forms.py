from django import forms
from .models import Kakeibo,Category


class UpdateForm(forms.ModelForm):
   class Meta:
       model = Kakeibo
       fields =['date', 'category', 'money', 'memo']
       labels={
            'date':'日付',
            'category':'カテゴリ',
            'money':'金額',
            'memo':'適用',
        }


class KakeiboForm(forms.ModelForm):
    class Meta:
        model = Kakeibo
        fields =['date', 'category', 'money', 'memo']
        labels={
            'date':'日付',
            'category':'カテゴリ',
            'money':'金額',
            'memo':'適用',
        }

class CategoryInsertForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['category_name']
        labels={
            'category_name':'カテゴリ'
        }
        


CHOICE_FIELD_RECODE_NUMBERS = (
    ('10', '10件'),
    ('15', '15件'),
    ('30', '30件'),
)

class RecordNumberForm(forms.Form):
    record_number = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'submit(this.form)'}), 
        choices=CHOICE_FIELD_RECODE_NUMBERS
    )

CHOICE_FIELD_ORDER_OPTION = (
    (0, '新着順'),
    (1, '古い順'),
)

class OrderForm(forms.Form):
    order_option = forms.ChoiceField(
        widget=forms.Select(attrs={'onchange': 'submit(this.form)'}),
        choices=CHOICE_FIELD_ORDER_OPTION
    )

   

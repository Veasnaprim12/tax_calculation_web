from django import forms


class SalaryTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    income = forms.DecimalField(
        label="ចំណូលប្រចាំឆ្នាំ",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 12,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    status = forms.ChoiceField(
        label="ស្ថានភាពគ្រួសារ",
        choices=[
            ('single', 'នៅលីវ'),
            ('married', 'រៀបការ'),
            ('family', 'មានកូន'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    wife_status = forms.ChoiceField(
        label="ស្ថានភាពប្រពន្ធ",
        choices=[
            ('housework', 'ធ្វើការផ្ទះ'),
            ('working', 'ធ្វើការ'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    dependents = forms.IntegerField(
        label="អ្នកអាស្រ័យ (នាក់)",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'class': 'form-input'
        })
    )
    
    grants_benefits = forms.DecimalField(
        label="អត្ថប្រយោជន៍សង្គម/អំណោទិ៍ (Grants/Benefits)",
        min_value=0,
        initial=0,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'class': 'form-input',
            'step': '0.01'
        })
    )


class PropertyTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    property_value = forms.DecimalField(
        label="តម្លៃអចលនទ្រព្យ",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 50,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    property_type = forms.ChoiceField(
        label="ប្រភេទអចលនទ្រព្យ",
        choices=[
            ('house', 'ផ្ទះ'),
            ('land', 'ដី'),
            ('apartment', 'អាផាតមិន'),
            ('commercial', 'អាជីវកម្ម'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class VATTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    amount = forms.DecimalField(
        label="តម្លៃលក់ (មិនរាប់ពន្ធ)",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )


# Keep the old form for backward compatibility
class TaxCalculatorForm(SalaryTaxForm):
    pass
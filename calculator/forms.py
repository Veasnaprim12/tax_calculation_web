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
class SpecialTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    product_origin = forms.ChoiceField(
        label="ដើមកំណើតទំនិញ",
        choices=[
            ('local', 'ទំនិញក្នុងស្រុក'),
            ('imported', 'ទំនិញនាំចូល'),
        ],
        initial='local',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    selling_price = forms.DecimalField(
        label="តម្លៃលក់ (មិនរាប់ពន្ធ)",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    product_type = forms.ChoiceField(
        label="ប្រភេទទំនិញ/សេវាកម្ម",
        choices=[
            ('spirits', 'សុរាវ/ម្សាធារ - 35%'),
            ('beer_restaurant', 'ម្សាធារលបៀរ - 30%'),
            ('liquor', 'បារី - 20%'),
            ('karaoke', 'បារីសីហ្គា វ - 25%'),
            ('furniture', 'ផ្គូផ្គង/ដើម - 10%'),
            ('silkworm', 'សូលឺម៉ាងត្ិ៍ - 5%'),
            ('transport', 'ដឹកជញ្ជូន - 10%'),
            ('telecom', 'ទូរគមនាគមន៍ - 3%'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
class AccomodationTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    room_price = forms.DecimalField(
        label="តម្លៃបន្ទប់",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    services_charge = forms.DecimalField(
        label="ថ្លៃសេវាកម្ម (ប្រសិនបើមាន)",
        min_value=0,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 500,000 (ឯកចិត្ត)',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    


class IncomeTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    income_type = forms.ChoiceField(
        label="ប្រភេទចំណូល",
        choices=[
            ('investment', 'ចំណូលវិនិយោគ (Dividend/Interest)'),
            ('business', 'ចំណូលពីលុយប្រតិបត្តិការ'),
            ('rental', 'ចំណូលឈ្នួលផ្ទះ'),
            ('other', 'ចំណូលផ្សេងទៀត'),
        ],
        initial='investment',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    income = forms.DecimalField(
        label="ចំណូលប្រចាំឆ្នាំ",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 5,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    business_expenses = forms.DecimalField(
        label="ការចំណាយលើលុយប្រតិបត្តិការ (ប្រសិនបើអាច)",
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


# Keep the old form for backward compatibility
class TaxCalculatorForm(SalaryTaxForm):
    pass


class WithholdingTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    withholding_type = forms.ChoiceField(
        label="ប្រភេទពន្ធកាត់ទុក",
        choices=[
            ('salary', 'ពន្ធកាត់ទុកលើប្រាក់ឈ្នួល'),
            ('dividend', 'ពន្ធកាត់ទុកលើផលប័ត្រ/ក្រុមហ៊ុន'),
            ('rental', 'ពន្ធកាត់ទុកលើឈ្នួលផ្ទះ'),
            ('other', 'ពន្ធកាត់ទុកផ្សេងទៀត'),
        ],
        initial='salary',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    amount = forms.DecimalField(
        label="ចំនួនដើម",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 5,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
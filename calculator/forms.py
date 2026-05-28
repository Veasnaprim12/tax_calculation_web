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
        label="អត្ថប្រយោជន៍សង្គម/អំណោយ (Grants/Benefits)",
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


class PatentTaxForm(forms.Form):
    category = forms.ChoiceField(
        label="ប្រភេទអ្នកជាប់ពន្ធ",
        choices=[
            ('small', 'អ្នកជាប់ពន្ធតូច (Small Taxpayer) - 400,000 ៛'),
            ('medium', 'អ្នកជាប់ពន្ធមធ្យម (Medium Taxpayer) - 1,200,000 ៛'),
            ('large', 'អ្នកជាប់ពន្ធធំ (Large Taxpayer) - 3,000,000 ៛'),
            ('large_above_10b', 'អ្នកជាប់ពន្ធធំ របរលើស ១០ប៊ីលានរៀល (Large > 10B KHR) - 5,000,000 ៛'),
        ],
        initial='small',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    activities = forms.IntegerField(
        label="ចំនួនសកម្មភាពអាជីវកម្ម",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 1',
            'class': 'form-input'
        })
    )
    
    timing = forms.ChoiceField(
        label="កាលបរិច្ឆេទបង្កើតអាជីវកម្ម",
        choices=[
            ('existing', 'អាជីវកម្មដែលមានស្រាប់ (បង់ពន្ធពេញឆ្នាំ)'),
            ('new_first_half', 'អាជីវកម្មថ្មី បង្កើតក្នុងឆមាសទី១ (Jan - Jun) - បង់ពេញ'),
            ('new_second_half', 'អាជីវកម្មថ្មី បង្កើតក្នុងឆមាសទី២ (Jul - Dec) - បង់ពាក់កណ្តាល'),
        ],
        initial='existing',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    branches = forms.IntegerField(
        label="ចំនួនសាខា/ឃ្លាំង នៅខេត្តផ្សេងទៀត",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 0',
            'class': 'form-input'
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
    
    transaction_value = forms.DecimalField(
        label="តម្លៃផ្គត់ផ្គង់/តម្លៃគយរួមពន្ធនាំចូល",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    transaction_type = forms.ChoiceField(
        label="ប្រភេទមុខទំនិញ/សេវាកម្ម",
        choices=[
            ('alcohol', 'គ្រឿងស្រវឹង (Alcohol) - 35%'),
            ('beer', 'ស្រាបៀរ (Beer) - 30%'),
            ('cigars', 'បារីស៊ីហ្គា (Cigars) - 25%'),
            ('cigarettes', 'បារីសាមញ្ញ (Cigarettes) - 20%'),
            ('energy_drinks', 'ភេសជ្ជៈពៅកម្លាំង (Energy Drinks) - 15%'),
            ('non_alcoholic', 'ភេសជ្ជៈគ្មានជាតិអាល់កុល/ទឹកផ្អែម - 10%'),
            ('plastic', 'ផលិតផលផ្លាស្ទិក (Plastic Products) - 10%'),
            ('air_transport', 'សេវាដឹកជញ្ជូនអ្នកដំណើរតាមផ្លូវអាកាស - 10%'),
            ('entertainment', 'សេវាកម្សាន្ត (ខារ៉ាអូខេ ម៉ាស្សា ហ្គោល...) - 10%'),
            ('fruit_juice', 'ទឹកផ្លែឈើ (Fruit Juice) - 5%'),
            ('cement', 'ស៊ីម៉ង់ត៍ (Cement) - 5%'),
            ('telecom', 'សេវាទូរគមនាគមន៍ (Telecom Services) - 3%'),
        ],
        initial='beer',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    supply_type = forms.ChoiceField(
        label="ប្រភេទនៃការផ្គត់ផ្គង់",
        choices=[
            ('domestic', 'ទំនិញក្នុងស្រុក (គិតពន្ធលើ ៩០% នៃតម្លៃវិក្កយបត្រ)'),
            ('service', 'សេវាកម្ម (គិតពន្ធលើ ១០០% នៃតម្លៃសេវា)'),
            ('import', 'ទំនិញនាំចូល (គិតពន្ធលើ ១០០% នៃតម្លៃគយរួមពន្ធនាំចូល)'),
        ],
        initial='domestic',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    number_of_transactions = forms.IntegerField(
        label="ចំនួនប្រតិបត្តិការ/បរិមាណ",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'placeholder': '1',
            'class': 'form-input'
        })
    )


class RegistrationTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    asset_type = forms.ChoiceField(
        label="ប្រភេទទ្រព្យសម្បត្តិផ្ទេរកម្មសិទ្ធិ",
        choices=[
            ('immovable', 'អចលនទ្រព្យ (Immovable Property)'),
            ('vehicle', 'យានយន្ត/មធ្យោបាយដឹកជញ្ជូន (Vehicle)'),
        ],
        initial='immovable',
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleRegistrationFields()'})
    )
    
    property_value = forms.DecimalField(
        label="តម្លៃវាយតម្លៃទ្រព្យសម្បត្តិ",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 50,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    relationship = forms.ChoiceField(
        label="ទំនាក់ទំនងសាច់ញាតិ (សម្រាប់តែអចលនទ្រព្យ)",
        choices=[
            ('none', 'គ្មានការលើកលែង (ផ្ទេរកម្មសិទ្ធិទូទៅ)'),
            ('immediate_exempt', 'សាច់ញាតិផ្ទាល់ (ប្តី-ប្រពន្ធ ឪពុកម្តាយ-កូន ជីដូនជីតា-ចៅ) - លើកលែងពន្ធ ១០០%'),
            ('extended_inheritance', 'បងប្អូនបង្កើត ឬ ដន្លងនិងកូនប្រសារ (មរតក - កាត់កង ២០០លានរៀល)'),
            ('extended_gift', 'បងប្អូនបង្កើត ឬ ដន្លងនិងកូនប្រសារ (អំណោយលើកដំបូង - កាត់កង ១០០លានរៀល)'),
        ],
        initial='none',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    is_vehicle_exempt = forms.BooleanField(
        label="យានយន្តប្រភេទលើកលែងពន្ធ (ម៉ូតូ កង់បី ត្រាក់ទ័រ កាណូត/នាវា <= ១៥០ សេះ)",
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class UnusedLandTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    land_area_sqm = forms.DecimalField(
        label="ផ្ទៃដីសរុប (ម៉ែត្រការ៉េ - ម២)",
        min_value=1,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 60,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    land_value = forms.DecimalField(
        label="តម្លៃដីក្នុងមួយម៉ែត្រការ៉េ (តម្លៃវាយតម្លៃដោយគណៈកម្មការ)",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 15,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
    
    years_unused = forms.IntegerField(
        label="ចំនួនឆ្នាំដែលដីមិនប្រើប្រាស់",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'placeholder': '1',
            'class': 'form-input'
        })
    )
    
    urban_type = forms.ChoiceField(
        label="ប្រភេទតំបន់ដី (ជាព័ត៌មានបន្ថែម)",
        choices=[
            ('urban', 'តំបន់ទីប្រជុំជន/ទីក្រុង'),
            ('suburban', 'តំបន់ជាយក្រុង'),
            ('rural', 'តំបន់ជនបទ'),
        ],
        initial='urban',
        required=False,
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
    
    nights = forms.IntegerField(
        label="ចំនួនបន្ទប់-យប់ (Room-Nights)",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10',
            'class': 'form-input'
        })
    )
    
    room_rate = forms.DecimalField(
        label="តម្លៃបន្ទប់ក្នុងមួយយប់ (Room Rate per Night)",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 100,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
class PLTTaxForm(forms.Form):
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
        label="ចំនួនដើម",
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 10,000,000',
            'class': 'form-input',
            'step': '0.01'
        })
    )
class TransportationTaxForm(forms.Form):
    currency = forms.ChoiceField(
        label="រូបិយប័ណ្ណ",
        choices=[
            ('KHR', '៛ រៀលកម្ពុជា'),
            ('USD', '$ ដុល្លារអាមេរិក'),
        ],
        initial='KHR',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    vehicle_type = forms.ChoiceField(
        label="ប្រភេទយានជំនិះ",
        choices=[
            ('car_sedan_suv', 'រថយន្តទេសចរណ៍ (Sedan, SUV, លក្ខណៈគ្រួសារ)'),
            ('motorcycle', 'ម៉ូតូ ឬរ៉ឺម៉កកង់បី (Motorcycle/TukTuk)'),
            ('truck_bus', 'រថយន្តដឹកទំនិញ ឬរថយន្តក្រុងដឹកអ្នកដំណើរ'),
        ],
        initial='car_sedan_suv',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    engine_capacity = forms.IntegerField(
        label="កម្លាំងម៉ាស៊ីន / ទំហំស៊ីឡាំង (CC)",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'ឧ. 1800 (គិតជា CC)',
            'class': 'form-input',
            'step': '1'
        })
    )
    
    # បង្កើតបញ្ជីឆ្នាំផលិតថយក្រោយ (ឡានចាស់បំផុតត្រឹមឆ្នាំ ១៩៨០ រហូតដល់ឆ្នាំបច្ចុប្បន្ន ២០២៦)
    CURRENT_YEAR = 2026
    YEAR_CHOICES = [(str(year), str(year)) for year in range(CURRENT_YEAR, 1979, -1)]
    
    manufacture_year = forms.ChoiceField(
        label="ឆ្នាំផលិតយានជំនិះ",
        choices=YEAR_CHOICES,
        initial=str(CURRENT_YEAR),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    is_late = forms.BooleanField(
        label="បង់ប្រាក់ពន្ធយឺតយ៉ាវ (ហួសថ្ងៃទី ៣០ ខែកញ្ញា)",
        required=False, # មិនបង្ខំឱ្យទំពក់យកទេ (Optional checkbox)
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox',
            'style': 'margin-right: 8px; transform: scale(1.2);'
        })
    )
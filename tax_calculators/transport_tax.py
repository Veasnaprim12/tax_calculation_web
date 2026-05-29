from decimal import Decimal

def calculate_vehicle_tax(vehicle_type, cylinder_capacity, manufacture_year):
    """
    គណនាពន្ធលើមធ្យោបាយដឹកជញ្ជូន (ពន្ធផ្លូវ) សម្រាប់ប្រទេសកម្ពុជា។
    តម្លៃនេះជាតម្លៃគំរូតាមប្រភេទរថយន្តទេសចរណ៍ទូទៅ (រៀល - KHR)។
    """
    tax_amount = Decimal('0.00')
    
    # បំប្លែងឆ្នាំទៅជាអាយុកាលរថយន្ត (Current Year គឺ ២០២៦)
    current_year = 2026
    age_of_vehicle = current_year - int(manufacture_year)
    
    if vehicle_type == 'car_sedan_suv':
        # កាត់បន្ថយតម្លៃពន្ធបើឡានអាយុកាលចាស់ (ឧទាហរណ៍៖ លើសពី ១០ ឆ្នាំ)
        is_old = age_of_vehicle > 10
        
        if cylinder_capacity <= 1000:
            tax_amount = Decimal('100000') if not is_old else Decimal('60000')
        elif 1000 < cylinder_capacity <= 1500:
            tax_amount = Decimal('150000') if not is_old else Decimal('100000')
        elif 1500 < cylinder_capacity <= 2000:
            # ឡានទូទៅដូចជា Prius, Camry, Morning
            tax_amount = Decimal('200000') if not is_old else Decimal('150000')
        elif 2000 < cylinder_capacity <= 3000:
            # ឡានប្រភេទ SUV ឬ Sedan ធំៗ
            tax_amount = Decimal('500000') if not is_old else Decimal('350000')
        else:
            # ឡានកម្លាំងខ្លាំង (ទំហំស៊ីឡាំងលើសពី 3000cc)
            tax_amount = Decimal('1000000') if not is_old else Decimal('700000')
            
    elif vehicle_type == 'motorcycle':
        if cylinder_capacity <= 125:
            # ម៉ូតូកម្លាំងត្រឹម ១២៥សេសេ ចុះក្រោម ត្រូវលើកលែងពន្ធជារៀងរហូត
            tax_amount = Decimal('0')
        elif 125 < cylinder_capacity <= 250:
            tax_amount = Decimal('10000')
        else:
            tax_amount = Decimal('20000')
            
    else:
        # សម្រាប់ប្រភេទឡានដឹកទំនិញ ឬឡានក្រុង (គិតតាមទម្ងន់សរុប ឬចំនួនកៅអី)
        tax_amount = Decimal('250000') 
        
    return tax_amount

# ឧទាហរណ៍នៃការដកស្រង់យកទៅប្រើប្រាស់៖
# ឡាន Prius ផលិតឆ្នាំ 2010 (កម្លាំង 1800cc) គិតក្នុងឆ្នាំ ២០២៦ គឺអាយុកាល ១៦ឆ្នាំ (ឡានចាស់)
prusa_tax = calculate_vehicle_tax(
    vehicle_type='car_sedan_suv', 
    cylinder_capacity=1800, 
    manufacture_year=2010
)
print(f"ប្រាក់ពន្ធផ្លូវត្រូវបង់៖ {prusa_tax:,} រៀល")
# ទិន្នផល៖ ប្រាក់ពន្ធផ្លូវត្រូវបង់៖ 150,000 រៀល
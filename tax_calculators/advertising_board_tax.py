from decimal import Decimal, ROUND_CEILING


FOREIGN_LETTER_RATE = Decimal("2000")


def _ceil_decimal(value):
    return Decimal(value).to_integral_value(rounding=ROUND_CEILING)


def calculate_advertising_board_tax(
    board_type,
    width_m,
    height_m,
    quantity,
    display_type,
    declaration_period,
    foreign_letter_dm=0,
):
    width_dm = Decimal(width_m) * Decimal("10")
    height_dm = Decimal(height_m) * Decimal("10")
    area_dm2 = width_dm * height_dm
    quantity = Decimal(quantity)
    foreign_letter_dm = _ceil_decimal(foreign_letter_dm or 0)

    rate = Decimal("0")
    base_tax = Decimal("0")
    foreign_tax = Decimal("0")
    notes = []

    if board_type == "paper_poster":
        rate = Decimal("500") if area_dm2 <= Decimal("40") else Decimal("700")
        foreign_rate = Decimal("1500") if area_dm2 <= Decimal("40") else Decimal("2100")
        base_tax = rate * quantity
        foreign_tax = foreign_rate * quantity if foreign_letter_dm > 0 else Decimal("0")
    elif board_type == "material_poster":
        if area_dm2 <= Decimal("40"):
            rate = Decimal("700")
            foreign_rate = Decimal("2100")
        elif area_dm2 <= Decimal("100"):
            rate = Decimal("1000")
            foreign_rate = Decimal("3000")
        else:
            notes.append("ផ្ទៃក្រឡាលើស 100 ដេស៊ីម៉ែត្រការ៉េ ដូច្នេះត្រូវគិតជាផ្ទាំងអក្សរ ឬផ្ទាំងរូបភាព។")
            rate = _display_rate("text_image", display_type)
            foreign_rate = FOREIGN_LETTER_RATE

        if area_dm2 <= Decimal("100"):
            base_tax = rate * quantity
            foreign_tax = foreign_rate * quantity if foreign_letter_dm > 0 else Decimal("0")
        else:
            base_tax = area_dm2 * rate * quantity
            foreign_tax = foreign_letter_dm * foreign_rate * quantity
    else:
        rate = _display_rate(board_type, display_type)
        base_tax = area_dm2 * rate * quantity
        foreign_tax = foreign_letter_dm * FOREIGN_LETTER_RATE * quantity

    subtotal = base_tax + foreign_tax
    period_multiplier = Decimal("1") if declaration_period == "first_half" else Decimal("0.5")
    total_tax = subtotal * period_multiplier

    return {
        "width_dm": width_dm,
        "height_dm": height_dm,
        "area_dm2": area_dm2,
        "quantity": quantity,
        "rate": rate,
        "base_tax": base_tax,
        "foreign_letter_dm": foreign_letter_dm,
        "foreign_tax": foreign_tax,
        "period_multiplier": period_multiplier,
        "total_tax": total_tax,
        "notes": notes,
    }


def _display_rate(board_type, display_type):
    business_sign_rates = {
        "no_light_parallel": Decimal("100"),
        "no_light_perpendicular": Decimal("150"),
        "light_parallel": Decimal("200"),
        "light_perpendicular": Decimal("250"),
    }
    text_image_rates = {
        "no_light_parallel": Decimal("500"),
        "no_light_perpendicular": Decimal("700"),
        "light_parallel": Decimal("700"),
        "light_perpendicular": Decimal("1000"),
        "vehicle": Decimal("1500"),
    }

    if board_type == "business_sign":
        return business_sign_rates.get(display_type, Decimal("100"))
    return text_image_rates.get(display_type, Decimal("500"))

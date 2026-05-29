from decimal import Decimal, ROUND_CEILING


# =====================================================
# FOREIGN LANGUAGE TAX RATES
# =====================================================

BUSINESS_FOREIGN_RATES = {

    "no_light_parallel": Decimal("200"),

    "no_light_perpendicular": Decimal("300"),

    "light_parallel": Decimal("400"),

    "light_perpendicular": Decimal("500"),

}


TEXT_IMAGE_FOREIGN_RATES = {

    "no_light_parallel": Decimal("1000"),

    "no_light_perpendicular": Decimal("1400"),

    "light_parallel": Decimal("1400"),

    "light_perpendicular": Decimal("2000"),

    "vehicle": Decimal("3000"),

}


# =====================================================
# ROUND UP HELPER
# =====================================================

def _ceil_decimal(value):

    return Decimal(value).to_integral_value(
        rounding=ROUND_CEILING
    )


# =====================================================
# MAIN CALCULATION
# =====================================================

def calculate_advertising_board_tax(
    board_type,
    width_m,
    height_m,
    quantity,
    display_type,
    declaration_period,
    foreign_letter_dm=0,
):

    # -----------------------------------------
    # CONVERT TO DECIMETER
    # -----------------------------------------

    width_dm = Decimal(str(width_m)) * Decimal("10")

    height_dm = Decimal(str(height_m)) * Decimal("10")

    area_dm2 = width_dm * height_dm

    quantity = Decimal(str(quantity))

    foreign_letter_dm = _ceil_decimal(
        foreign_letter_dm or 0
    )

    # -----------------------------------------
    # INITIALIZE
    # -----------------------------------------

    rate = Decimal("0")

    base_tax = Decimal("0")

    foreign_tax = Decimal("0")

    notes = []

    # =====================================================
    # 1. PAPER POSTER
    # =====================================================

    if board_type == "paper_poster":

        if area_dm2 <= Decimal("40"):

            rate = Decimal("500")

            foreign_rate = Decimal("1500")

        else:

            rate = Decimal("700")

            foreign_rate = Decimal("2100")

        base_tax = rate * quantity

        if foreign_letter_dm > 0:

            foreign_tax = (
                foreign_rate
                * quantity
            )

    # =====================================================
    # 2. RUBBER / CLOTH / MATERIAL POSTER
    # =====================================================

    elif board_type == "material_poster":

        # <= 40 dm²

        if area_dm2 <= Decimal("40"):

            rate = Decimal("700")

            foreign_rate = Decimal("2100")

            base_tax = rate * quantity

            if foreign_letter_dm > 0:

                foreign_tax = (
                    foreign_rate
                    * quantity
                )

        # >40 to 100 dm²

        elif area_dm2 <= Decimal("100"):

            rate = Decimal("1000")

            foreign_rate = Decimal("3000")

            base_tax = rate * quantity

            if foreign_letter_dm > 0:

                foreign_tax = (
                    foreign_rate
                    * quantity
                )

        # >100 dm² = commercial board

        else:

            notes.append(
                "Area exceeds 100 dm², "
                "therefore calculated as "
                "commercial letter/picture board."
            )

            rate = _display_rate(
                "text_image",
                display_type
            )

            base_tax = (
                area_dm2
                * rate
                * quantity
            )

            foreign_rate = TEXT_IMAGE_FOREIGN_RATES.get(
                display_type,
                Decimal("1000")
            )

            foreign_tax = (
                foreign_letter_dm
                * foreign_rate
                * quantity
            )

    # =====================================================
    # 3. BUSINESS SIGNBOARD
    # =====================================================

    elif board_type == "business_sign":

        rate = _display_rate(
            "business_sign",
            display_type
        )

        base_tax = (
            area_dm2
            * rate
            * quantity
        )

        foreign_rate = BUSINESS_FOREIGN_RATES.get(
            display_type,
            Decimal("200")
        )

        foreign_tax = (
            foreign_letter_dm
            * foreign_rate
            * quantity
        )

    # =====================================================
    # 4. LETTER / PICTURE BOARD
    # =====================================================

    elif board_type == "text_image":

        rate = _display_rate(
            "text_image",
            display_type
        )

        base_tax = (
            area_dm2
            * rate
            * quantity
        )

        foreign_rate = TEXT_IMAGE_FOREIGN_RATES.get(
            display_type,
            Decimal("1000")
        )

        foreign_tax = (
            foreign_letter_dm
            * foreign_rate
            * quantity
        )

    # =====================================================
    # 5. VEHICLE ADVERTISEMENT
    # =====================================================

    elif board_type == "vehicle":

        rate = Decimal("1500")

        base_tax = (
            area_dm2
            * rate
            * quantity
        )

        foreign_tax = (
            foreign_letter_dm
            * Decimal("3000")
            * quantity
        )

    # =====================================================
    # SUBTOTAL
    # =====================================================

    subtotal = base_tax + foreign_tax

    # =====================================================
    # PERIOD MULTIPLIER
    # =====================================================

    if declaration_period == "first_half":

        period_multiplier = Decimal("1")

    else:

        period_multiplier = Decimal("0.5")

    # =====================================================
    # TOTAL TAX
    # =====================================================

    total_tax = subtotal * period_multiplier

    # =====================================================
    # RETURN RESULT
    # =====================================================

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


# =====================================================
# DISPLAY RATE LOOKUP
# =====================================================

def _display_rate(
    board_type,
    display_type
):

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

    # BUSINESS SIGNBOARD

    if board_type == "business_sign":

        return business_sign_rates.get(
            display_type,
            Decimal("100")
        )

    # COMMERCIAL BOARD

    return text_image_rates.get(
        display_type,
        Decimal("500")
    )
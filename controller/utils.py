def parse_set_id_from_button_name(button_name: str) -> int:
    return int(button_name.split(':')[0])


def validate_set_id_in_button_name(button_name: str) -> bool:
    try:
        parse_set_id_from_button_name(button_name)
        return True
    except ValueError:
        return False

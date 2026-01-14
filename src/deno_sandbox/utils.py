import re


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_to_camel_case(data):
    if isinstance(data, dict):
        return {to_camel_case(k): convert_to_camel_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_camel_case(i) for i in data]
    else:
        return data


def to_snake_case(camel_str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def convert_to_snake_case(data):
    if isinstance(data, dict):
        return {to_snake_case(k): convert_to_snake_case(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_snake_case(i) for i in data]
    else:
        return data

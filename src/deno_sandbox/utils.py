import re


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_keys_camel(data):
    if isinstance(data, dict):
        return {to_camel_case(k): convert_keys_camel(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_camel(i) for i in data]
    else:
        return data


def to_snake_case(camel_str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def convert_to_snake(data):
    if isinstance(data, dict):
        return {to_snake_case(k): convert_to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_snake(i) for i in data]
    else:
        return data

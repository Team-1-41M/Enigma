def create(content_list, element_data):
    id = element_data["id"]

    if any(e["id"] == id for e in content_list):
        return

    content_list.append(element_data)

    return content_list


def _is_default(value) -> bool:
    """
    Checks if value is default.

    Args:
        value: value to check.

    Returns:
        bool: True if value is default, False otherwise.
    """

    if isinstance(value, int) or isinstance(value, float):
        return value == 0

    if isinstance(value, str):
        return value == ""

    return False


def _remove_defaults(data: dict) -> dict:
    """
    Removes default values from data.

    Args:
        data: data to remove default values from.

    Returns:
        dict: data without default values.
    """

    undefaulted = {}

    for key, value in data.items():
        if value is not None and not _is_default(value):
            undefaulted[key] = value

    return undefaulted


def update(content_list, element_data):
    for i, element in enumerate(content_list):
        if element["id"] == element_data["id"]:
            for key, value in element_data.items():
                content_list[i][key] = value
            content_list[i] = _remove_defaults(content_list[i])
            break

    return content_list


def put(content_list, element_data):
    foundIndex = next(
        (i for i, e in enumerate(content_list) if e["id"] == element_data["id"]), None
    )
    if foundIndex is None:
        return
    found = content_list[foundIndex]
    temp = content_list[:foundIndex] + content_list[foundIndex + 1 :]

    newIndex = 0
    if "after" in element_data:
        whomIndex = next(
            (i for i, e in enumerate(temp) if e["id"] == element_data["after"]), None
        )
        if whomIndex is None:
            return
        newIndex = whomIndex + 1

    return temp[:newIndex] + [found] + temp[newIndex:]


def delete(elements, id):
    def find_descendants(id):
        return [element["id"] for element in elements if element.get("parent") == id]

    def delete_recursive(id):
        descendants = find_descendants(id)
        for descendant in descendants:
            delete_recursive(descendant)
        nonlocal elements
        elements = [element for element in elements if element["id"] != id]

    delete_recursive(id)

    return elements

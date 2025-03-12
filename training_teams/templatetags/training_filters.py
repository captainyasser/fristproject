from django import template

register = template.Library()

@register.filter
def dict_to_list(dict_items):
    """Convert dict_items to a list"""
    return list(dict_items)

@register.filter
def chunk_vertical(value, columns):
    """
    يقسم القائمة إلى أعمدة عمودية.
    """
    chunk_size = (len(value) + columns - 1) // columns
    result = []
    for i in range(chunk_size):
        row = []
        for j in range(columns):
            index = i + j * chunk_size
            if index < len(value):
                row.append(value[index])
            else:
                row.append((None, None))  # إضافة صف فارغ
        result.append(row)
    return result


# @register.filter
# def range_filter(value):
#     """Generate a range from 0 to the given value."""
#     return range(value)

# @register.filter
# def get_item(sequence, index):
#     """Get an item from a sequence by index."""
#     try:
#         return sequence[index]
#     except (IndexError, TypeError):
#         return None
    
    
    
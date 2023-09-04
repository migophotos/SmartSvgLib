from xml.dom import minidom


def add_element(element_type, params_dict, document, parent_elem=None):
    """
    Creates svg element, sets attributes and append it to parent, if it not null
    the new element returned
    Usage example: createElement('circle',{cx:50,cy:50,r:10})
    Special case for 'text' element creation: append pair text:'any text...' into params object
    and this text will be automatically appended to 'text' element
    """
    # Fix for error: <circle > attribute r: Negative value is not valid!
    if element_type == "circle" and params_dict['r'] < 0:
        params_dict['r'] = 1
    namespace = "http://www.w3.org/2000/svg"
    text_data = ""

    elem = document.createElementNS(namespace, element_type)
    for key in params_dict.keys():
        if key == "text":
            text_data = params_dict[key]
        else:
            elem.setAttribute(key, params_dict[key])

    if parent_elem is not None:
        parent_elem.appendChild(elem)
    if element_type == 'text' or element_type == 'textPath':
        elem.appendChild(document.createTextNode(text_data))

    return elem

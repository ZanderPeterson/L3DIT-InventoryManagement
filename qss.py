# QSS (Effectively CSS)
# Due to the use of f-strings, double curly brackets must be used where normally only one would be required.
no_qss: str = f"""
    border: none; 
    padding: 0px; 
    margin: 0px;
"""
basic_element: str = f"""
    background-color: #cccccc; 
    color: black; 
    padding: 10px; 
    border: 2px solid black; 
    border-radius: 16px;
"""
basic_button_hover: str = f"""
    border-color: #5555cc;
"""
basic_button_pressed: str = f"""
    border-color: #5555cc;
"""
inventory_available_button_style: str = f"""
    QPushButton {{
        {basic_element}
        background-color: #aaffaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}

    }}
    QPushButton:checked {{
        {basic_button_pressed}
        background-color: #55ff55;
    }}
"""
inventory_unavailable_button_style: str = f"""
    QPushButton {{
        {basic_element}
        background-color: #ffaaaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}

    }}
    QPushButton:checked {{
        {basic_button_pressed}
        background-color: #ff5555;
    }}
"""

noissues_button_style: str = f"""
    QPushButton {{
        {basic_element}
        background-color: #aaffaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}

    }}
    QPushButton:checked {{
        {basic_button_pressed}
        background-color: #55ff55;
    }}
"""

issues_button_style: str = f"""
    QPushButton {{
        {basic_element}
        background-color: #ffffaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}

    }}
    QPushButton:checked {{
        {basic_button_pressed}
        background-color: #ffff55;
    }}
"""

all_button_style: str = f"""
    QPushButton {{
        {basic_element}
        background-color: #ffaaaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}

    }}
    QPushButton:checked {{
        {basic_button_pressed}
        background-color: #ff5555;
    }}
"""

item_list_available: str = f"""
    {basic_element}
    background-color: #55ff55;
"""

item_list_unavailable: str = f"""
    {basic_element}
    background-color: #ff5555;
"""

item_in_list: str = f"""
    {basic_element}
    padding: 0px;
"""

item_label: str = f"""
    {no_qss}
    padding: 10px;
    border: 4px solid rgba(0, 0, 0, 0);
"""

item_checkout_button: str = f"""
    QPushButton {{
        {basic_element}
        margin: 0px;
        background-color: #ffffaa;
    }}
    QPushButton:hover {{
        {basic_button_hover}
        margin: 0px;
    }}
    QPushButton:checked {{
        {basic_button_pressed}
        margin: 0px;
        background-color: #ffff55;
    }}
"""

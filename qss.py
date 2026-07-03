# QSS (Effectively CSS)
# Due to the use of f-strings, double curly brackets must be used where normally only one would be required.
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

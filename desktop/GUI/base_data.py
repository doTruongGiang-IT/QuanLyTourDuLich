from GUI.pages.customer import CustomerGUI
from .pages.tour import TourGUI
from .pages.group import GroupGUI

MENU = {
    "menu_tour_management": {
        "name": "Tour Management",
        "data": [
            ["menu_tour_management_tour", "Tour", TourGUI.tour_render_callback],
            ["menu_tour_management_tour_characteristic", "Tour Characteristic", TourGUI.tour_characteristic_render_callback],
            ["menu_tour_management_tour_type", "Tour Type", TourGUI.tour_type_render_callback],
            ["menu_tour_management_tour_price", "Tour Price", TourGUI.tour_price_render_callback],
            ["menu_tour_management_tour_location", "Location", TourGUI.location_render_callback],
        ]
    },
    "menu_group_management": {
        "name": "Group Management",
        "data": [
            ["menu_group_management_group", "Group", GroupGUI.group_render_callback],
        ]
    },
    "menu_customer_managment": {
        "name": "People Management",
        "data": [
            ["menu_customer_management_customer", "Customer", CustomerGUI.customer_render_callback],
        ]
    },
    "menu_statictis": {
        "name": "Statistic",
        "data": [
            ["menu_statistic_general", "General", TourGUI.tour_render_callback],
            ["menu_statistic_tour_statistic", "Tour Status", TourGUI.tour_render_callback],
            ["menu_statistic_revenue", "Revenue", TourGUI.tour_render_callback],
        ]
    }
}


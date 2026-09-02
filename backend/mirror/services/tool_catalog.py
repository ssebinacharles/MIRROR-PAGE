from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ToolProfile:
    name: str
    risk_level: str = 'LOW'
    read_only: bool = True
    side_effect: bool = False
    financial: bool = False
    reversible: bool = True
    requires_approval: bool = False
    data_scope: tuple[str, ...] = ()

BUILTIN_TOOLS = {
    'search_products': ToolProfile('search_products', data_scope=('public_product_information',)),
    'get_product_details': ToolProfile('get_product_details', data_scope=('public_product_information',)),
    'compare_products': ToolProfile('compare_products', data_scope=('public_product_information',)),
    'add_to_cart': ToolProfile('add_to_cart', 'MEDIUM', False, True, False, True, True, ('public_product_information',)),
    'purchase_product': ToolProfile('purchase_product', 'CRITICAL', False, True, True, False, True, ('public_product_information',)),
    'draft_message': ToolProfile('draft_message', 'LOW', False, True, False, True, False, ('public_contact_information',)),
    'send_message': ToolProfile('send_message', 'HIGH', False, True, False, False, True, ('public_contact_information',)),
    'get_application': ToolProfile('get_application', 'MEDIUM', True, False, False, True, False, ('application_data',)),
    'draft_application': ToolProfile('draft_application', 'MEDIUM', False, True, False, True, False, ('application_data',)),
    'submit_application': ToolProfile('submit_application', 'CRITICAL', False, True, False, False, True, ('application_data',)),
    'find_available_slots': ToolProfile('find_available_slots', 'LOW', True, False, False, True, False, ('public_schedule',)),
    'book_appointment': ToolProfile('book_appointment', 'HIGH', False, True, False, True, True, ('public_schedule',)),
}

def ensure_builtin_tools():
    from mirror.models import Tool
    created = []
    for name, p in BUILTIN_TOOLS.items():
        obj, was_created = Tool.objects.get_or_create(
            name=name,
            defaults={
                'title': name.replace('_',' ').title(),
                'description': f'MIRROR demo tool: {name.replace("_", " ")}.',
                'risk_level': p.risk_level,
                'read_only': p.read_only,
                'side_effect': p.side_effect,
                'financial': p.financial,
                'reversible': p.reversible,
                'requires_approval': p.requires_approval,
                'annotations': {'dataScope': list(p.data_scope)},
            },
        )
        if was_created:
            created.append(obj)
    return created

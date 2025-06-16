from django import template
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    """
    Renders a hierarchical menu from the database with active items highlighted.

    This function performs exactly one database query to fetch all items for a
    given menu. It then constructs the tree structure in memory, determines
    the active item based on the current request URL, and identifies all
    parent items that need to be expanded.

    Args:
        context: The template context, used to access the current request.
        menu_name: The unique name of the menu to render.

    Returns:
        A dictionary containing the processed menu data for rendering in the
        'menu/draw_menu.html' template.
    """
    try:
        request_path = context['request'].path
    except KeyError:
        request_path = '/'

    all_items = MenuItem.objects.filter(menu_name=menu_name).order_by('pk')

    item_map = {item.pk: item for item in all_items}
    root_items = []
    active_item = None

    for item in all_items:
        item.resolved_url = item.get_url()
        # Attach an empty list for potential children to avoid errors in the template
        item.child_items = []

        if item.parent_id and item.parent_id in item_map:
            parent = item_map[item.parent_id]
            parent.child_items.append(item)
        else:
            root_items.append(item)

        if request_path.startswith(item.resolved_url):
            if not active_item or len(item.resolved_url) > len(active_item.resolved_url):
                active_item = item

    expanded_item_ids = set()
    if active_item:
        expanded_item_ids.add(active_item.pk)
        parent = item_map.get(active_item.parent_id)
        while parent:
            expanded_item_ids.add(parent.pk)
            parent = item_map.get(parent.parent_id)

    return {
        'menu_items': root_items,
        'expanded_item_ids': expanded_item_ids,
        'active_item_id': active_item.pk if active_item else None,
    }
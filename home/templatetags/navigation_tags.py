from django import template

# import site:
from wagtail.models import Site

# from base.models import FooterText

register = template.Library()


# ... keep the definition of get_footer_text and add the get_site_root template tag:
@register.simple_tag(takes_context=True)
def get_site_root(context):
    nav =Site.find_for_request(context["request"]).root_page
    # print("this is the navvvv --------->>",nav)
    # for menu in nav.get_children().live():
    #     # print('this is menu--------->>>>',menu)
    #     # for submenu in menu.get_children().live():
    #     #     # print("submenu--->",submenu) 


    return Site.find_for_request(context["request"]).root_page
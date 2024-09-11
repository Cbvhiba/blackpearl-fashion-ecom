from django import template
from blackpearl_frntend.views import FILTER_PRICE_RANGE
register = template.Library()

@register.filter
def to_name_list(queryset):
    return [i.Varient_Name.lower() for i in queryset]

@register.filter
def Size(queryset):
    for i in queryset:
        if 'Size' == i.Varient_Name or 'size' == i.Varient_Name or 'SIZE' == i.Varient_Name:
            return i
        
@register.filter
def Color(queryset):
    for i in queryset:
        if 'Color' == i.Varient_Name or 'color' == i.Varient_Name or 'COLOR' == i.Varient_Name:
            return i

@register.filter
def to_id_list(queryset):
    return [i.id for i in queryset]

@register.filter
def get_item(dictionary, key):
    return FILTER_PRICE_RANGE[dictionary].get(key)

@register.filter
def get_P_Item(queryset, list):
    for j in list:
        for i in queryset:
            if i.uid == j:
                list.remove(i.uid)
                return i
            
@register.filter
def nonDuplicate(queryset):
    a =[]
    for i in queryset:
        print(i.uid)
        if i not in a:
            a.append(i)
            print(a)   
    return a
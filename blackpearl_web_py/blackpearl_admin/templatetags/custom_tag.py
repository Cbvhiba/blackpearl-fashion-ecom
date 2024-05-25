from django import template
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
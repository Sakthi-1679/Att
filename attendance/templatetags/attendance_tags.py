from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dict by key in templates."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def attendance_badge(percentage):
    """Return Bootstrap badge class based on attendance percentage."""
    try:
        pct = float(percentage)
        if pct >= 75:
            return 'bg-success'
        elif pct >= 60:
            return 'bg-warning text-dark'
        else:
            return 'bg-danger'
    except (ValueError, TypeError):
        return 'bg-secondary'


@register.filter
def status_badge(status):
    """Return Bootstrap badge class for attendance status."""
    mapping = {
        'present': 'bg-success',
        'absent': 'bg-danger',
        'informed_leave': 'bg-warning text-dark',
    }
    return mapping.get(status, 'bg-secondary')


@register.simple_tag
def attendance_percentage(student, start_date=None, end_date=None):
    return student.attendance_percentage(start_date=start_date, end_date=end_date)

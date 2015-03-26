from core.models import tag_name
from random import randint

# returns popular tags from file ? cache, will be dynamic in future updates
def get_static_data():
    res = []
    append = res.append

    all_tags = tag_name.objects.all()
    demo_pop_tags = [t.name for t in all_tags]

    #demo_pop_tags = ["Technopark", "Baumanka", "C", "Python", "MySQL", "Ruby", "apple", "iOS", "swift", "django", "php", "flask", "objective-c", "Ubuntu-server", "VPS", "Coffee Script", "sudo"]
    demo_labels = ["label label-default", "label label-primary", "label label-success", "label label-info", "label label-warning", "label label-danger"]
    for tag in demo_pop_tags:
        append({"text": tag, "label": demo_labels[randint(0, len(demo_labels)-1)]})

    data = {}
    data["popular_tags"] = res
    data["popular_users"] = ["Vasya Pupkin", "accl_9912_xz", "Dart Vader", "ggl.cm", "qwerTY"]
    return data


# will add the popular tags-processor later here

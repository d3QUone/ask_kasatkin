import json


FILENAME = "best_data.txt"


# this script loads (?) once an hour, asks db for updates and save the results









def save_data(data):
    with open(FILENAME, "w") as f:
        f.write(json.dumps(data))

#demo_labels = ["label label-default", "label label-primary", "label label-success", "label label-info", "label label-warning", "label label-danger"]

selected_tags = ["technopark", "baumanka", "c", "python", "mysql", "ruby", "apple", "iOS", "swift", "django", "sudo", "flask"]

test_data = {
    "popular_tags": [{"text": tag, "label": ""} for tag in selected_tags],
    "popular_users": ["Vasya Pupkin", "accl_9912_xz", "Dart Vader"]
}

save_data(test_data)  # test


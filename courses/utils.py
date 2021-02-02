import os

def file_location(instance, filename):
    main_folder = "File contents"
    loc = os.path.join(main_folder, instance.owner.username, filename)
    return loc

def image_location(instance, filename):
    loc = os.path.join("Image Contents", instance.owner.username, filename)
    return loc

def course_image(instance, filename):
    loc = os.path.join("Course Image", instance.title, filename)
    return loc
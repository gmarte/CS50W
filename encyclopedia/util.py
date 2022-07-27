import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content, accion):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename) and accion == "edit":
        default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        msg = "edited"
    elif default_storage.exists(filename) and accion == "new":
        msg = "Error: encyclopedia entry already exists"
    elif not default_storage.exists(filename) and accion == "new":
        default_storage.save(filename, ContentFile(content))
        msg = "success"
    return msg


def search_entry(query):
    """
    search for an specific encyclopedia entry or close
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if (filename.endswith(".md") and query in re.sub(r"\.md$", "", filename))))


def get_random_entry():
    """
    retrieve a random encyclopedia entry
    """


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        content = f.read().decode("utf-8")
        content = '\n'.join(_.strip() for _ in content.split('\n'))

        # return  f.read().decode("utf-8")
        return content
    except FileNotFoundError:
        return None

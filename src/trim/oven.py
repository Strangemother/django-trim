def cook(func):
    """Given a function, bake the functionality into trims,
    allowing for generic import across the app.

    Pre baked items are cooked immediately.
    """
    print("Cook", func)

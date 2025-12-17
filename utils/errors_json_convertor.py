def simplify_errors(error_response):
    """
    Convert nested 'errors' dict like:
    {
        "errors": {
            "__all__": ["Invalid credentials."]
        }
    }
    into:
    {
        "errors": "Invalid credentials."
    }
    """
    errors = error_response.get("errors", {})
    
    # Collect all messages into a flat list
    messages = []
    if isinstance(errors, dict):
        for field_errors in errors.values():
            if isinstance(field_errors, (list, tuple)):
                messages.extend(str(msg) for msg in field_errors)
            else:
                messages.append(str(field_errors))
    else:
        # If 'errors' is not a dict, just stringify it
        messages.append(str(errors))

    # Join multiple messages if needed
    combined = " ".join(messages).strip()
    return {"errors": combined}



def simplify_form_errors(form):
    """
    Flatten Django form.errors into a single 'errors' string.
    """
    errors = form.errors  # ErrorDict
    messages = []

    for field_errors in errors.values():
        # field_errors is usually an ErrorList (list-like)
        for msg in field_errors:
            messages.append(str(msg))

    combined = " ".join(messages).strip()
    return {"errors": combined}
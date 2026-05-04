def detect_intent(text):

    text = text.lower()

    if "help" in text:

        return "Help Request"

    elif any(word in text for word in [
        "problem",
        "issue",
        "broken",
        "not working"
    ]):

        return "Complaint"

    elif any(word in text for word in [
        "how",
        "what",
        "why",
        "when",
        "where"
    ]):

        return "Question"

    elif any(word in text for word in [
        "good",
        "great",
        "awesome",
        "nice",
        "love"
    ]):

        return "Feedback"

    else:

        return "General"

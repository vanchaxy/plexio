def to_camel(string: str) -> str:
    words = string.split('_')
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

def smart_split(line, sep):
    if line == None:
        return []
    return list(filter(lambda x: x, line.split(sep)))
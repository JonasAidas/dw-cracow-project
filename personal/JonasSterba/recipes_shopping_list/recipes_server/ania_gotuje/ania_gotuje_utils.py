import re


def find_title(string, start=': "', stop="|"):
    result = re.search(string.split(start)[0] + '(.*)' + string.split(stop)[1], string).group(1)
    result = result.replace(start, '').replace(stop, '').strip()
    return result
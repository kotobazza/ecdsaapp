import textwrap

def wrapText(string, size):
    return "\n".join(textwrap.wrap(string, size))

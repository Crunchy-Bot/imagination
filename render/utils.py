from textwrap import wrap


def wrap_and_join(text: str, characters: int, max_lines=2) -> str:
    return "\n".join(wrap(text, max_lines=max_lines, width=characters))


import click
from read_sdoc import extract_requirements_from_file
import jinja2
from typing import List, Tuple
import re

TEMPLATE= """{% raw %}
-doc_begin='Automatically extracted from {{ source }}'

-requirement_coverages+={TEST, tests, {}}

-requirement_coverages+={IMPLEMENT, implements, {}}
{% endraw %}

{% for set_name, requirements in requirement_sets %}
-requirements+={% raw %}{{% endraw %}{{set_name}}, {% raw %}{{% endraw %}
{% for requirement in requirements %}  {{requirement}}{% if not loop.last %},{% endif %}
{% endfor %}{% raw %}}, {{% endraw %}
  IMPLEMENT,
  TEST
{% raw %}}}{% endraw %}
{% endfor %}
"""

def build_config(sdoc: str, requirement_sets: List[Tuple[str, str]]) -> str:
    requirements = extract_requirements_from_file(sdoc)

    rules = [(set_name, re.compile(pattern)) for set_name, pattern in requirement_sets]

    uids = sorted(requirements.keys())
    sets: List[Tuple[str, List[str]]] = []
    for set_name, pattern in rules:
        matched_uids = [uid for uid in uids if pattern.fullmatch(uid)]
        sets.append((set_name, matched_uids))

    template = jinja2.Template(TEMPLATE)
    output = template.render(source=sdoc, requirement_sets=sets)
    return output


@click.command()
@click.argument("sdoc", type=click.Path())
@click.option(
    "--requirement-set", "-r",
    multiple=True,
    type=(str, str),
    help="Requirement set as name and regex pattern (e.g., -r I 'I-.*')")
def main(sdoc: str, requirement_set: List[Tuple[str, str]]) -> None:
    output = build_config(sdoc, requirement_set)
    print(output)


if __name__ == "__main__":
    main()
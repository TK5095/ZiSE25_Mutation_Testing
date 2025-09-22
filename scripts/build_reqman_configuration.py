
import click
from read_sdoc import extract_requirements_from_file
import jinja2
from typing import List, Tuple, Optional
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

def build_config(sdoc: str, requirement_sets: List[Tuple[str, str]], enabled_components: Optional[List[str]] = None) -> str:
    requirements = extract_requirements_from_file(sdoc)

    # Filter requirements by enabled components if specified
    if enabled_components is not None:
        filtered_requirements = {}
        for uid, req in requirements.items():
            # Include requirement if it has no component tag, or if its component is enabled
            if req.component is None or req.component in enabled_components:
                filtered_requirements[uid] = req
        requirements = filtered_requirements

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
@click.option(
    "--enabled-component", "-c",
    multiple=True,
    type=str,
    help="Enabled component (e.g., -c APP_DISPLAY -c APP_BUZZER)")
def main(sdoc: str, requirement_set: List[Tuple[str, str]], enabled_component: List[str]) -> None:
    enabled_components = list(enabled_component) if enabled_component else None
    output = build_config(sdoc, requirement_set, enabled_components)
    print(output)


if __name__ == "__main__":
    main()
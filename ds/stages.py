"""The stages a scheduler can call: which prompt, what input, what limits.

Input models forbid unknown keys, so a typo in the scheduler's JSON fails
before a single token is spent instead of being silently ignored.
"""

from dataclasses import dataclass
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from ds.config import REPO


class _Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NoInput(_Input):
    pass


class MonthInput(_Input):
    mes: str | None = Field(default=None, pattern=r"^\d{4}-(0[1-9]|1[0-2])$")


class TopicInput(_Input):
    tema: str = Field(min_length=3)


@dataclass(frozen=True)
class Stage:
    prompt: str
    input: type[_Input]
    # Ceilings, not estimates. The run stops when it reaches one. With a
    # subscription token the cost is notional but the SDK still enforces it.
    budget_usd: float
    max_turns: int
    needs_website: bool = False


STAGES: dict[str, Stage] = {
    "plan-month": Stage("plan-month", MonthInput, budget_usd=3, max_turns=120),
    "write-blog-post": Stage(
        "write-blog-post", TopicInput, budget_usd=8, max_turns=200, needs_website=True
    ),
    "make-week": Stage("make-week", NoInput, budget_usd=6, max_turns=200),
    "publish-week": Stage("publish-week", NoInput, budget_usd=3, max_turns=120),
    "monthly-report": Stage("monthly-report", MonthInput, budget_usd=3, max_turns=120),
}

ALIASES = {
    "plan": "plan-month",
    "post": "write-blog-post",
    "week": "make-week",
    "publish": "publish-week",
    "report": "monthly-report",
}


def resolve(name: str) -> str | None:
    name = ALIASES.get(name, name)
    return name if name in STAGES else None


def build_prompt(stage: Stage, payload: _Input, website: str, today: date) -> str:
    """The prompt file plus the `## Entrada` block.

    Same shape the old Node runner built, so the prompts read the same.
    """
    lines = [
        (REPO / "prompts" / f"{stage.prompt}.md").read_text(),
        "\n---\n\n## Entrada\n",
        f"- Fecha de hoy: {today.isoformat()}",
        f"- WEBSITE_REPO: {website or '(no configurado)'}",
    ]
    values = payload.model_dump(exclude_none=True)
    if values:
        lines += [f"- {key}: {value}" for key, value in values.items()]
    else:
        lines.append("- Sin argumento: usa el valor por defecto que indique el prompt.")
    return "\n".join(lines)

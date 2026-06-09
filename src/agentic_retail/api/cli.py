"""CLI: ingest a dataset and ask questions of it."""
from __future__ import annotations

from pathlib import Path

import click

from agentic_retail.adapters import REGISTRY
from agentic_retail.agents import Router
from agentic_retail.ingest import ingest as run_ingest, load_canonical
from agentic_retail.tools import registry as tool_registry


@click.group()
def cli() -> None:
    """Agentic retail analysis."""


@cli.command("ingest")
@click.option("--source", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--adapter", required=True, type=click.Choice(sorted(REGISTRY)))
@click.option("--out", required=True, type=click.Path(file_okay=False, path_type=Path))
def ingest_cmd(source: Path, adapter: str, out: Path) -> None:
    ds = run_ingest(source, adapter, out)
    click.echo(f"Ingested {ds.name} ({ds.grain}) → {out}")
    click.echo(f"Available fields: {sorted(ds.available_fields())}")


@cli.command("tools")
@click.option("--data", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
def tools_cmd(data: Path) -> None:
    ds = load_canonical(data)
    fields = ds.available_fields()
    click.echo(f"Dataset fields: {sorted(fields)}")
    for t in tool_registry.all():
        flag = "✓" if t.is_applicable(ds) else "✗"
        click.echo(f"  {flag} [{t.category:12s}] {t.name:20s} {t.description}")


@cli.command("ask")
@click.option("--data", required=True, type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("question")
def ask_cmd(data: Path, question: str) -> None:
    ds = load_canonical(data)
    decision = Router().route(question, ds)
    click.echo(f"[router] {decision.rationale}")
    result = decision.tool.run(ds)
    click.echo(f"[{result.tool}] {result.summary}")


if __name__ == "__main__":
    cli()

import re
from typing import List, Tuple
from github import Github
import os

from github.Issue import Issue
import rich
import click
from rich.prompt import Confirm
from rich.table import Table, box


def generate_table() -> Table:
    table = Table(
        title="Issues to LGTM",
        show_lines=True,
        box=box.ROUNDED,
        expand=False,
    )
    table.add_column("Repository", style="cyan", no_wrap=True)
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("By", style="green")
    table.add_column("Content", style="blue")
    return table


def generate_formatted_str(issue: Issue, commiter: str) -> Tuple[str, str]:
    formatted_packages_str_for_table = ""
    formatted_packages_str_for_ask = "  "
    formatted_packages_str_for_ask_separator = " \n  "

    updated_packages: List[Tuple[str, str]] = []
    formatted_list: List[str] = []
    if commiter == "renovate[bot]":
        updated_packages = re.findall(r"\[(.*?)\].*?-> `(.*)`", issue.body)

    elif commiter == "pre-commit-ci[bot]":
        updated_packages = re.findall(r"\[(.*):.* →(.*)\]", issue.body)

    for pkg in updated_packages:
        formatted_list.append(f"{pkg[0].rsplit('/')[-1]}: {pkg[1]}")

    formatted_packages_str_for_table = "\n".join(formatted_list)
    formatted_packages_str_for_ask += formatted_packages_str_for_ask_separator.join(formatted_list)

    return formatted_packages_str_for_table, formatted_packages_str_for_ask


@click.command()
@click.option(
    "-u",
    "--users",
    help="comma-separated list of users to match",
    default="renovate[bot],pre-commit-ci[bot]",
    show_default=True,
)
@click.option("-y", "--yes", is_flag=True, help="Answer yes to all questions")
@click.option("-t", "--token", help="GitHub token")
@click.option("-d", "--dry-run", is_flag=True, help="Dry run")
def main(users: str, yes: bool, token: str, dry_run: bool) -> None:
    issues_to_lgtm: List[Issue] = []
    users_to_match: List[str] = users.split(",")
    api = Github(login_or_token=token or os.environ["GITHUB_TOKEN"])
    table = generate_table()

    for issue in api.search_issues(f"is:open is:pr involves:{api.get_user().login} archived:false sort:updated-desc"):
        _commiter = issue.user.login
        _repository = issue.repository.full_name
        if _commiter not in users_to_match:
            continue

        formatted_packages_str_for_table, formatted_packages_str_for_ask = generate_formatted_str(
            issue=issue, commiter=_commiter
        )

        if yes:
            lgtm = True
        else:
            lgtm = Confirm.ask(
                f"{_repository}: {issue.title}, by {_commiter}\npackages:\n{formatted_packages_str_for_ask}\nLGTM?",
                choices=["y", "n"],
                default="y",
            )
        if lgtm:
            issues_to_lgtm.append(issue)
            table.add_row(
                _repository,
                issue.title.strip(),
                _commiter,
                formatted_packages_str_for_table,
            )

    if issues_to_lgtm:
        rich.print(table)
        lgtm_all = Confirm.ask(
            "lgtm all issues?",
            choices=["y", "n"],
            default="y",
        )
        if lgtm_all:
            for _issue in issues_to_lgtm:
                rich.print(f"{_issue.repository.full_name}: lgtm {_issue.title} by {_issue.user.login}. {dry_run=}")
                if not dry_run:
                    _issue.create_comment("/lgtm")


if __name__ == "__main__":
    main()

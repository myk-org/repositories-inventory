# Scripts

- release-it-repos
- generate-inventory-markdown
- github-auto-lgtm
- poetry-tools

Run any command with `--help` to see usage

## Requirements

- [poetry](https://python-poetry.org/)
- [pipx](https://github.com/pypa/pipx)

## Installation

##### poetry

```bash
poetry install
```

##### pipx

```bash
git clone https://github.com/myk-org/repositories-inventory.git
cd repositories-inventory
pipx install .
```

### Update

```bash
git remote update
```

##### poetry

```bash
poetry install
```

##### pipx

```bash
pipx install . -f
```

## release-it-repos

Check and release to `Pypi` using [release-it](https://github.com/release-it/release-it) for all repositories under [REPOS_INVENTORY](../REPOS_INVENTORY.md)

### Usage

Set base `git` directory via OS environment or in the config file.

```bash
export GIT_BASE_DIR=<git repositories path>
```

```yaml
git-base-dir: ~/git/
repositories: https://raw.githubusercontent.com/myk-org/repositories-inventory/refs/heads/main/REPOS_INVENTORY.md
repositories:
  https://github.com/user/repository1:
    - main
  https://github.com/user/repository2:
    - main
    - feature

repositories-mapping: # If local repository folder is different from the repository name
  cloud-tools: cloud-tools-upstream

include-repositories: # Check only these repositories
  - cloud-tools
```

### Usage

Run `poetry run release-it-repos` to execute the script
Check `poetry run release-it-repos --help` for more info

import re
import yaml


def to_yaml() -> str:
    repositories = "manifests/old.md"
    with open(repositories) as fd:
        repos = fd.readlines()

    final_repositories = {}
    for line in repos:
        if re.findall(r"\[.*]\(.*\)", line):
            repo_data = [section.strip() for section in line.split("|") if section]
            if len(repo_data) < 4:
                continue

            repo_name = re.findall(r"\[.*]", repo_data[0])[0].strip("[").rstrip("]")
            github_url = re.findall(r"\(.*\)", repo_data[0])[0].strip("(").rstrip(")")
            branches = [br.strip("`") for br in repo_data[3].split()]

            container = ":heavy_check_mark:" in repo_data[1]
            if container:
                container_url = re.findall(r"\(.*\)", repo_data[1])[0].strip("(").rstrip(")")
            else:
                container_url = ""

            release = ":heavy_check_mark:" in repo_data[2]
            if release:
                release_url = re.findall(r"\(.*\)", repo_data[2])[0].strip("(").rstrip(")")
            else:
                release_url = ""

            final_repositories[repo_name] = {
                "github_url": github_url,
                "branches": branches,
                "container": container,
                "container_url": container_url,
                "release": release,
                "release_url": release_url,
            }

    return yaml.dump(final_repositories)


if __name__ == "__main__":
    print(to_yaml())

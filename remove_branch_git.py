import argparse
from git import Repo

def remove_branches(repo: Repo, names: list, remote: bool = False):
    for branch in repo.branches:
        branch_name = branch.name
        for name in names:
            if branch_name.find(name, 0, len(name)) == 0 and repo.active_branch.name != branch_name:
                print('Local branch deleted: ' + branch_name)
                branch.delete(repo, branch_name, force=True)
                if remote:
                    remove_remote_branches(repo, names)


def remove_remote_branches(repo: Repo, names: list):
    origin = repo.remotes.origin
    for remote in origin.refs:
        origin_name = remote.name.removeprefix('origin/')
        for name in names:
            if origin_name.find(name, 0, len(name)) == 0:
                repo.git.push('--delete', 'origin', origin_name)
                print('Deleted remote: ' + origin_name)


parser = argparse.ArgumentParser(description="Git branch delete",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", "--remote", action="store_true", help="Delete from remote also")
parser.add_argument("git", help="Git location")
parser.add_argument("branch_name", help="Branch name")
args = parser.parse_args()
config = vars(args)
repo = Repo(config['git'])
remove_branches(repo, [config['branch_name']], config['remote'])


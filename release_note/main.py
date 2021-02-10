import os
from github import Github
from release_note.repository import Repository


def get_version_and_tag_name():
    "バージョン名とタグ名を作る"
    major = 1
    minor = 0
    patch = 0
    src_dir = os.environ['CODEBUILD_SRC_DIR']
    with open("%s/build.gradle" % src_dir) as f:
        for line in f.readlines():
            if(line.startswith("    ext.major = ")):
                major = int(line.split()[-1])
            if(line.startswith("    ext.minor = ")):
                minor = int(line.split()[-1])
            if(line.startswith("    ext.patch = ")):
                patch = int(line.split()[-1])
    version_name = "%d.%d.%d" % (major, minor, patch)
    tag_name = "release_%d_%d_%d" % (major, minor, patch)
    return version_name, tag_name


def main():
    # バージョン名とタグ名を作る
    version_name, tag_name = get_version_and_tag_name()
    # アクセストークンを持ってGithubオブジェクトを作成
    access_token = os.environ['GITHUB_API_ACCESS_TOKEN']
    repository_name = os.environ['GITHUB_REPOSITORY']
    organization = os.environ.get('GITHUB_ORGANIZATION')
    g = Github(access_token)
    # リポジトリを取得
    if organization is not None:
        # Organizationを使っている場合
        gr = g.get_organization(
            organization).get_repo(repository_name)
    else:
        gr = g.get_user().get_repo(repository_name)
    # インスタンスにする
    r = Repository(gr)
    # masterブランチにマージ済みプルリク一覧テキストを作成する
    text = r.make_marged_prs()
    # デバッグ表示する
    print("%s %s" % (version_name, tag_name))
    print("")
    print(text)
    # git releaseを作成する
    # r.create_release(tag_name, version_name, text)

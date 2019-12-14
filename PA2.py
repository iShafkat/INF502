######################################################################################################################
# Team members: Anuraag Srivastava(as4378)                                                                           #
#               Vinod Kumar Gummadi(vg289)                                                                           #
#               Shafkat Islam(si229)                                                                                 #
######################################################################################################################




import json
import requests
from bs4 import BeautifulSoup
from datetime import date
from dateutil import parser
import csv
import pathlib
import pandas as pd
import time
import os
import matplotlib.pyplot as plt

username = 'as4378'
token = 'cc3ab432f5da0f6c84798b9f010fe319cfeae276'
gh_session = requests.Session()
gh_session.auth = (username, token)

login_list = []
users_list = []
pull_requests_list = []


class User:
    def __init__(self, login, repositories, projects, followers, following, contributions):
        self.login = login
        self.repositories = repositories
        self.projects = projects
        self.followers = followers
        self.following = following
        self.contributions = contributions
        self.pull_requests = None
        self.has_a_twitter = False if gh_session.get("https://twitter.com/" + str(login)).status_code != 200 else True

    def to_CSV(self):
        return [self.login, self.repositories, self.projects, self.followers, self.following,
                self.contributions, len(self.pull_requests), self.has_a_twitter]

    def get_header(self):
        return ["login", "repositories", "projects", "followers", "following", "contributions",
                "pull_requests", "has_a_twitter"]

    def as_dict(self):
        return {'login': self.login, 'followers': self.followers, 'following': self.following,
                'contributions': self.contributions, 'pull_requests': len(self.pull_requests),
                'repositories': self.repositories}


class Repository:
    def __init__(self, name, owner, description, homepage, license, forks, watchers):
        self.date_of_collection = str(date.today())
        self.name = name
        self.owner = owner
        self.description = description
        self.homepage = homepage
        self.license = license
        self.forks = forks
        self.watchers = watchers
        self.pull_requests = []

    def to_CSV(self):
        return [self.date_of_collection, self.name, self.owner, self.description,
                self.homepage, self.license, self.forks, self.watchers]

    def get_header(self):
        return ["date_of_collection", "name", "owner", "description", "homepage", "license", "forks", "watchers"]

    def print_info(self):
        print(str(self.owner) + "/" + str(self.name) + ": " + str(self.description) + "(" + str(self.watchers) + ")")


class PullRequest:
    def __init__(self, repo_name, title, number, body, state, date_of_creation, closing_date, user,
                 commits, additions, deletions, changed_files):
        self.repo_name = repo_name
        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.date_of_creation = date_of_creation
        self.closing_date = closing_date
        self.user = user
        self.commits = commits
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files

    def to_CSV(self):
        return [self.title, self.number, self.state, self.date_of_creation, self.closing_date, self.user,
                self.commits, self.additions, self.deletions, self.changed_files]

    def get_header(self):
        return ["title", "number", "state", "date_of_creation", "closing_date", "user", "commits", "additions",
                "deletions", "changed_files"]

    def print_info(self):
        print(str(self.number) + ": " + str(self.title))

    def as_dict(self):
        return {'state': self.state, 'commits': self.commits, 'additions': self.additions,
                'deletions': self.deletions, 'changed_files': self.changed_files, 'user': self.user,
                'date_of_creation': self.date_of_creation, 'repo_name': self.repo_name}


def get_repo_info(repo_name):
    json_response_repos = gh_session.get("https://api.github.com/repos/" + str(repo_name))
    return json_response_repos


repos_list = []
pull_requests_list = []


def get_pull_requests(owner, name):
    url = "https://api.github.com/search/issues?q=is:pr+repo:"
    current_url = url + str(owner) + "/" + str(name)
    json_response_pulls = gh_session.get(current_url)
    return json_response_pulls


def get_pull_request_details(owner, name, number):
    url = "https://api.github.com/repos/" + str(owner) + "/" + str(name) + "/pulls/" + str(number)
    json_response_pull = gh_session.get(url)
    return json_response_pull


def save_users_csv():
    try:
        for u in users_list:
            to_CSV("users.csv", u)

        print("Data saved successfully.\n")
        return True
    except Exception as e:
        print("There was an issue in saving to users.csv.\n")
        print(e)
        return False


def save_projects_csv():
    try:
        for r in repos_list:
            to_CSV("projects.csv", r)

        print("Data saved successfully.\n")
        return True
    except Exception as e:
        print("There was an issue in saving to projects.csv.")
        print(e)
        return False


def save_pull_requests_csv():
    try:
        # create a projects folder if not already exists
        if not os.path.exists("projects"):
            os.mkdir("projects")

        # loop through all pull requests objects
        for p in pull_requests_list:
            file = "projects/" + str(p.user) + "-" + str(p.repo_name) + ".csv"
            to_CSV(file, p)

        print("Data saved successfully.\n")
        return True
    except Exception as e:
        print("There was an issue in saving to owner-project.csv.")
        print(e)
        return False


def to_CSV(file, row):
    if pathlib.Path(file).exists():
        with open(file, 'a', newline='') as fd:
            csvwriter = csv.writer(fd)
            csvwriter.writerow(row.to_CSV())
    else:
        with open(file, 'w', newline='') as fd:
            csvwriter = csv.writer(fd)
            csvwriter.writerow(row.get_header())
            csvwriter.writerow(row.to_CSV())


def collect_user_requested_repo(owner, repository):
    try:
        # get repository info and add to repositories list

        # get the data for repository using api call
        r = get_repo_info(str(owner) + "/" + str(repository)).json()

        name = str(r["name"])
        description = str(r["description"])
        owner = str(r["owner"]["login"])
        homepage = str(r["homepage"])
        license = str(r["license"])
        forks = str(r["forks"])
        watchers = str(r["watchers"])

        # storing the repository information in Repository class object
        current_repo = Repository(name, owner, description, homepage, license, forks, watchers)
        repos_list.append(current_repo)  # adding this object to global repository list

        # get pull requests for the above repository using api call
        current_pull_requests = []
        current_pull_request = get_pull_requests(str(current_repo.owner), str(current_repo.name)).json()

        # dropping into the "items" level from the json response
        current_pull_items = current_pull_request["items"]

        for i in current_pull_items:
            title = str(i["title"])
            number = str(i["number"])
            body = str(i["body"])
            state = str(i["state"])
            date_of_creation = str(i["created_at"])
            closing_date = str(i["closed_at"]) if state != "open" else None
            user = str(i["user"]["login"])

            # get the additional details by making an api call using pull request number
            pull_details = get_pull_request_details(current_repo.owner, current_repo.name, number).json()
            commits = str(pull_details["commits"])
            additions = str(pull_details["additions"])
            deletions = str(pull_details["deletions"])
            changed_files = str(pull_details["changed_files"])

            # storing the pull request information in PullRequest class object
            current_pull_request = PullRequest(current_repo.name, title, number, body, state, date_of_creation,
                                               closing_date, user,
                                               commits, additions, deletions, changed_files)
            pull_requests_list.append(current_pull_request)  # add this object to global pull requests list

            # also add this to local list which will help in getting users info for this pull request
            current_pull_requests.append(current_pull_request)

            # adding reference to this pull request object to current repository pull-requests list
            current_repo.pull_requests.append(current_pull_request)

        # get users information using web scraping
        url = "https://github.com/"
        repo_class = "Counter hide-lg hide-md hide-sm"
        for p in current_pull_requests:
            current_url = url + p.user
            website_url = gh_session.get(current_url).text
            soup = BeautifulSoup(website_url, 'lxml')
            list_soup = soup.findAll("span", {"class": repo_class})
            repo = list_soup[0].text.strip()
            project = list_soup[1].text.strip()
            stars = list_soup[2].text.strip()
            followers = list_soup[3].text.strip()
            following = list_soup[4].text.strip()

            contributions = soup.findAll("h2", {"class": "f4 text-normal mb-2"})
            contributions = str(contributions[0].text.strip().split()[0])

            # create a User class object to store information for the current user
            current_user = User(p.user, repo, project, followers, following, contributions)

            # add this to object to global users list
            users_list.append(current_user)

            # adding reference to all the pull-requests created by this user
            pull_requests = [p for p in pull_requests_list if p.user == current_user.login]
            current_user.pull_requests = pull_requests

        print("Data collected successfully.\n")
        return True  # success

    except Exception as e:
        print("There was an issue in collecting data.\n")
        print(e)
        return False  # failure


def get_all_repos():
    i = 1
    for r in repos_list:
        r.print_info()


def get_pull_requests_for_repo(repo_index):
    repo = repos_list[repo_index]
    print("\n")
    for p in repo.pull_requests:
        p.print_info()


def get_repo_summary(repo_index):
    repo = repos_list[repo_index]
    open_pull_requests = len([p for p in repo.pull_requests if p.state == "open"])
    closed_pull_requests = len([p for p in repo.pull_requests if p.state == "closed"])
    users = len(set([p.user for p in repo.pull_requests]))
    oldest_pull_request = min([parser.parse(p.date_of_creation) for p in repo.pull_requests])
    temp_users = list(set([p.user for p in repo.pull_requests]))
    users_twitter = 0

    for t in temp_users:
        user = [u for u in users_list if u.login == t]
        if user is not None and len(user) > 0:
            user = user[0]
            if user.has_a_twitter:
                users_twitter += 1

    print("\nFollowing is the summary for " + str(repo.name) + " repository: \n")
    print("No. of pull requests in open state: " + str(open_pull_requests))
    print("No. of pull requests in closed state: " + str(closed_pull_requests))
    print("No. of users: " + str(users))
    print("Oldest pull request: " + str(oldest_pull_request.strftime('%m/%d/%Y')))
    print("Users with valid twitter account: " + str(users_twitter))
    print("\n")


def print_graphics(repo_index):
    repo = repos_list[repo_index]
    pull_requests = [p for p in repo.pull_requests]
    df = pd.DataFrame([p.as_dict() for p in pull_requests])

    df["commits"] = pd.to_numeric(df["commits"])
    df["additions"] = pd.to_numeric(df["additions"])
    df["deletions"] = pd.to_numeric(df["deletions"])
    df["changed_files"] = pd.to_numeric(df["changed_files"])

    state_closed = df[df.state == "closed"]
    state_open = df[df.state == "open"]
    data_to_plot = [state_open['commits'], state_closed['commits']]
    plt.boxplot(data_to_plot, patch_artist=True)
    plt.title("open and closed pull requests per commits")
    plt.show()

    data_to_plot = [state_open['additions'], state_closed['additions']]
    plt.boxplot(data_to_plot, patch_artist=True)
    plt.title("open and closed pull requests per additions")
    plt.show()

    data_to_plot = [state_open['deletions'], state_closed['deletions']]
    plt.boxplot(data_to_plot, patch_artist=True)
    plt.title("open and closed pull requests per deletions")
    plt.show()

    df1 = df[['user', 'changed_files']]
    df1 = df1.groupby('user')['changed_files'].apply(list)
    df1 = df1.reset_index()
    data_to_plot = [d for d in df1['changed_files']]
    plt.boxplot(data_to_plot, patch_artist=True)
    plt.title("# of changed_files grouped by user")
    plt.show()

    plt.scatter(df['additions'], df['deletions'])
    plt.xlabel('additions')
    plt.ylabel('deletions')
    plt.title('additions vs deletions')
    plt.show()

    plt.hist(df['commits'])
    plt.ylabel('# of commits')
    plt.title('# of commits per pull request')
    plt.show()


def print_graphics_all():
    df = pd.DataFrame([p.as_dict() for p in pull_requests_list])

    df['date_of_creation'] = [parser.parse(x).date() for x in df['date_of_creation']]
    df['commits'] = pd.to_numeric(df['commits'])

    df['counts'] = df['commits']
    df1 = df[['date_of_creation', 'counts']]
    df1 = df1.groupby('date_of_creation').count()
    df1 = df1.reset_index()
    plt.plot(df1['date_of_creation'], df1['counts'])
    plt.title("number of pull requests per day")
    plt.xlabel("day")
    plt.ylabel("# of pull-requests")
    plt.show()

    df_open = df[df['state'] == 'open']
    df_open = df_open[['date_of_creation', 'counts']]
    df_open = df_open.groupby('date_of_creation').count()
    df_open = df_open.reset_index()
    plt.plot(df_open['date_of_creation'], df_open['counts'], label='open')

    df_closed = df[df['state'] == 'closed']
    df_closed = df_closed[['date_of_creation', 'counts']]
    df_closed = df_closed.groupby('date_of_creation').count()
    df_closed = df_closed.reset_index()
    plt.plot(df_closed['date_of_creation'], df_closed['counts'], label='closed')

    plt.legend()
    plt.xlabel("day")
    plt.ylabel("# of pull-requests")
    plt.title("open and closed pull-requests per day")
    plt.show()

    df_users_repo = pd.DataFrame(columns=['repo', 'users'])

    i = 0
    for r in repos_list:
        users = len(set([p.user for p in r.pull_requests]))
        df_users_repo.loc[i] = [r.name, users]
        i += 1

    plt.bar(df_users_repo['repo'], df_users_repo['users'])
    plt.xlabel("repository")
    plt.ylabel("# of users")
    plt.title("# of users per repository")
    plt.show()

    plt.hist(df['commits'])
    plt.xlabel("pull-request")
    plt.ylabel('# of commits')
    plt.title('# of commits per pull request')
    plt.show()


def list_all_repos():
    i = 1
    print("The repositories available are:\n")
    for r in repos_list:
        print(str(i) + ". " + str(r.name) + "\n")
        i += 1


def list_all_pull_requests(repo_index):
    repo = repos_list[repo_index]
    print("The pull requests are:\n")
    for p in repo.pull_requests:
        print(p.number + str(". ") + p.title)


def get_corr_users():
    df = pd.DataFrame([u.as_dict() for u in users_list])

    df['followers'] = [x.replace(",", "").replace(" ", "") for x in df['followers']]
    df['followers'] = [float(x[:-1]) * 1000 if x[-1] == 'k' else float(x) for x in df['followers']]

    df['following'] = [x.replace(",", "").replace(" ", "") for x in df['following']]
    df['following'] = [float(x[:-1]) * 1000 if x[-1] == 'k' else float(x) for x in df['following']]

    df['contributions'] = [x.replace(",", "").replace(" ", "") for x in df['contributions']]
    df['contributions'] = [float(x[:-1]) * 1000 if x[-1] == 'k' else float(x) for x in df['contributions']]

    df['repositories'] = [x.replace(",", "").replace(" ", "") for x in df['repositories']]
    df['repositories'] = [float(x[:-1]) * 1000 if x[-1] == 'k' else float(x) for x in df['repositories']]

    df['pull_requests'] = pd.to_numeric(df['pull_requests'])
    print(df.corr())
    print("\n")


def get_corr_pull_requests(repo_index):
    repo = repos_list[repo_index]
    df = pd.DataFrame([p.as_dict() for p in repo.pull_requests])
    df = df[['commits', 'additions', 'deletions', 'changed_files']]
    df['commits'] = pd.to_numeric(df['commits'])
    df['additions'] = pd.to_numeric(df['additions'])
    df['deletions'] = pd.to_numeric(df['deletions'])
    df['changed_files'] = pd.to_numeric(df['changed_files'])
    print(df.corr())
    print("\n")


if __name__ == "__main__":
    select = 0  # variable for user selection

    print("\n\t*********************************************")
    print("\t******* Welcome to the GitHub API App *******")
    print("\t*********************************************")

    try:
        while select != 10:
            print("\n\nWhat would you like to do?")
            print("Choose from one of the following options: ")
            print("\t[1] Collect data for a specific repository from GitHub.")
            print("\t[2] List all the collected repositories.")
            print("\t[3] List all pull requests from an existing repository.")
            print("\t[4] List the summary of a repository.")
            print("\t[5] Create graphics for a given repository.")
            print("\t[6] Create graphics for all the collected repositories.")
            print("\t[7] Calculate the correlation between the data collected for users.")
            print("\t[8] Calculate the correlation between all the numeric data in the pull requests for a repository.")
            print("\t[9] Save to CSV.")
            print("\t[10] Exit the Program")

            select = int(input("Please provide the number corresponding to the option: "))
            if select == 1:
                owner = input("Enter the github owner name: ")
                repo = input("Enter the repository name: ")
                collect_user_requested_repo(owner, repo)
            elif select == 2:
                list_all_repos()
            elif select == 3:
                list_all_repos()
                print("Please select a Repository from the list")
                index = int(input("Enter the number corresponding to the Repository of interest: "))
                list_all_pull_requests(index - 1)
            elif select == 4:
                list_all_repos()
                print("Please select a Repository from the list")
                index = int(input("Enter the number corresponding to the Repository of interest: "))
                get_repo_summary(index - 1)
            elif select == 5:
                list_all_repos()
                print("Please select a Repository from the list")
                index = int(input("Enter the number corresponding to the Repository of interest: "))
                print_graphics(index - 1)
            elif select == 6:
                print_graphics_all()
            elif select == 7:
                get_corr_users()
            elif select == 8:
                list_all_repos()
                print("Please select a Repository from the list")
                index = int(input("Enter the number corresponding to the Repository of interest: "))
                get_corr_pull_requests(index - 1)
            elif select == 9:
                print("\t[1] Save users data to users.csv.")
                print("\t[2] Save projects data to projects.csv.")
                print("\t[3] Save pull requests data to projects/owner-project.csv.\n")
                temp = int(input("Enter the number corresponding to the Action of interest: "))
                if temp == 1:
                    save_users_csv()
                elif temp == 2:
                    save_projects_csv()
                elif temp == 3:
                    save_pull_requests_csv()
                else:
                    print("invalid selection\n")

            elif select == 10:
                break
            else:
                print("invalid selection\n")

            i = 0
            while i != 1:
                i = int(input("\npress 1 to continue\n"))

    except Exception as e:
        print(e)

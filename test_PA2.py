######################################################################################################################
# Team members: Anuraag Srivastava(as4378)                                                                           #
#               Vinod Kumar Gummadi(vg289)                                                                           #
#               Shafkat Islam(si229)                                                                                 #
######################################################################################################################



import unittest
from PA2 import *


# use command "python -m unittest -b" on command line to run unit tests and suppress print messages from code

# Some of the tests might fail if the user info or pull requests etc. gets updated on github  before testing.

class TestGitHub(unittest.TestCase):

    def test_data_collection(self):
        # collect data for a valid user and repository
        res1 = collect_user_requested_repo("mojombo", "chronic")
        # collect data for invalid user and repository
        res2 = collect_user_requested_repo("random_user", "random_repo123123123")

        self.assertTrue(res1)
        self.assertFalse(res2)

    def test_forks_watchers_repo(self):
        repo = repos_list[0]  # pick the chronic repository
        self.assertEqual(repo.forks, "437")
        self.assertEqual(repo.watchers, "3001")

    def test_has_a_twitter(self):
        collect_user_requested_repo("as4378", "opart")
        user = [u for u in users_list if u.login == "as4378"]
        self.assertTrue(user[0].has_a_twitter)

    def test_pull_requests(self):
        repo = repos_list[0]  # pick the chronic repository
        self.assertEqual(len(repo.pull_requests), 30)

    def test_user_data(self):
        user = [u for u in users_list if u.login == "stanhu"][0]
        self.assertEqual(user.followers, "52")
        self.assertEqual(user.following, "0")
        self.assertEqual(user.contributions, "1,003")

    def test_save_to_csv(self):
        self.assertTrue(save_users_csv())
        self.assertTrue(save_projects_csv())
        self.assertTrue(save_pull_requests_csv())



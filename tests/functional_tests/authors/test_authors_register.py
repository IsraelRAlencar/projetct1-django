from tests.functional_tests.authors.base import AuthorsBaseTest


class AuthorsReqisterTest(AuthorsBaseTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url + '/authors/register')
        
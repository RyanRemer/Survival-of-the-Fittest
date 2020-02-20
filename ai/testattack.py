import unittest as ut
from attack import Attack


class TestAttack(ut.TestCase):

    def setUp(self):
        self.attack_obj = Attack()
    # ## END SETUP() ## #

    def tearDown(self):
        pass
    # ## END TEARDOWN() ## #

    def test_poke(self):
        self.assertTrue(self.attack_obj.poke())
    # ## END TEST_POKE() ## #


if __name__ == "__main__":
    ut.main()

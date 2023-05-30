import unittest
from unittest.mock import MagicMock, Mock
from moodclient.mudshell import MUDShell
from moodclient.monster_options import UndefinedParameterException

class TestClientMVP(unittest.TestCase):

    def setUp(self):
        self.network_adapter = MagicMock()
        self.res = []
        self.network_adapter.SendInfoToServer = Mock(
            return_value='aaa', side_effect=lambda x: self.res.append(x))
        self.network_adapter.GetInfoFromServer = Mock(
            return_value='bbb')
        self.network_adapter.SendInfoToServerWithoutResponse = Mock(
            side_effect=lambda x: self.res.append(x))
        self.shell = MUDShell()
        self.shell.SetNetworkAdapter(self.network_adapter)

    def testMoveUp(self):
        self.shell.do_up('')
        assert self.res[-1] == 'move 0 -1'

    def testMoveRight(self):
        self.shell.do_right('')
        assert self.res[-1] == 'move 1 0'

    def testAddMonster1(self):
        self.shell.do_addmon('default hp 100 coords 1 4 hello aaa')
        assert self.res[-1] == 'addmon default aaa 1 4 100'

    def testAddMonster2(self):
        self.shell.do_addmon('cheese coords 1 4 hp 10 hello bbb')
        assert self.res[-1] == 'addmon cheese bbb 1 4 10'

    def testWrongMonsterCreation(self):
        self.shell.do_addmon('cheese coords 1 4 hello bbb')
        assert len(self.res) == 0

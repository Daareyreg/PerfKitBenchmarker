"""Tests for messaging_service.py.

This is the common interface used by the benchmark VM to run the benchmark.
"""

import unittest
from unittest import mock

from perfkitbenchmarker import messaging_service
from perfkitbenchmarker import virtual_machine
from tests import pkb_common_test_case

MESSAGING_SERVICE_DATA_DIR = 'messaging_service_scripts'


class DummyMessagingService(messaging_service.BaseMessagingService):

  CLOUD = 'dummy'

  def _InstallCloudClients(self):
    pass

  def Run(self, *args, **kwargs):
    pass

  def _Create(self, *args, **kwargs):
    pass

  def _Delete(self, *args, **kwargs):
    pass


class MessagingServiceTest(pkb_common_test_case.PkbCommonTestCase):

  def setUp(self):
    super().setUp()
    self.client = mock.create_autospec(
        virtual_machine.BaseVirtualMachine, instance=True)
    self.messaging_service = DummyMessagingService()
    self.messaging_service.client_vm = self.client

  @mock.patch.object(DummyMessagingService, '_InstallCloudClients')
  @mock.patch.object(DummyMessagingService, '_InstallCommonClientPackages')
  def testPrepareClientVm(self, install_cloud_clients_mock,
                          install_common_client_packages_mock):
    self.messaging_service.PrepareClientVm()
    install_cloud_clients_mock.assert_called_once_with()
    install_common_client_packages_mock.assert_called_once_with()

  def testPrepareBasicVmClient(self):
    self.messaging_service._InstallCommonClientPackages()

    self.client.assert_has_calls([
        mock.call.RemoteCommand('sudo pip3 install absl-py numpy'),
        mock.call.RemoteCommand(
            'mkdir -p ~/perfkitbenchmarker/scripts/messaging_service_scripts'),
        mock.call.RemoteCommand(
            "find ~/perfkitbenchmarker -type d -exec touch '{}/__init__.py' \\;"
        ),
        mock.call.RemoteCommand(
            'mkdir -p ~/perfkitbenchmarker/scripts/messaging_service_scripts'
        ),
        mock.call.PushDataFile(
            'messaging_service_scripts/messaging_service_client.py',
            '~/perfkitbenchmarker/scripts/messaging_service_scripts/messaging_service_client.py'
        )
    ])


if __name__ == '__main__':
  unittest.main()

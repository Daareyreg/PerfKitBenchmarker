# Copyright 2018 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for perfkitbenchmarker.providers.aws.aws_disk."""

import unittest
from absl import flags
from perfkitbenchmarker import errors
from perfkitbenchmarker.providers.aws import aws_disk
from tests import pkb_common_test_case

FLAGS = flags.FLAGS
_COMPONENT = 'test_component'


class AwsDiskSpecTestCase(pkb_common_test_case.PkbCommonTestCase):

  def testDefaults(self):
    spec = aws_disk.AwsDiskSpec(_COMPONENT)
    self.assertIsNone(spec.device_path)
    self.assertIsNone(spec.disk_number)
    self.assertIsNone(spec.disk_size)
    self.assertIsNone(spec.disk_type)
    self.assertIsNone(spec.provisioned_iops)
    self.assertIsNone(spec.throughput)
    self.assertIsNone(spec.mount_point)
    self.assertEqual(spec.num_striped_disks, 1)

  def testProvidedValid(self):
    spec = aws_disk.AwsDiskSpec(
        _COMPONENT,
        device_path='test_device_path',
        disk_number=1,
        disk_size=75,
        disk_type='test_disk_type',
        provisioned_iops=1000,
        throughput=100,
        mount_point='/mountpoint',
        num_striped_disks=2,
    )
    self.assertEqual(spec.device_path, 'test_device_path')
    self.assertEqual(spec.disk_number, 1)
    self.assertEqual(spec.disk_size, 75)
    self.assertEqual(spec.disk_type, 'test_disk_type')
    self.assertEqual(spec.provisioned_iops, 1000)
    self.assertEqual(spec.throughput, 100)
    self.assertEqual(spec.mount_point, '/mountpoint')
    self.assertEqual(spec.num_striped_disks, 2)

  def testProvidedNone(self):
    spec = aws_disk.AwsDiskSpec(
        _COMPONENT, provisioned_iops=None, throughput=None
    )
    self.assertIsNone(spec.provisioned_iops)
    self.assertIsNone(spec.throughput)

  def testInvalidOptionTypes(self):
    with self.assertRaises(errors.Config.InvalidValue):
      aws_disk.AwsDiskSpec(_COMPONENT, provisioned_iops='ten')

  def testNonPresentFlagsDoNotOverrideConfigs(self):
    FLAGS.provisioned_iops = 2000
    FLAGS.provisioned_throughput = 200
    FLAGS.data_disk_size = 100
    spec = aws_disk.AwsDiskSpec(
        _COMPONENT, FLAGS, disk_size=75, provisioned_iops=1000, throughput=150
    )
    self.assertEqual(spec.disk_size, 75)
    self.assertEqual(spec.provisioned_iops, 1000)
    self.assertEqual(spec.throughput, 150)

  def testPresentFlagsOverrideConfigs(self):
    FLAGS['provisioned_iops'].parse(2000)
    FLAGS['provisioned_throughput'].parse(200)
    FLAGS['data_disk_size'].parse(100)
    spec = aws_disk.AwsDiskSpec(
        _COMPONENT, FLAGS, disk_size=75, provisioned_iops=1000, throughput=150
    )
    self.assertEqual(spec.disk_size, 100)
    self.assertEqual(spec.provisioned_iops, 2000)
    self.assertEqual(spec.throughput, 200)


if __name__ == '__main__':
  unittest.main()

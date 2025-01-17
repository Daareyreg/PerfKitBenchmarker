"""Module containing Nvidia HPL installation and cleanup functions.

https://catalog.ngc.nvidia.com/orgs/nvidia/containers/hpc-benchmarks
"""


def Install(vm):
  vm.Install('build_tools')
  vm.Install('docker')
  vm.Install('nvidia_driver')
  vm.Install('slurm')
  vm.Install('cuda_toolkit')

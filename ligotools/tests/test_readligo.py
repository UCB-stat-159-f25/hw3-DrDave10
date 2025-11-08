import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
from unittest.mock import MagicMock, patch
from ligotools import readligo as rl

MOCK_STRAIN = np.arange(10)
MOCK_CHANNEL = 'H1'
MOCK_META = {'UTCstart': 1234567890}

@patch('h5py.File')
def test_loaddata_returns_arrays(mock_h5file):
    # Setup mock so required keys always exist
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    strain_group = MagicMock()
    strain_group.__getitem__.side_effect = lambda x: MOCK_STRAIN if x == 'Strain' else None
    meta_group = MagicMock()
    meta_group.__getitem__.side_effect = lambda x: MOCK_META[x]
    mock_file.__getitem__.side_effect = lambda k: {
        'strain': strain_group,
        'meta': meta_group
    }.get(k, MagicMock())
    mock_h5file.return_value = mock_file

    strain, time, dq = rl.loaddata('fakefile.hdf5', 'H1')
    assert strain is not None
    assert isinstance(strain, np.ndarray)
    assert time is not None
    assert isinstance(time, np.ndarray)

@patch('h5py.File')
def test_loaddata_strain_not_zeros(mock_h5file):
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    strain_group = MagicMock()
    strain_group.__getitem__.side_effect = lambda x: MOCK_STRAIN if x == 'Strain' else None
    meta_group = MagicMock()
    meta_group.__getitem__.side_effect = lambda x: MOCK_META[x]
    mock_file.__getitem__.side_effect = lambda k: {'strain': strain_group, 'meta': meta_group}[k]
    mock_h5file.return_value = mock_file

    strain, time, dq = rl.loaddata('anyfile.hdf5', MOCK_CHANNEL)
    assert np.any(strain != 0)
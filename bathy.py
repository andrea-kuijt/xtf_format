import pyxtf
import os, glob
import numpy as np
import matplotlib.pyplot as plt

# The bathymetry and sonar headers are implemented, however - which can be read while ignoring the unimplemented packets
test_path = '/Users/Andrea/PycharmProjects/DEEP/pyxtf-master/xtf/0008 _NHI_L03_20190419 - 0002.xtf'
(fh, p) = pyxtf.xtf_read(test_path)
n_channels = fh.channel_count(verbose=True)
actual_chan_info = [fh.ChanInfo[i] for i in range(0, n_channels)]

f'Number of data channels: {n_channels}\n'
print('Number of data channels: {}\n'.format(n_channels))
print(actual_chan_info[0])
print([key for key in p])
bathy_ch = p[pyxtf.XTFHeaderType.bathy_xyza]  # type: List[pyxtf.XTFPingHeader]
bathy_ch_ping1 = bathy_ch[0]
print(bathy_ch_ping1)

os.chdir("/Users/Andrea/PycharmProjects/DEEP/pyxtf-master/xtf")

for file in glob.glob("*.xtf"):
    print(os.path.basename(file))
    (fh, p) = pyxtf.xtf_read(file)
    n_channels = fh.channel_count(verbose=True)
    actual_chan_info = [fh.ChanInfo[i] for i in range(0, n_channels)]
    f'Number of data channels: {n_channels}\n'
    print('Number of data channels: {}\n'.format(n_channels))
    print(actual_chan_info[0])
    print([key for key in p])
    bathy_ch = p[pyxtf.XTFHeaderType.bathy_xyza]  # type: List[pyxtf.XTFPingHeader]
    bathy_ch_ping1 = bathy_ch[0]
    print(bathy_ch_ping1)

bathy_subchan0 = bathy_ch_ping1.data[0]  # type: np.ndarray
bathy_subchan1 = bathy_ch_ping1.data[1]  # type: np.ndarray

print(bathy_subchan0.shape)
print(bathy_subchan1.shape)

fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
ax1.semilogy(np.arange(0, bathy_subchan0.shape[0]), bathy_subchan0)
ax2.semilogy(np.arange(0, bathy_subchan1.shape[0]), bathy_subchan1)
plt.show()

bathy_ping1_ch_header0 = bathy_ch_ping1.ping_chan_headers[0]

print(bathy_ping1_ch_header0)
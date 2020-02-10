import pyxtf
import os, glob
import numpy as np
import matplotlib.pyplot as plt

# The bathymetry and sonar headers are implemented, however - which can be read while ignoring the unimplemented packets
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
    sonar_ch = p[pyxtf.XTFHeaderType.sonar]  # type: List[pyxtf.XTFPingHeader]
    sonar_ch_ping1 = sonar_ch[1]
    print(sonar_ch_ping1)

# The data and header for each subchannel is contained in the data and ping_chan_headers respectively.
# The data is a list of numpy arrays (one for each subchannel)
sonar_subchan0 = sonar_ch_ping1.data[0]  # type: np.ndarray
sonar_subchan1 = sonar_ch_ping1.data[1]  # type: np.ndarray

print(sonar_subchan0.shape)
#print(sonar_subchan1.shape)
#
# fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12,8))
# ax1.semilogy(np.arange(0, sonar_subchan0.shape[0]), sonar_subchan0)
# ax2.semilogy(np.arange(0, sonar_subchan1.shape[0]), sonar_subchan1)
# plt.show()

# Each subchannel has a XTFPingChanHeader,
# which contains information that can change from ping to ping in each of the subchannels
sonar_ping1_ch_header0 = sonar_ch_ping1.ping_chan_headers[3]

print(sonar_ping1_ch_header0)

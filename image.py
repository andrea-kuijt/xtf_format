import numpy as np
import matplotlib.pyplot as plt
from pyxtf import xtf_read, concatenate_channel, XTFHeaderType
import sys

np.set_printoptions(threshold=sys.maxsize)

# Read file header and packets
test_path = '/Users/Andrea/PycharmProjects/DEEP/pyxtf-master/xtf/0009 _NHI_L04_20190419 - 0001.xtf'
(fh, p) = xtf_read(test_path)

# Show what is in channels
n_channels = fh.channel_count(verbose=True)
actual_chan_info = [fh.ChanInfo[i] for i in range(0, n_channels)]
f'Number of data channels: {n_channels}\n'
print('Number of data channels: {}\n'.format(n_channels))
print('The following (supported) packets are present (XTFHeaderType:count): \n\t' +
      str([key.name + ':{}'.format(len(v)) for key, v in p.items()]))


# Get multibeam/bathy data (xyza) if present
if XTFHeaderType.bathy_xyza in p:
    np_mb = [[y.fDepth for y in x.data] for x in p[XTFHeaderType.bathy_xyza]]

    # Allocate room (with padding in case of varying sizes)
    mb_concat = np.full((len(np_mb), max([len(x) for x in np_mb])), dtype=np.float32, fill_value=np.nan)
    for i, line in enumerate(np_mb):
        mb_concat[i, :len(line)] = line

    # Transpose if the longest axis is vertical
    is_horizontal = mb_concat.shape[0] < mb_concat.shape[1]
    mb_concat = mb_concat if is_horizontal else mb_concat.T
    plt.figure()
    plt.imshow(mb_concat, cmap='hot')
    plt.colorbar(orientation='horizontal')
    plt.suptitle('Bathy Data', fontsize = 18)

# Get sonar data if present
if XTFHeaderType.sonar in p:
    upper_limit = 2 ** 16
    np_chan1 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=0, weighted=True)
    np_chan2 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=1, weighted=True)
    np_chan3 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=2, weighted=True)
    np_chan4 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=3, weighted=True)

    #  Clip to range (max cannot be used due to outliers)
    #  More robust methods are possible (through histograms / statistical outlier removal)
    np_chan1.clip(0, upper_limit - 1, out=np_chan1)
    np_chan2.clip(0, upper_limit - 1, out=np_chan2)
    np_chan3.clip(0, upper_limit - 1, out=np_chan3)
    np_chan4.clip(0, upper_limit - 1, out=np_chan4)

    # The sonar data is logarithmic (dB), add small value to avoid log10(0)
    np_chan1 = np.log10(np_chan1 + 1, dtype=np.float32)
    np_chan2 = np.log10(np_chan2 + 1, dtype=np.float32)
    np_chan3 = np.log10(np_chan3 + 1, dtype=np.float32)
    np_chan4 = np.log10(np_chan4 + 1, dtype=np.float32)

    # Transpose so that the largest axis is horizontal
    np_chan1 = np_chan1 if np_chan1.shape[0] < np_chan1.shape[1] else np_chan1.T
    np_chan2 = np_chan2 if np_chan2.shape[0] < np_chan2.shape[1] else np_chan2.T
    np_chan3 = np_chan3 if np_chan3.shape[0] < np_chan3.shape[1] else np_chan3.T
    np_chan4 = np_chan4 if np_chan4.shape[0] < np_chan4.shape[1] else np_chan4.T

    print(np_chan1)

    # The following plots the waterfall-view in separate subplots
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.imshow(np_chan1, cmap='afmhot', vmin=0, vmax=np.log10(upper_limit))
    # ax2.imshow(np_chan2, cmap='afmhot', vmin=0, vmax=np.log10(upper_limit))
    #ax4.yaxis.set_visible(False)
    #ax3.imshow(np_chan3, cmap='afmhot', vmin=0, vmax=np.log10(upper_limit))
    #ax4.imshow(np_chan4, cmap='afmhot', vmin=0, vmax=np.log10(upper_limit))
#     ax1.invert_xaxis()
#     fig.suptitle('Sonar Data Image', fontsize = 18)
#     fig.tight_layout()
# # #
# #     # The following plots a waterfall-view of the 100th ping (in the file)
#     fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
#     ax1.plot(np.arange(0, np_chan1.shape[1]), np_chan1[196, :])
#     ax2.plot(np.arange(0, np_chan2.shape[1]), np_chan2[196, :])
#     ax3.plot(np.arange(0, np_chan3.shape[1]), np_chan3[196, :])
#     ax4.plot(np.arange(0, np_chan4.shape[1]), np_chan4[196, :])
#     fig.suptitle('Sonar Data Graph', fontsize = 18)
#
# # # Get attitude data if present
# if XTFHeaderType.attitude in p:
#     pings = p[XTFHeaderType.attitude]  # type: List[XTFAttitudeData]
#     heave = [ping.Heave for ping in pings]
#     pitch = [ping.Pitch for ping in pings]
#     roll = [ping.Roll for ping in pings]
#     heading = [ping.Heading for ping in pings]
#
#     fig, (ax1, ax2) = plt.subplots(2, 1)
#     ax1.plot(range(0, len(heave)), heave, label='heave')
#     ax1.plot(range(0, len(pitch)), pitch, label='pitch')
#     ax1.plot(range(0, len(roll)), roll, label='roll')
#     ax1.legend()
#     ax2.plot(range(0, len(heading)), heading, label='heading')
#     ax2.legend()
#     fig.tight_layout()
#     fig.suptitle('Attitude Data', fontsize = 18)
#
# # Get navigation data if present
# if XTFHeaderType.navigation in p:
#     pings = p[XTFHeaderType.navigation]  # type: List[XTFHeaderNavigation]
#     alt = [ping.RawAltitude for ping in pings]
#     x = [ping.RawXcoordinate for ping in pings]
#     y = [ping.RawYcoordinate for ping in pings]
#
#     fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
#     ax1.plot(range(0, len(alt)), alt, label='altitude')
#     ax1.set_title('altitude')
#     ax2.plot(range(0, len(x)), x, label='x')
#     ax2.set_title('x')
#     ax3.plot(range(0, len(y)), y, label='y')
#     ax3.set_title('y')
#     fig.tight_layout()
#     fig.suptitle('Navigation Data', fontsize = 18)
# #
# plt.show()

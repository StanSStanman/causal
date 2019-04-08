import mne
import numpy as np

# def forward_model():


def get_epochs_dics(epochs_event, fwd, fmin=0, fmax=np.inf, tmin=None, tmax=None, tstep=0.005, win_lenghts=0.2,
                    mode='multitaper', mt_bandwidth=None, on_epochs=True, avg_tapers=True):

    if tmin is None:
        tmin = epochs_event.times[0]
    if tmax is None:
        tmax = epochs_event.times[-1] - win_lenghts

    n_tsteps = int(((tmax - tmin) * 1e3) // (tstep * 1e3))

    power = []
    time = np.zeros(n_tsteps)

    for it in range(n_tsteps):

        win_tmin = tmin + (it * tstep)
        win_tmax = win_tmin + win_lenghts
        time[it] = win_tmin + (win_lenghts / 2.)

        avg_csds = None

        print('.....From {0}s to {1}s'.format(win_tmin, win_tmax))

        csds = mne.time_frequency.csd_multitaper(epochs_event, fmin=fmin, fmax=fmax, tmin=tmin, tmax=tmax,
                                                 bandwidth=mt_bandwidth, n_jobs=-1)

        if len(csds[0]._data.shape) > 2:
            avg_csds = mne.time_frequency.csd_multitaper(epochs_event, fmin=fmin, fmax=fmax, tmin=tmin, tmax=tmax,
                                                         bandwidth=mt_bandwidth, n_jobs=-1)

        beamformer = mne.beamformer.make_dics(epochs_event.info, fwd, csds, reg=0.05)
        power_time = mne.beamformer.apply_dics_csd(csds, avg_csds)

        power.append(power_time)

    surface, volume = mne.beamformer.tf_dics(epochs_event, fwd, noise_csds=None, tmin=tmin, tmax=tmax, tstep=tstep,
                                             win_lengths=win_lenghts, mode=mode, freq_bins=None, frequencies=None,
                                             mt_bandwidth=mt_bandwidth, pick_ori=None, inversion='single',
                                             normalize_fwd=False)


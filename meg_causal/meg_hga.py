import mne
import numpy as np
import pandas as pd
import brainets
from directories import *

subjects = ['subject_01', 'subject_02', 'subject_04', 'subject_05', 'subject_06', 'subject_07',
           'subject_08', 'subject_09', 'subject_10', 'subject_11', 'subject_13']
scenarios = range(1, 16)

def compute_singletrial_sourcepower(subj_dir, subject, scenario, event):

    # -------------------------------------------------------------------------------------------------------------------
    # Anatomical data
    # -------------------------------------------------------------------------------------------------------------------
    # File to align coordinate frames meg2mri computed using mne analyze (interactive gui)
    fname_trans = trans_file.format(subject)
    # Brain object file
    fname_brain = brain_file.format(subject)
    # Source space files
    fname_src = src_file.format(subject)

    # Load source space
    brain = pd.read_pickle(fname_brain)
    src = pd.read_pickle(fname_src)

    # ------------------------------------------------------------------------------------------------------------------
    # Functional data
    # ------------------------------------------------------------------------------------------------------------------
    # Epoched event-of-interest data
    fname_event = os.path.join(prep_dir.format(subject, scenario), '{0}_{1}-epo.fif'.format(subject, event))
    epochs_event = mne.read_epochs(fname_event)
    # Epoched baseline data
    fname_baseline = os.path.join(prep_dir.format(subject, scenario), '{0}_baseline-epo.fif'.format(subject))
    epochs_baseline = mne.read_epochs(fname_baseline)
    # Output filename for source power analysis at the atals level
    fname_power =os.path.join(hga_dir.format(subject, scenario), '{0}_{1}_hga_log-epo.fif'.format(subject, event))

    # ------------------------------------------------------------------------------------------------------------------
    # Artifact rejection
    # ------------------------------------------------------------------------------------------------------------------
    fname_ar = os.path.join(prep_dir.format(subject, scenario), '{0}_artifact_rejection.pickle'.format(subject))
    ar_data = pd.read_pickle(fname_ar)

    print('Loading epochs in memory')
    epochs_event.load_data()
    epochs_baseline.load_data()

    print('Removing bad trials')
    if ar_data[0]:
        epochs_event.drop(indices=ar_data[0])
        epochs_baseline.drop(indices=ar_data[0])

    print('Removing bad channels')
    if ar_data[1]:
        epochs_event.drop_channels(ar_data[1])
        epochs_baseline.drop_channels(ar_data[1])
    print('Done')

    # ------------------------------------------------------------------------------------------------------------------
    # Functional parameters
    # ------------------------------------------------------------------------------------------------------------------
    # High-gamma activity (HGA) parameters (k=11)
    fmin = 88
    fmax = 92
    mt_bandwidth = 60
    # High-gamma activity (HGA) parameters (k=19)
    # fmin = 98
    # fmax = 102
    # mt_bandwidth = 100
    # Time parameters
    win_lengths = 0.2
    tstep = 0.005
    # Sampling rate of power estimates
    sfreq = 1 / tstep
    # Initial time points of multitaper window
    if event == 'action':
        # Action
        t_event = [-1.5, 1.5 - win_lengths]
        # t_event = [-0.1, 0.2 - win_lengths]
    elif event == 'outcome':
        # Outcome
        # t_event = [-1.5, 1.5 - win_lengths]
        t_event = [-1.6, 2.1 - win_lengths]
    elif event == 'baseline':
        # Baseline
        t_event = [-1.5, -1.0]
    # Time window for baseline
    t_bline = [-1.5, -1.0]#[1.0, 1.5-win_lengths]#

    # ------------------------------------------------------------------------------------------------------------------
    # Computing the single-shell forward solution using raw data for each session
    # ------------------------------------------------------------------------------------------------------------------
    # for c_s in range(2):

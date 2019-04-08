import os

subjects_dir = os.path.join('D:\\', 'Databases', 'db_mne', 'meg_causal')
prep_dir = os.path.join(subjects_dir, '{0}', 'prep', '{1}')
hga_dir = os.path.join(subjects_dir, '{0}', 'hga', '{1}')

trans_file = os.path.join(subjects_dir, '{0}', 'trans', '{0}-trans.fif')
brain_file = os.path.join(subjects_dir, '{0}', 'src', '{0}-brain.pickle')
src_file = os.path.join(subjects_dir, '{0}', 'src', '{0}-src.pickle')

bem_model_file = os.path.join(subjects_dir, '{0}', 'bem', '{0}-{1}-bem.fif')
bem_sol_file = os.path.join(subjects_dir, '{0}', 'bem', '{0}-{1}-bem-sol.fif')
file_fwd = os.path.join(subjects_dir, '{0}', 'fwd', '{0}-{1}-fwd.fif')
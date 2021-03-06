import os
import os.path as op
import logging
import shutil
import sys
import re
from collections import defaultdict

lgr = logging.getLogger('heudiconv')

def create_key(subdir, file_suffix, outtype=('nii.gz', 'dicom'),
               annotation_classes=None, prefix=''):
    if not subdir:
        raise ValueError('subdir must be a valid format string')
    # may be even add "performing physician" if defined??
    template = os.path.join(
        prefix,
        "{bids_subject_session_dir}",
        subdir,
        "{bids_subject_session_prefix}_%s" % file_suffix
    )
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category 
    subject: participant id 
    seqitem: run number during scanning
    subindex: sub index within group
    session: scan index for longitudinal acq
    """
    lgr.info("Processing %d seqinfo entries", len(seqinfo))
    and_dicom = ('dicom', 'nii.gz')

    #lgr.info("this is a test AAAA")
    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w', 'nii.gz')
    dwi = create_key('sub-{subject}/dwi/sub-{subject}_run-{item:01d}_dwi', 'nii.gz')
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_rec-{rec}_run-{item:01d}_bold', 'nii.gz')
    info = {t1w: [], dwi: [], rest: []}
    for s in seqinfo:
	"""lgr.info("total_files_till_now %s", s.total_files_till_now)
	lgr.info("example_dcm_file  %s", s.example_dcm_file)
	lgr.info("series_id  %s", s.series_id)
	lgr.info("dcm_dir_name  %s", s.dcm_dir_name)
	lgr.info("unspecified2  %s", s.unspecified2)
	lgr.info("unspecified3  %s", s.unspecified3)
	lgr.info("dim1  %s", s.dim1)
	lgr.info("dim2  %s", s.dim2)
	lgr.info("dim3  %s", s.dim3)
	lgr.info("dim4  %s", s.dim4)
	lgr.info("TR  %s", s.TR)
	lgr.info("TE  %s", s.TE)
	lgr.info("protocol_name  %s", s.protocol_name)
	lgr.info("is_motion_corrected  %s", s.is_motion_corrected)
	lgr.info("is_derived  %s", s.is_derived)
	lgr.info("patient_id  %s", s.patient_id)
	lgr.info("study_description  %s", s.study_description)
	lgr.info("referring_physician_name  %s", s.referring_physician_name)
	lgr.info("series_description  %s", s.series_description)
	lgr.info("image_type %s", s.image_type)
        """
        lgr.info("sequece: %s", vars(s))
        if (s.dim3 == 224) and (s.dim4 == 1) and ('t1' in s.protocol_name):
          lgr.info("THIS WILL BE THE T1: %s", s.series_id)
          info[t1w] = [s.series_id] # assign if a single series meets criteria
        if (s.dim3 == 3) and (s.dim2 == 512) and ('t1' in s.protocol_name):
          lgr.info("THIS WILL BE THE T1: %s", s.series_id)
          info[t1w] = [s.series_id] # assign if a single series meets criteria

        if (11 <= s.dim3 <= 22) and (s.dim4 == 1) and ('dti' in s.protocol_name):
          info[dwi].append(s.series_id) # append if multiple series meet criteria
        if (s.dim4 > 10) and ('taskrest' in s.protocol_name):
            if s.is_motion_corrected: # exclude non motion corrected series
                info[rest].append({'item': s.series_id, 'rec': 'corrected'})
            else:
                info[rest].append({'item': s.series_id, 'rec': 'uncorrected'})
    return info

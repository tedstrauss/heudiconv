import os

def create_key(template, outtype=('nii.gz','dicom'), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)

t1w_low_res = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-lowres_T1w')
t1w_high_res = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_acq-highres_T1w')
t2w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')
flanker = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-flanker_bold')
dwi_64dir = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dwi')
dwi_b0s = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_acq-B0s_dwi')
rest = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-rest_bold')

info = {
                t1w_low_res: [],
                t1w_high_res: [],
                t2w: [],
                flanker: [],
                dwi_64dir: [],
                dwi_b0s: [],
                rest: [],
            }

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    data = create_key('run{item:03d}')
    info = {data: []}
    last_run = len(seqinfo)

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:
        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """

        if s.protocol_name == 'MPRAGE GRAPPA2':
            info[t1w_low_res] = [s.series_id]
        if s.protocol_name == 'Axial T2-FLAIR':
            info[t2w] = [s.series_id]
        if s.protocol_name == 'FLANKER':
            info[flanker] = [s.series_id]
        if s.protocol_name == 'REST':
            info[rest] = [s.series_id]
        if s.protocol_name == 'MPRAGE T1 Coronal - TI=900':
            info[t1w_high_res] = [s.series_id]
        if s.protocol_name == 'DTI-64 DIRECTIONS':
            info[dwi_64dir] = [s.series_id]
        if s.protocol_name == 'DTI-EXTRA B0':
            info[dwi_b0s] = [s.series_id]

    return info

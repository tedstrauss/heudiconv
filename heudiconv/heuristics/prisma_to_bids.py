import os
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    dwi = create_key('sub-{subject}/dwi/sub-{subject}_run-{item:01d}_dwi')
    rest = create_key('sub-{subject}/func/sub-{subject}_task-rest_rec-{rec}_run-{item:01d}_bold')
    info = {t1w: [], dwi: [], rest: []}
    for s in seqinfo:
        if (s.dim3 == 176) and (s.dim4 == 1) and ('t1' in s.protocol_name):
          info[t1w] = [s.series_id] # assign if a single series meets criteria
        if (11 <= s.dim3 <= 22) and (s.dim4 == 1) and ('dti' in s.protocol_name):
          info[dwi].append(s.series_id) # append if multiple series meet criteria
        if (s.dim4 > 10) and ('taskrest' in s.protocol_name):
            if s.is_motion_corrected: # exclude non motion corrected series
                info[rest].append({'item': s.series_id, 'rec': 'corrected'})
            else:
                info[rest].append({'item': s.series_id, 'rec': 'uncorrected'})
    return info

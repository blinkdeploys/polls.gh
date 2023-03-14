from django_rq import job     
from report.utils import collate_results, clear_collated_results


@job # ("high", timeout=600) # timeout is optional
def collation_task(context=None):
    # print(f'running job ... {context}')
    total = collate_results(can_clear=True, is_verbose=False)
    print(f'{total} records collated')
    print('::::::::::::::::::::::::::::::::::::::')
    return "Response from async method"

@job
def clear_collation_task():
    return clear_collated_results()

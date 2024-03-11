import itertools

list1 = [1, 2, 3]

print(list1[-1])

while job_index < n:
    job_with_min_runtime = get_next_job_with_minimal_runtime(min_run[-1], job_list)
    min_run.append(job_with_min_runtime)
    job_list.remove(job_with_min_runtime)
    job_index += 1
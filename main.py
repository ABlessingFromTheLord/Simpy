parallel_jobs = []
temp = []
n = len(jobs)

job_index_1 = 0
while job_index_1 < n:
    job_1 = jobs[job_index_1]
    machine = job_1.get_machine_required()
    if job_1 not in temp:
        temp.append(job_1)
        jobs.remove(job_1)
        n -= 1

        job_2_index = 0
        while job_2_index < n:
            if jobs[job_2_index].get_machine_required() == machine:
                temp.append(jobs[job_2_index])
                jobs.remove(jobs[job_2_index])
                n -= 1
            else:
                job_2_index += 1
        parallel_jobs.append(temp.copy())
        temp.clear()
    else:
        job_index_1 += 1
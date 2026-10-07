from ortools.sat.python import cp_model

def solve_job_shop_scheduling(jobs):
    model = cp_model.CpModel()

    all_tasks = []  # List to store all task variables
    all_machines = set()  # Set to store all machine variables
    max_end_time = 0  # Variable to store the maximum end time of all tasks

    # Iterate through each job
    for job_id, job in enumerate(jobs):
        # Iterate through each task in the job
        for task_id, (machine_id, duration) in enumerate(job):
            # Create machine variable representing the machine for the task
            machine_var = model.NewIntVar(0, len(jobs) * sum(t[1] for t in max(job, key=lambda x: x[1])), f"job{job_id}_task{task_id}_machine")
            # Create duration variable representing the duration of the task
            duration_var = model.NewIntVar(duration, duration, f"job{job_id}_task{task_id}_duration")

            # Add task variables to the list
            all_tasks.append((machine_var, duration_var))
            # Add machine variable to the set of all machines
            all_machines.add(machine_var)

            # Constrain the machine variable of the current task to be the same as the previous task
            if task_id > 0:
                model.Add(machine_var == prev_machine_var)

            # Store the current machine variable as the previous machine variable for the next iteration
            prev_machine_var = machine_var

            # Create end variable representing the end time of the task
            end_var = model.NewIntVar(0, len(jobs) * sum(t[1] for t in max(job, key=lambda x: x[1])), f"job{job_id}_task{task_id}_end")
            # Constrain the end variable to be equal to the sum of machine variable and duration variable
            model.Add(duration_var == duration)
            model.Add(end_var == machine_var + duration_var)

            # Update the maximum end time
            if task_id == len(job) - 1:
                max_end_time = max(max_end_time, end_var)

    # Constrain tasks on the same machine to not overlap
    for m in all_machines:
        model.AddNoOverlap([task[0] for task in all_tasks if task[0] == m])

    # Minimize the maximum end time
    model.Minimize(max_end_time)

    # Create a solver instance
    solver = cp_model.CpSolver()

    # Solve the model
    status = solver.Solve(model)

    # Print the optimal schedule if found
    if status == cp_model.OPTIMAL:
        print(f"Optimal Schedule (Makespan: {solver.ObjectiveValue()}):")
        for job_id, job in enumerate(jobs):
            for task_id, (machine_id, duration) in enumerate(job):
                start_time = solver.Value(all_tasks[job_id * len(jobs) + task_id][0])
                print(f"Job {job_id}, Task {task_id}: Machine {machine_id}, Start Time {start_time}, Duration {duration}, End Time {start_time + duration}")
    else:
        print("No solution found.")

# Problem 1
jobs_1 = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 4), (1, 3), (2, 1)],
    [(0, 2), (1, 4), (2, 3)]
]
solve_job_shop_scheduling(jobs_1)

# Problem 2
jobs_2 = [
    [(0, 3), (1, 2), (2, 4), (3, 3)],
    [(1, 5), (0, 3), (3, 2)],
    [(2, 2), (3, 1), (0, 4), (1, 4)],
    [(3, 4), (2, 3), (1, 5)]
]
solve_job_shop_scheduling(jobs_2)

# Problem 3
jobs_3 = [
    [(0, 4), (1, 2), (2, 3), (3, 5), (4, 2)],
    [(2, 2), (3, 1), (1, 3), (4, 4)],
    [(0, 3), (1, 4), (2, 2), (3, 3)]
]
solve_job_shop_scheduling(jobs_3)

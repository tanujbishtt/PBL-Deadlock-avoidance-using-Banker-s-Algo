def run_bankers_algorithm_logic(allocation, max_need, initial_available, num_processes, num_resources):
    need_matrix = [
        [max_need[i][j] - allocation[i][j] for j in range(num_resources)]
        for i in range(num_processes)
    ]
    work_vector = list(initial_available)
    finish_flags = [False] * num_processes
    safe_sequence_order = []
    simulation_steps_log = []
    iterations_without_progress = 0
    while len(safe_sequence_order) < num_processes and iterations_without_progress <= num_processes:
        found_process_in_current_iteration = False
        for i in range(num_processes):
            if not finish_flags[i]:
                can_process_execute = True
                for j in range(num_resources):
                    if need_matrix[i][j] > work_vector[j]:
                        can_process_execute = False
                        break
                if can_process_execute:
                    current_work_before_execution = list(work_vector)
                    for j in range(num_resources):
                        work_vector[j] += allocation[i][j]
                    finish_flags[i] = True
                    safe_sequence_order.append(i)
                    found_process_in_current_iteration = True
                    iterations_without_progress = 0
                    simulation_steps_log.append({
                        "process_executed": i,
                        "work_before_execution": current_work_before_execution,
                        "allocation": list(allocation[i]),
                        "work_after_execution": list(work_vector),
                        "safe_sequence_progress": list(safe_sequence_order)
                    })
                    break
        if not found_process_in_current_iteration:
            iterations_without_progress += 1
            if iterations_without_progress > num_processes:
                break
    is_safe_state = all(finish_flags)
    return need_matrix, simulation_steps_log, safe_sequence_order, is_safe_state

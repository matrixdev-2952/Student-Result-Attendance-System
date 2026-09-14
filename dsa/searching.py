def binary_search(students, target_roll):

    low = 0
    high = len(students) - 1

    while low <= high:

        mid = (low + high) // 2

        current_roll = students[mid]["roll_no"]

        if current_roll == target_roll:
            return students[mid]

        elif current_roll < target_roll:
            low = mid + 1

        else:
            high = mid - 1

    return None
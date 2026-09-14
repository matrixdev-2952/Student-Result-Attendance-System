def merge_sort(students):
    """
    Sort students by average marks
    in descending order using Merge Sort.
    """

    # Base case
    if len(students) <= 1:
        return students

    # Find middle
    mid = len(students) // 2

    # Divide the list
    left = merge_sort(students[:mid])
    right = merge_sort(students[mid:])

    # Merge sorted halves
    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["average"] >= right[j]["average"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements from left
    while i < len(left):
        result.append(left[i])
        i += 1

    # Add remaining elements from right
    while j < len(right):
        result.append(right[j])
        j += 1

    return result
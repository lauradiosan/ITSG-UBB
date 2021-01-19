def get_mask_overlap(mask1, mask2):
    result = []
    true_count = 0
    for i in range(len(mask1)):
        for j in range(len(mask1[i])):
            if mask1[i][j]:
                if mask2[i][j]:
                    true_count += 1
                    result.append(1)
                else:
                    result.append(0)

    if true_count == 0:
        return 0

    return sum(result) / true_count

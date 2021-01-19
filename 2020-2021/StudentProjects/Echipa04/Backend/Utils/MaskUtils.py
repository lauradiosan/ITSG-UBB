from PIL import Image


class MaskUtils:
    def get_empty_mask(self, width, height):
        result = []
        for i in range(height):
            result.append([])
            for j in range(width):
                result[i].append(0)
        return result

    def combine_masks(self, masks, width, height):
        result_mask = self.get_empty_mask(width, height)
        if masks is not None:
            for mask in masks:
                for i in range(len(mask)):
                    for j in range(len(mask[i])):
                        if mask[i][j]:
                            result_mask[i][j] = 1
        return result_mask

    def get_intersection_union_sum(self, expected, output):
        intersection = 0
        union = 0
        sum = 0
        for i in range(len(output)):
            for j in range(len(output[i])):
                comb = output[i][j] + expected[i][j]
                sum += comb
                if comb > 0:
                    union += 1
                if comb == 2:
                    intersection += 1
        return intersection, union, sum

    def print_mask(self, mask):
        res = ""
        for i in range(len(mask)):
            for j in range(len(mask[i])):
                res += str(mask[i][j])
            res += '\n'
        print(res)

    def draw_mask(self, mask, output):
        img = Image.new('RGB', (len(mask), len(mask[0])), color=(0, 0, 0))
        for x in range(len(mask)):
            for y in range(len(mask[x])):
                if mask[x][y]:
                    img.putpixel((x, y), (255, 255, 255))
        img.save(output)

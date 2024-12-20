import cv2
import numpy as np

img = cv2.imread("ascii.png", cv2.IMREAD_UNCHANGED)
np_image = np.array(img)
a = """\"#$%&'()*+,-./
        0123456789:;<=>?
        @ABCDEFGHIJKLMNO
        PQRSTUVWXYZ[\\]^_
        `abcdefghijklmno
        pqrstuvwxyz{|}~"""
b = [3, 1396910056791, 4815521733, 18859827505, 23938666821, 3, 1118805, 346385, 341, 139432065, 193, 1015809, 65, 1143087377,
33424543941, 33858929199, 15619998255, 17749822105, 15620127807, 15621129293, 4433658431, 15621113391, 6728664623, 69, 197, 138547785, 1040219137, 19170337, 4299440687,
18842451503, 16694951471, 15603893807, 16694953519, 33320639551, 1108384831, 15621219391, 18842451505, 1909911, 15620129297, 18842164529, 33320633377, 18842441585, 18842703473, 15621211695,
23942710831, 18842435119, 15620126783, 4433514655, 15621211697, 4641572401, 19182175793, 18842194257, 4433514833, 33321787935, 1872463, 17456826433, 1984807, 17733, 1065151889409,
32814675969, 16695014433, 15604430849, 32801348113, 32278886401, 35794733, 533600991233, 18842498081, 125, 499877691409, 156457233, 9557, 18846755841, 18842434561, 15621208065,
567960983553, 1108980737, 16657741825, 1123795, 32801080321, 4648911873, 32939492353, 18593694721, 533600977921, 33357593601, 1122965, 127, 338065, 1639, ]


def char_to_int(np_array):
    h, w, _ = np_array.shape
    res = 0
    i = 0
    for y in range(h):
        for x in range(w):
            if np.array_equal(np_array[y, x], [0, 255, 0, 255]):
                res += 2 ** i
            i += 1
    return res

height, width, channels = np_image.shape
char_height = 8
char_width = 8

prev_x = 0
for y in range(0, height, 8):
    for x in range(0, width):
        if np.all(np_image[y:y+8, x] == [0,0,0,0]):
            char = char_to_int(np_image[y:y + 8, prev_x:x])
            if char > 1:
                print(char, end = ", ")
            prev_x = x + 1
    print()

# new_image = np.zeros_like(np_image)
# i, j = 0, 0
# pas = False
# for y in range(0, height, 8):
#     i = y
#     j = 0
#     for x in range(0, width, 8):
#         new_image[i,j] = [0, 255, 0, 255]
#         for w in range(char_width):
#             if not np.all(np_image[y:y+8, x+w] == 0):
#                 for h in range(char_height):
#                     new_image[i, j] = np_image[y+h, x+w]
#                     i += 1
#                 j += 1
#                 i = y
#             else:
#                 if not pas:
#                     for h in range(char_height):
#                         new_image[i, j] = [0,0,0,0]
#                         i += 1
#                     j += 1
#                     i = y
#                     pas = True
#         pas = False
#             # else:
#             #     for h in range(char_height):
#             #         new_image[y+h, x+w] = [255,255,255,255]
# # cv2.imshow("aboba",np_image)
# cv2.imwrite('ascii.png', new_image)
# # cv2.waitKey(0)
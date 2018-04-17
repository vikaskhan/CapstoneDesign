import sys
sys.path.insert(0, '~/opencv_workspace/')
import opencv as cv2

counter = 0

for i in range(1:4000)
    if 0 < i < 10:
        image = cv2.imread('neg-000' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
    elif 10 <= i < 100:
        image = cv2.imread('neg-00' + str(i))   
    elif 100 <= i < 1000:
        image = cv2.imread('neg-0' + str(i))   
    elif 1000 <= i < 10000:
        image = cv2.imread('neg-' + str(i))
    if not image is None:
        new_image = cv2.resize(image, (100, 100))
        cv2.imwrite("neg"+str(counter)+".jpg",new_image)
        counter+=1

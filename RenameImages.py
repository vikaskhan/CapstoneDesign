import cv2

counter = 0
image = None

for i in range(2000):
    if 0 <= i < 10:
        image = cv2.imread('NegImages/neg-000' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
    elif 10 <= i < 100:
        image = cv2.imread('NegImages/neg-00' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)   
    elif 100 <= i < 1000:
        image = cv2.imread('NegImages/neg-0' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)   
    elif 1000 <= i < 10000:
        image = cv2.imread('NegImages/neg-' + str(i) + '.jpg', cv2.IMREAD_GRAYSCALE)
    if not image is None:
        new_image = cv2.resize(image, (100, 100))
        cv2.imwrite("NegImages/neg"+str(counter)+".jpg",new_image)
        line = "NegImages/neg"+str(counter)+".jpg\n"
        with open('bg.txt', 'a') as f:
            f.write(line)
        counter+=1

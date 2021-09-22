from random import shuffle
import cv2


def img2bipolar(mat, t):
    matt = mat.copy()
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] < t:
                matt[i][j] = -1
            else:
                matt[i][j] = 1
    return matt


def bipolar2img(mat):
    matt = mat.copy()
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 1:
                matt[i][j] = 255
            else:
                matt[i][j] = 0
    return matt


def mat2vec(mat):
    vec = []
    for v in mat:
        for element in v:
            vec.append(element)
    return vec


def vec2mat(vec, a, mat):
    matt = mat.copy()
    for i in range(a):
        for j in range(a):
            matt[i][j] = vec[i*a+j]
    return matt


def create_w(vec):
    w = []
    for i in range(len(vec)):
        v = []
        for j in range(len(vec)):
            if i == j:
                v.append(0)
            else:
                v.append(1 if vec[i] == vec[j] else -1)
        w.append(v)
    return w


def iteration(first_vec, w, theta, iterations, last_s, check):
    if iterations == 0 or check:
        return first_vec
    print(iterations)
    check = True
    total = list(range(len(first_vec)))
    for k in range(len(first_vec)):
        shuffle(total)
        i = total.pop()
        if iterations != ITERATIONS:
            s = last_s[i]
        else:
            s = 0
            for j in range(len(first_vec)):
                if i != j:
                    if w[j][i] == first_vec[j]:
                        s += 1
                    else:
                        s -= 1
            last_s[i] = s
        if s+first_vec[i] > theta and first_vec[i] != 1:
            if check:
                print("change")
                check = False
            for p in range(len(first_vec)):
                last_s[p] += w[p][i]*2
            first_vec[i] = 1
        elif s+first_vec[i] < theta and first_vec[i] != -1:
            if check:
                print("change")
                check = False
            for p in range(len(first_vec)):
                last_s[p] -= w[p][i]*2
            first_vec[i] = -1

    return iteration(first_vec, w, theta, iterations-1, last_s, check)


if __name__ == "__main__":
    T = 128
    ITERATIONS = 8000

    train_img = cv2.imread('train.jpg')
    train_img = cv2.resize(train_img, (80, 80))
    train_imgGray = cv2.cvtColor(train_img, cv2.COLOR_BGR2GRAY)
    bipolar_train_img = img2bipolar(train_imgGray, T)
    img_w = create_w(mat2vec(bipolar_train_img))
    train_img_ = bipolar2img(bipolar_train_img)
    cv2.imwrite("train_.png", train_img_)
    print("Training Finished")
    print("Recycling...")

    test_img = cv2.imread('test.jpg')
    test_img = cv2.resize(test_img, (80, 80))
    test_imgGray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    bipolar_test_img = img2bipolar(test_imgGray, T)
    recycled_img = bipolar2img(vec2mat(iteration(mat2vec(bipolar_test_img), img_w, 0, ITERATIONS, [0]*ITERATIONS, False),
                                       80, bipolar_test_img))
    cv2.imwrite("test_.png", recycled_img)

    cv2.imshow('Train image', train_img_)
    cv2.imshow('Recycled Image', recycled_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

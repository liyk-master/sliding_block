import cv2 as cv


def get_pos(image):
    # 高斯滤波
    blurred = cv.GaussianBlur(image, (5, 5), 0)
    # 图像二值化
    canny = cv.Canny(blurred, 200, 400)
    # 提取边缘轮廓  参数说明 分别为: 二值图像, 只检测最外围轮廓, 仅保存轮廓的拐点信息
    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        M = cv.moments(contour)  # 计算边缘值的形状和方向  主要是判断方向
        if M['m00'] == 0:
            cx = 0
        else:
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        # 面积在5000-70000之间 且 周长在 300-390  依次来筛选在指定范围大小的矩形
        if 5000 < cv.contourArea(contour) < 7000 and 300 < cv.arcLength(contour, True) < 390:  # 计算轮廓的面积
            if cx < 240:
                continue
            x, y, w, h = cv.boundingRect(contour)  # 最小外接矩形
            # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  #显示外接矩形
            # cv.imshow("test",image)
            return x * 341 / 672  # 341 * 672 是实际尺寸和显示尺寸
    return 0


if __name__ == '__main__':
    img0 = cv.imread('./img/douban.jpg')
    res = get_pos(img0)
    print("res：", res)
    # 等待执行完毕 0 一直执行
    cv.waitKey(0)
    # while True:
    #     if cv.waitKey(0) == ord("q"):
    #         print("进程退出！")
    #         break
    # 释放内存
    cv.destroyAllWindows()

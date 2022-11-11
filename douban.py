import asyncio
from pyppeteer import launch
import requests
import cv2 as cv
import test as ts
import json

width, height = 1366, 768


# 下载背景图
def downLoadImg(uri, imgName):
    content = requests.get(uri).content  # 下载背景
    f = open('./img/' + imgName, mode='wb')
    f.write(content)
    f.close()
    print('下载完成背景图片')


async def main():
    browser = await launch(headless=False,
                           args=[f'--window-size={width},{height}', '--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.goto(
        'https://accounts.douban.com/passport/login')
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.click('.account-tab-account')  # 点击密码登录
    await page.waitFor(1000)  # 等待一秒操作
    await page.type('#username', "15600717958", {"delay": 50})  # delay 模拟人操作
    await page.waitFor(1000)
    await page.type('#password', "15600717958lyk", {"delay": 50})
    await page.waitFor(1000)
    await page.click('.account-form-field-submit')  # click 点击事件
    await page.waitForSelector('#tcaptcha_iframe_dy')  # 等待验证出现
    await page.waitFor(1000)
    frame = page.frames  # 得到page中所有iframe对象的列表iframe = frame[0]# 如果iframe内还有iframe，则使用childFrames取出子iframe列表childiframes = iframe.childFrames# iframe对象可以定位节点，获取属性值等，与page对象用法相同，但在页面操作中不同
    # 循环执行
    step = 0
    while True:
        if step > 9:
            print('滑块失败！')
            break
        # 获取distance
        slideBg = await frame[1].J("#slideBg")
        # divImg = await frame[1].evaluate('(slideBg) => slideBg.style.background-image', slideBg)
        divImg = await slideBg.getProperty('style')
        divImg1 = await divImg.getProperty('background-image')
        divImg2 = await divImg1.jsonValue()
        # 组装图片url https://t.captcha.qq.com/
        uri = 'https://t.captcha.qq.com/' + divImg2[6:-2]
        # 下载下来
        # 用resqust下载图片
        downLoadImg(uri, 'douban.png')
        img0 = cv.imread('./img/douban.png')
        distance = ts.get_pos(img0)
        if distance == 0:   # 等于零计算失败 刷新验证码重新执行
            await frame[1].click('#reload')
            await frame[1].waitFor(3000)
            print('计算失败，重新计算！！')
            continue


        el = await frame[1].J('.tc-fg-item')
        box = await el.boundingBox()
        await frame[1].hover('.tc-fg-item')  # 模拟鼠标移动到选择元素
        await page.mouse.down()
        await page.mouse.move(box['x'] + distance, box['y'], {"steps": 50})
        await page.mouse.up()
        # await page.waitFor(2000)
        step += 1
        # 判断是否滑块成功
        finalResponse = await page.waitForResponse(lambda res: res.url == 'https://t.captcha.qq.com/cap_union_new_verify' and res.status == 200)
        result = await finalResponse.json()
        # print(type(result))
        # print(result['errorCode'])
        if int(result['errorCode']) > 0:
            await frame[1].click('#reload')
            print('滑动失败，重新计算滑动！！')
            continue
        else:
            print('滑动成功，关闭浏览器~~~')
            break

    await page.close()


asyncio.get_event_loop().run_until_complete(main())

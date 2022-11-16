import asyncio
import requests
from pyppeteer import launch


async def main():
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto('https://www.toutiao.com')
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.waitFor(2000)  # 等待页面加载完毕
    # 拉取默认的数量
    res = await page.querySelectorAll('.feed-card-article-l')
    # print(res)
    for i in range(len(res)):
        # 推送前三条数据
        if i > 2:
            break
        a_res = await res[i].J('a')
        a_href = await (await a_res.getProperty('href')).jsonValue()
        a_value = await (await a_res.getProperty('textContent')).jsonValue()
        # a_dic = {
        #     "a_href": a_href,
        #     "a_value": a_value,
        # }
        # a_res_value.append(a_dic)
        # 直接循环推送给自己
        data = {
            "user_id": '2874459391',
            "message": str(a_value) + '\n' + str(a_href),
        }
        response = requests.post(url='http://domain/send_private_msg', data=data).json()   # 发送到QQ
        print(response)

    # await asyncio.sleep(100)
    # await page.waitFor(1)
    print('执行成功~~')
    await page.close()


asyncio.get_event_loop().run_until_complete(main())

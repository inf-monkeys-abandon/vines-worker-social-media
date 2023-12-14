from playwright.sync_api import sync_playwright
from .utils import get_statics_folder


def sign(uri, data=None, a1="", web_session=""):
    err_msg = ""
    max_tries = 5
    tried = 0
    for i in range(max_tries):
        try:
            tried += 1
            with sync_playwright() as playwright:
                stealth_js_folder = get_statics_folder()
                stealth_js_path = f"{stealth_js_folder}/stealth.min.js"
                print(f"Load stealth.min.js at {stealth_js_path}")
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                context_page.wait_for_load_state()
                # # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                # sleep(5)
                print("开始计算签名")
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                print("签名结果：", encrypt_params)
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception as e:
            print(e)
            err_msg = str(e)
            if tried > max_tries:
                # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
                raise Exception(f"签名失败: {err_msg}")

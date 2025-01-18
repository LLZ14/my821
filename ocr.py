import tkinter as tk
from tkinter import messagebox
import threading
import requests
import pyautogui
import cv2
import time
import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import numpy as np

# 配置日志
logging.basicConfig(filename='ocr_monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 屏幕截图
def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)  # region参数可以限定截图的区域
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)  # 转换为BGR格式
    return screenshot

# 保存截图到本地，文件夹命名为qq邮箱（弃用）
# def save_screenshot(screenshot, save_path):
#     # 确保路径正确，包含扩展名
#     if not save_path.lower().endswith(('.png', '.jpg', '.jpeg')):
#         save_path += ".png"  # 默认保存为.png格式
#
#     if not os.path.exists(os.path.dirname(save_path)):
#         os.makedirs(os.path.dirname(save_path))  # 如果目录不存在，创建目录
#
#     if screenshot is not None and screenshot.size > 0:
#         result = cv2.imwrite(save_path, screenshot)  # 保存为文件
#         if result:
#             print(f"截图已保存到: {save_path}")  # 控制台输出
#             logging.info(f"截图已保存到: {save_path}")
#         else:
#             print(f"无法保存截图到: {save_path}")  # 控制台输出
#             logging.error(f"无法保存截图到: {save_path}")
#     else:
#         print("截图无效，无法保存。")  # 控制台输出
#         logging.error("截图无效，无法保存。")
# 保存截图到本地
def save_screenshot(screenshot, save_dir="saved_screenshots"):
    # 设置固定的保存文件夹名为 'save_pic'
    save_dir = "save_pic"  #

    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # 如果目录不存在，创建目录

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(save_dir, f"monitor_{timestamp}.png")

    if screenshot is not None and screenshot.size > 0:
        result = cv2.imwrite(save_path, screenshot)  # 保存为文件
        if result:
            print(f"截图已保存到: {save_path}")  # 控制台输出
            logging.info(f"截图已保存到: {save_path}")
        else:
            print(f"无法保存截图到: {save_path}")  # 控制台输出
            logging.error(f"无法保存截图到: {save_path}")
    else:
        print("截图无效，无法保存。")  # 控制台输出
        logging.error("截图无效，无法保存。")


#删除本地图片

# 请求本地OCR接口进行识别
def ocr_with_local_api(image, ocr_ip, username="user"):
    ocr_url = f"http://{ocr_ip}:5001/readImage"  # 固定端口和路径
    files = {
        'file': ('screenshot.png', cv2.imencode('.png', image)[1].tobytes(), 'image/png'),
    }
    data = {'username': username}

    try:
        response = requests.post(ocr_url, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            if 'answer' in result:
                return result['answer'], result['img_stream']
            else:
                print(f"OCR接口未返回有效结果: {response.text}")  # 控制台输出
                logging.error(f"OCR接口未返回有效结果: {response.text}")
                # 弹出警告框并恢复界面
                if app:
                    app.append_output("服务请求失败，正在恢复...\n")
                    messagebox.showwarning("警告", "服务请求失败，请检查OCR服务。")
                return None, None
        else:
            print(f"请求本地OCR接口失败: {response.status_code} - {response.text}")  # 控制台输出
            logging.error(f"请求本地OCR接口失败: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"请求OCR接口时发生错误: {str(e)}")  # 控制台输出
        logging.error(f"请求OCR接口时发生错误: {str(e)}")
        # 弹出警告框并恢复界面
        if app:
            app.append_output("服务请求失败，正在恢复...\n")
            messagebox.showwarning("警告", "服务请求失败，请检查OCR服务。")
        return None, None


# 邮件通知
def send_email(subject, body, receiver_emails):
    sender_email = "@qq.com"  # 发送邮箱地址
    password = ""  # 发送邮箱授权码

    # 确保 body 是一个字符串，如果传入的是列表，则合并为一个字符串
    if isinstance(body, list):
        body = "\n".join(body)

    # 确保receiver_emails是一个列表，使用逗号分隔邮箱
    if isinstance(receiver_emails, str):
        receiver_emails = [email.strip() for email in receiver_emails.split(",")]

    # 打印调试信息，查看收件人邮箱地址列表
    print(f"收件人邮箱列表: {receiver_emails}")
    logging.info(f"收件人邮箱列表: {receiver_emails}")
    app.append_output(f"收件人邮箱列表: {receiver_emails}")

    # 遍历所有收件人邮箱，逐一发送
    for receiver_email in receiver_emails:
        if "@" not in receiver_email or "." not in receiver_email:
            print(f"邮箱地址格式不正确: {receiver_email}")
            logging.error(f"邮箱地址格式不正确: {receiver_email}")
            app.append_output(f"邮箱地址格式不正确: {receiver_email}")
            continue  # 如果格式错误，跳过该邮箱

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP_SSL('smtp.qq.com', 465)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.close()
            print(f"邮件已发送给: {receiver_email}")  # 控制台输出
            logging.info(f"邮件已发送给: {receiver_email}")
            app.append_output(f"邮件已发送给: {receiver_email}")
        except Exception as e:
            print(f"邮件发送失败给 {receiver_email}: {str(e)}")  # 控制台输出
            logging.error(f"邮件发送失败给 {receiver_email}: {str(e)}")
            app.append_output(f"邮件发送失败给 {receiver_email}: {str(e)}")



# 定期监控并识别
def monitor_screen(interval=5, target_texts=None, save_dir="save_pic", email_sent_event=None, app=None):
    round_counter = 1

    if target_texts is None:
        target_texts = ["10s完成", "验证码", "请输入", "验证", "挂机", "完成"]

    while True:
        if email_sent_event and email_sent_event.is_set():
            app.append_output("邮件已发送，停止监控并删除截图。\n")
            print("邮件已发送，停止监控并删除截图。")
            logging.info("邮件已发送，停止监控并删除截图。")
            app.stop_monitoring()
            break

        app.append_output(f"第{round_counter}轮监听任务开始...")
        logging.info(f"第{round_counter}轮监听任务开始...")

        screenshot = capture_screen()
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # 保证 save_dir 是固定的文件夹路径，而不是邮箱地址
        save_path = os.path.join(save_dir, f"monitor_{timestamp}.png")
        save_screenshot(screenshot, save_path)

        ocr_ip = app.ocr_url_entry.get().strip()
        recognized_text, _ = ocr_with_local_api(screenshot, ocr_ip)

        if recognized_text:
            print(f"识别文本: {recognized_text}")
            logging.info(f"识别文本: {recognized_text}")
            matched = False
            for target_text in target_texts:
                if target_text in recognized_text:
                    app.append_output(f"检测到目标文本: {target_text}")
                    print(f"检测到目标文本: {target_text}")
                    logging.info(f"检测到目标文本: {target_text}")
                    matched = True
                    if email_sent_event and not email_sent_event.is_set():
                        app.append_output("准备发送邮件...\n")
                        email_sent_event.set()
                        send_email("触发验证，请及时验证", f"检测到的文本为: {target_text}\n截图已保存",
                                   app.receiver_email)
                        if send_email:
                            app.append_output("邮件已发送，停止监控并删除截图。\n")
                            print("邮件已发送，停止监控并保存了截图.")
                            logging.info("邮件已发送，停止监控并保存了截图.")
                            break
                        else:
                            app.append_output("邮件发送失败.\n")
                            print("邮件发送失败.")
                            logging.error("邮件发送失败.")
                            break

            if not matched:
                if os.path.exists(save_path):
                    os.remove(save_path)
                    app.append_output(f"未检测到目标文本，已删除截图: {save_path}")
                    print(f"未检测到目标文本，已删除截图: {save_path}")
                    logging.info(f"未检测到目标文本，已删除截图: {save_path}")
                else:
                    app.append_output(f"未检测到目标文本，但截图不存在: {save_path}")
                    print(f"未检测到目标文本，但截图不存在: {save_path}")
                    logging.info(f"未检测到目标文本，但截图不存在: {save_path}")



        app.append_output(f"第{round_counter}轮监听任务完成。\n")
        logging.info(f"第{round_counter}轮监听任务完成。\n")
        round_counter += 1

        time.sleep(interval)


# 启动监控线程
def start_monitoring_thread(interval=5, target_texts=None, email_sent_event=None, app=None):
    # monitor_thread = threading.Thread(target=monitor_screen, args=(interval, target_texts, app.receiver_email, email_sent_event, app))
    # 在启动监控线程时传递一个固定的文件夹路径，而不是邮箱地址
    monitor_thread = threading.Thread(target=monitor_screen,args=(interval, target_texts, "save_pic", email_sent_event, app))

    monitor_thread.daemon = True
    monitor_thread.start()

# 修改启动监控的函数
class OCRMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR监控工具")
        self.root.geometry("600x550")  # 增加高度
        self.root.resizable(False, False)  # 禁止自动拉伸窗口
        self.root.eval('tk::PlaceWindow . center')  # 窗口在屏幕中央
        self.is_monitoring = False
        self.target_texts = []
        self.receiver_email = ""
        self.ocr_url = ""
        self.email_sent_event = threading.Event()  # 初始化Event对象
        self.monitor_thread = None  # 用来保存线程对象

        self.create_widgets()

    def create_widgets(self):
        # 开始按钮
        self.start_button = tk.Button(self.root, text="开始监听", command=self.start_monitoring)
        self.start_button.pack(pady=10)

        # 停止按钮
        self.stop_button = tk.Button(self.root, text="停止监听", state="disabled", command=self.stop_monitoring)
        self.stop_button.pack(pady=10)

        # 目标文本输入框
        self.target_text_label = tk.Label(self.root, text="请输入目标文本（分号隔开）：")
        self.target_text_label.pack(pady=5)

        self.target_text_entry = tk.Entry(self.root, width=40)
        self.target_text_entry.pack(pady=5)

        # OCR服务器IP输入框
        self.ocr_url_label = tk.Label(self.root, text="请输入OCR服务器IP地址：")
        self.ocr_url_label.pack(pady=5)

        self.ocr_url_entry = tk.Entry(self.root, width=40)
        self.ocr_url_entry.pack(pady=5)

        # 收件人邮箱输入框
        self.receiver_email_label = tk.Label(self.root, text="请输入收件人邮箱（多个邮箱请使用en，分隔）：")
        self.receiver_email_label.pack(pady=5)

        self.receiver_email_entry = tk.Entry(self.root, width=40)
        self.receiver_email_entry.pack(pady=5)

        # 添加时间间隔输入框
        self.interval_label = tk.Label(self.root, text="请输入时间间隔（秒）：")
        self.interval_label.pack(pady=5)

        self.interval_entry = tk.Entry(self.root, width=40)
        self.interval_entry.pack(pady=5)

        # 输出框
        self.output_text = tk.Text(self.root, width=70, height=15)
        self.output_text.pack(pady=10)

    def append_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def start_monitoring(self):
        target_texts_input = self.target_text_entry.get().strip()
        self.receiver_email = self.receiver_email_entry.get().strip()
        self.ocr_url = self.ocr_url_entry.get().strip()

        # 获取时间间隔，确保是有效的数字
        interval_input = self.interval_entry.get().strip()

        if not interval_input.isdigit() or int(interval_input) <= 0:
            messagebox.showerror("错误", "请输入有效的时间间隔（正整数）")
            return
        interval = int(interval_input)

        if not target_texts_input:
            messagebox.showerror("错误", "请输入监控文本内容")
            return

        if not self.receiver_email:
            messagebox.showerror("错误", "请输入收件人邮箱")
            return

        if not self.ocr_url:
            messagebox.showerror("错误", "请输入OCR服务器IP地址")
            return

        # 验证邮箱格式
        if "@" not in self.receiver_email or "." not in self.receiver_email:
            messagebox.showerror("错误", "请输入有效的邮箱")
            return

        # 分割目标文本
        self.target_texts = [text.strip() for text in target_texts_input.split(";")]

        # 禁用开始按钮，启用停止按钮
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # 最小化应用界面
        self.root.iconify()

        # 清除旧的任务标志和事件
        self.email_sent_event.clear()

        # 启动监控线程，传递时间间隔
        start_monitoring_thread(interval=interval, target_texts=self.target_texts,
                                email_sent_event=self.email_sent_event, app=self)

        self.append_output(f"监听任务已启动，间隔时间为 {interval} 秒...\n")

    def stop_monitoring(self):
        self.append_output("监听任务已停止。\n")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

        # 恢复显示应用界面
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRMonitorApp(root)
    root.mainloop()

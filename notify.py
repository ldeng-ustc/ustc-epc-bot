import platform
import smtplib, email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

if platform.system() == "Windows":
    import winsound
    # pywin32在venv下会出现问题，运行报错：
    #    ImportError: DLL load failed while importing win32api: 找不到指定的模块。
    # 这里若Import失败，提供一个空类以供使用
    try:
        from win10toast_click import ToastNotifier
    except:
        class ToastNotifier:
            def show_toast(*args, **kvargs):
                pass



class EmailSender:

    def __init__(self, addr, pwd):
        self.smtp = addr.split("@")[1]
        self.addr = addr
        self.pwd  = pwd

    def send(self, subject, content):
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"]    = self.addr
        msg["To"]      = self.addr
        text = MIMEText(content, "html", "utf-8")
        msg.attach(text)
        smtp = smtplib.SMTP()
        smtp.connect(self.smtp)
        smtp.login(self.addr, self.pwd)
        smtp.sendmail(self.addr, self.addr, msg.as_string())
        smtp.quit()


class DesktopToaster:
    def __init__(self) -> None:
        if platform.system() == "Windows":
            self.toaster = ToastNotifier()
        else:
            self.toaster = None


    def on_destroy(self, hwnd, msg, wparam, lparam):
        pass

    def toast(self, subject, content):
        if self.toast is not None:
            self.toaster.show_toast(subject, content, icon_path="python.ico", threaded=True)
            winsound.PlaySound("./misc/chirp.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

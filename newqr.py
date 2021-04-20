import requests
import urllib.parse

class NewQRLogin:
    API_URL = "https://api.lrtt.icu/secondaryQrCodeLogin.do"
    HEADERS = {
        "android_lite": {
            "User-Agent": "LLA/2.12.0 SKR-H0 9",
            "X-Line-Application": "ANDROIDLITE\t2.12.0\tAndroid OS\t9;SECONDARY"
        },
        "android": {
            "User-Agent": "Line/10.6.2",
            "X-Line-Application": "ANDROID\t10.6.2\tAndroid OS\t10"
        },
        "ios_ipad": {
            "User-Agent": "Line/10.1.1",
            "X-Line-Application": "IOSIPAD\t10.1.1\tiPhone 8\t11.2.5"
        },
        "ios": {
            "User-Agent": "Line/10.1.1",
            "X-Line-Application": "IOS\t10.1.1\tiPhone 8\t11.2.5"
        },
        "chrome": {
            "User-Agent": "Line/2.1.5",
            "X-Line-Application": "CHROMEOS\t2.1.5\tChrome OS\t12.1.1"
        },
        "desktopwin": {
            "User-Agent": "Line/5.12.3",
            "X-Line-Application": "DESKTOPWIN\t5.21.3\tWindows\t10"
        },
        "desktopmac": {
            "User-Agent": "Line/5.12.3",
            "X-Line-Application": "DESKTOPMAC\t5.21.3\tMAC\t10.15"
        }
    }

    def parseLogin(this, loginInfo):
        return (loginInfo["token"], loginInfo["certificate"])

    def loginWithQrCode(self, header, certificate="", callback=lambda output: print(output)):
        assert header in self.HEADERS, "invaild header"
        resp = requests.post(self.API_URL + "/login?" + urllib.parse.urlencode({"custom_headers": self.HEADERS[header], "certificate": certificate}))
        res = resp.json()
        if resp.status_code != 200:
            raise Exception(res)
        callback("Login URL: %s" % (res["url"]))

        while "token" not in res:
            resp = requests.post(self.API_URL + res["callback"])
            res = resp.json()
            if resp.status_code != 200:
                raise Exception(res)

            if "pin" in res:
                callback("𝙲𝙾𝙳𝙴 𝙿𝙸𝙽 : %s" % (res["pin"]))

        return res['token']

    def loginQrCodeWithWebPinCode(self, header, certificate="", callback=lambda output: print(output)):
        assert header in self.HEADERS, "invaild header"
        resp = requests.post(self.API_URL + "/login?" + urllib.parse.urlencode({"custom_headers": self.HEADERS[header], "certificate": certificate}))
        res = resp.json()
        if resp.status_code != 200:
            raise Exception(res)
        callback("เข้าเว็ปนี้ก่อนล็อคอิน\n %s" % (res["web"]))
        callback("กดลิงค์นี้ภายใน 2 นาทีนะ\n%s" % (res["url"]))

        while "token" not in res:
            resp = requests.post(self.API_URL + res["callback"])
            res = resp.json()
            if resp.status_code != 200:
                raise Exception(res)

        return res['token']

if __name__ == "__main__":
    qrv2 = NewQRLogin()
    token, cert = qrv2.loginQrCodeWithWebPinCode("android_lite")
    print("Access Token: " + token)
    print("Certificate: " + cert)
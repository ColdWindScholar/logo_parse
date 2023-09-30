import os
import sys

magic = b'\xff\xd8\xff\xe0'


def tell_head(path):
    with open(path, 'rb') as logo:
        buf = logo.read(4)
        if len(buf) < 4:
            print("解析到尾部")
            return False
        while buf != magic:
            buf = logo.read(4)
        else:
            seek = logo.tell() - 4
            return seek


def parse(path):
    print(f"Start parse {path}")
    print("开始截取文件:splash.jpg")
    if not (seek := tell_head(path)):
        print("非LOGO文件")
    else:
        with open(path, 'rb') as logo:
            logo.seek(seek)
            with open(os.path.join(os.path.dirname(path), 'splash.jpg'), 'wb') as splash:
                buf = logo.read(200)
                splash.write(buf)
                while len(buf) == 200:
                    buf = logo.read(200)
                    splash.write(buf)
                else:
                    splash.write(logo.read(200))


def write(jpg, logo):
    print(f"写入{jpg}到{logo}")
    seek = tell_head(logo)
    if tell_head(jpg) == 0 and seek:
        print("文件头解析通过")
        header = open(logo, 'rb').read(seek)
        with open(logo, 'wb') as new, open(jpg, 'rb') as pic:
            new.write(header)
            new.write(pic.read())
        print("完毕！")
    else:
        print(f"{logo}或{jpg}格式错误")


def usage():
    print('''
    机顶盒LOGO分解打包工具
    作者:寒风居士 QQ:3590361911
    用法：
    logo_parse parse logo.img 【分析logo并解包镜像】
    logo_parse write logo.jpg logo.img 【写入新的JPG到LOGO】
    ''')


if __name__ == '__main__':
    if (sen := len(sys.argv)) < 2:
        usage()
    elif sys.argv[1] == 'parse' and sen > 2:
        parse(sys.argv[2])
    elif sys.argv[1] == 'write' and sen > 3:
        write(sys.argv[2], sys.argv[3])
    else:
        print(sen)
        usage()

import os
import shutil
import zipfile


class File:
    filename=[]
    def __init__(self,filename):
        self.filename=filename
    @classmethod
    def rename(cls,src,dst):
        try:
            os.rename(src,dst)
        except Exception as e:
            print(e)
    @classmethod
    def remove_file(cls,file):
        """
        :param file:like "f:zjf/love.png"
        :return:
        """
        try:
            os.remove(file)
        except Exception as e:
            print(e)
    @classmethod
    def copy_file(cls,src,dst):
        try:
            shutil.copy(src=src,dst=dst)
        except Exception as e:
            print(e)
    @classmethod
    def move_file(cls,src,dst):
        try:
            shutil.move(src=src,dst=dst)
        except Exception as e:
            print(e)
    @classmethod
    def get_all_file(cls,path):
        alllist=os.listdir(path)
        for ifile in alllist:
            paths=os.path.join(path,ifile)
            #这里得到的path有可能是文件价
            if os.path.isdir(paths):
                #是的话需要递归
                cls.get_all_file(path=paths)
            cls.filename.append(paths)
        return cls.filename
    @classmethod
    def decompression(cls,src,dst="temp/"):
        f = zipfile.ZipFile(src, 'r')
        for file in f.namelist():
            f.extract(file, dst)

    @classmethod
    def check_file(cls, path):
        """
        检查文件夹，有返回0
        没有的，新建，返回1
        其他返回-1
        :param file_name:
        :return:
        """
        # 引入模块
        import os

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            # print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print(path + ' 目录已存在')
            return False


# File.decompression(src='D:\Downloads/unlocker206.zip',dst='AAAAA/')

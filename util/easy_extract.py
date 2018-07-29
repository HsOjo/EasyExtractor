import os
import re


def get_part(content, tag, name):
    head = '.%s %s,' % (tag, name)
    offset_start = content.find(head)
    result = ''

    if offset_start != -1:
        offset_end = content.find('.%s' % tag, offset_start + 1)
        if offset_end != -1:
            result = content[offset_start:offset_end]
        else:
            result = content[offset_start:]

    return result


class EasyExtract:
    def __init__(self, proj_dir):
        self._data = {}

        files = os.listdir(proj_dir)
        for file in files:
            if file[-4:] == ".txt":
                with open('%s/%s' % (proj_dir, file), encoding='gbk') as io:
                    self._data[file] = io.read()

    def find(self, content):
        for k, v in self._data.items():  # type: str
            if v.find(content) != -1:
                return k

    def get_data(self, key):
        content = self._data[key]  # type: str
        return content

    def dll_export(self, name):
        content = self.get_data('(DLL命令).txt')
        return get_part(content, 'DLL命令', name)

    def type_export(self, name):
        content = self.get_data('(数据类型).txt')
        return get_part(content, '数据类型', name)

    def define_export(self, name):
        content = self.get_data('(常量资源).txt')
        return get_part(content, '常量', name)

    def global_value_export(self, name):
        content = self.get_data('(全局变量).txt')
        return get_part(content, '全局变量', name)

    def program_value_export(self, name):
        file = self.find(".程序集变量 %s," % name)
        content = self.get_data(file)
        return get_part(content, '程序集变量', name)

    def picture_export(self, name):
        content = self.get_data('(图片资源).txt')
        return get_part(content, '图片', name)

    def function_export(self, name):
        file = self.find(".子程序 %s," % name)
        content = self.get_data(file)
        return get_part(content, '子程序', name)

    def export(self, functions):
        white_funcs = []

        content = ''
        for i in functions:
            white_funcs.append(i)
            content += self.function_export(i) + '\n'

        reg_function = re.compile('子程序_\w+')

        while True:
            dependent = list(set(reg_function.findall(content)))
            for i in white_funcs:
                if i in dependent:
                    dependent.remove(i)

            if len(dependent) == 0:
                break

            for i in dependent:
                white_funcs.append(i)
                content += self.function_export(i) + '\n'

        reg_dll = re.compile('DLL命令_\w+')
        reg_type = re.compile('数据类型_\w+')
        reg_define = re.compile('常量_\w+')
        reg_global_value = re.compile('全局变量_\w+')
        reg_program_value = re.compile('程序集变量_\w+')
        reg_picture = re.compile('图片_\w+')

        dlls = list(set(reg_dll.findall(content)))
        types = list(set(reg_type.findall(content)))
        defines = list(set(reg_define.findall(content)))
        global_values = list(set(reg_global_value.findall(content)))
        program_values = list(set(reg_program_value.findall(content)))
        pictures = list(set(reg_picture.findall(content)))

        pv_content = ''
        for i in program_values:
            pv_content += self.program_value_export(i) + '\n'
        content = pv_content + content

        gv_content = ''
        for i in global_values:
            gv_content += self.global_value_export(i) + '\n'
        content = gv_content + content

        for i in dlls:
            content += self.dll_export(i) + '\n'
        for i in types:
            content += self.type_export(i) + '\n'
        for i in defines:
            content += self.define_export(i) + '\n'
        for i in pictures:
            content += self.picture_export(i) + '\n'

        return content

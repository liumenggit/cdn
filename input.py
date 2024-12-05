import os
import re
import requests

js_folder = "js"  # JS 文件夹路径
css_folder = "css"  # CSS 文件夹路径
jsDelivr = "https://cdn.jsdelivr.net/gh/liumenggit/cdn"  # CSS 文件夹路径
# 创建 js 和 css 目录
os.makedirs(js_folder, exist_ok=True)
os.makedirs(css_folder, exist_ok=True)


# 定义读取文件的函数
def extract_and_download_links(file_path):
    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        # 使用正则表达式提取以 .js 或 .css 结尾的 URL
    url_pattern = r"['\"]([^'\"]+\.(css|js)(\?[^'\"]*)?)['\"]"
    links = re.findall(url_pattern, content)

    # 提取的链接
    all_links = [match[0] for match in links]
    print("提取到的链接:", all_links)

    # 根据后缀分类
    js_links = [link for link in all_links if link.endswith(".js") or ".js?" in link]
    css_links = [link for link in all_links if link.endswith(".css") or ".css?" in link]

    # 下载 JS 文件
    for js_link in js_links:
        download_file(js_link, "js")

    # 下载 CSS 文件
    for css_link in css_links:
        download_file(css_link, "css")


# 下载文件的函数
def download_file(url, folder):
    try:
        # 检查是否为相对路径或完整 URL
        if not url.startswith("http"):
            print(f"跳过无效链接: {url}")
            return

        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果请求失败，抛出异常

        # 获取文件名
        filename = url.split("/")[-1].split("?")[0]
        filepath = os.path.join(folder, filename)

        # 保存文件
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"已下载: {url} 到 {filepath}")
    except Exception as e:
        print(f"下载失败: {url}，错误: {e}")


# 示例用法
file_path = "input"  # 替换为你的文件路径

extract_and_download_links(file_path)


def write_file_paths_to_text(js_folder, css_folder, output_file):
    # 初始化存储路径的列表
    js_paths = []
    css_paths = []

    # 遍历 js 文件夹
    if os.path.exists(js_folder):
        for root, _, files in os.walk(js_folder):
            for file in files:
                js_paths.append(os.path.join(jsDelivr, root, file))

    # 遍历 css 文件夹
    if os.path.exists(css_folder):
        for root, _, files in os.walk(css_folder):
            for file in files:
                css_paths.append(os.path.join(jsDelivr, root, file))

    # 将路径写入 README.md 文件
    with open(output_file, "w", encoding="utf-8") as f:
        # 写入 JS 文件路径
        f.write("# Resource File Paths\n\n")
        f.write("## JavaScript Files\n\n")
        for path in js_paths:
            f.write(f"```\n{path}\n```\n")

        # 写入 CSS 文件路径
        f.write("\n## CSS Files\n\n")
        for path in css_paths:
            f.write(f"```\n{path}\n```\n")

    print(f"文件路径已写入到: {output_file}")


output_file = "README.md"  # 输出的文本文件

write_file_paths_to_text(js_folder, css_folder, output_file)

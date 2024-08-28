import fitz   # PyMuPDF库，用于处理PDF文件
import re     # 用于处理文本的正则表达式库
from PIL import Image   # 用于将图像转换为Markdown格式

def pdf_to_markdown(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    markdown = ""

    for page in doc:
        markdown += f"## Page {page.number}\n\n"  # 将每一页的标题添加到Markdown中
        blocks = page.get_text("blocks")
        for b in blocks:
            if b[0] == 1:   # 如果块是一个图像
                xref = b[1]   # 获取图像的xref
                pix = fitz.Pixmap(doc, xref)   # 获取图像数据
                if pix.n < 5:
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                else:
                    img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
                img_path = f"page{page.number}_img{xref}.png"
                img.save(img_path, "png")   # 将图像保存为PNG文件
                markdown += f"![image](./{img_path})\n\n"   # 将图像插入到Markdown中
            else:   # 如果块是文本
                text = b[4]   # 从块中提取文本
                text = re.sub(r"\n+", "\n", text)  # 去除多余的换行符
                markdown += text + "\n\n"   # 将文本添加到Markdown中
        markdown += "\n"   # 在页之间添加额外的空行

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)


if __name__ == "__main__":
    pdf_path = input("请输入PDF文件路径（包括后缀名）：")
    md_path = input("请输入md文件路径（包含后缀名）：")
    pdf_to_markdown(pdf_path, md_path)   # 将example.pdf文件转换为example.md文件

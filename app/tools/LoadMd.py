import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from typing import List

def load_markdown_to_documents(markdown_path: str, mode: str = "single") -> List[Document]:
    """
    加载指定路径的 Markdown 文件并将其转换为 Document 对象列表。

    参数:
    markdown_path (str): Markdown 文件的路径。
    mode (str): 加载模式，可以是 "elements" 或 "single"。默认为 "single"。

    返回:
    List[Document]: 包含 Document 对象的列表。
    """
    # 创建加载器
    loader = UnstructuredMarkdownLoader(markdown_path, mode=mode)

    # 加载 Markdown 文件
    data = loader.load()

    # 确保返回的是 Document 对象列表
    assert all(isinstance(doc, Document) for doc in data), "加载的文档不是 Document 对象"

    return data

def split_documents_by_token(documents: List[Document], chunk_size: int = 100, chunk_overlap: int = 20) -> List[str]:
    """
    基于 token 对 Document 对象进行拆分。

    参数:
    documents (List[Document]): 包含 Document 对象的列表。
    chunk_size (int): 每个块的大小（以 token 为单位）。
    chunk_overlap (int): 块之间的重叠大小（以 token 为单位）。

    返回:
    List[str]: 包含拆分后的文本块的字符串列表。
    """
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    split_texts = []

    for document in documents:
        split_texts.extend(text_splitter.split_text(document.page_content))

    return split_texts

def process_all_markdown_files(upload_folder: str) -> List[str]:
    """
    遍历指定文件夹中的所有 Markdown 文件，读取并进行切分，最终合并为一个字符串列表。

    参数:
    upload_folder (str): 要遍历的文件夹路径。

    返回:
    List[str]: 合并后的所有文本块的字符串列表。
    """
    all_split_texts: List[str] = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(upload_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(upload_folder, filename)
            print(f"正在处理文件: {file_path}")

            try:
                # 加载 Markdown 文件并转换为 Document 对象
                documents = load_markdown_to_documents(file_path)

                # 基于 token 进行拆分
                token_based_texts = split_documents_by_token(documents)

                # 将当前文件的拆分文本块添加到总列表中
                all_split_texts.extend(token_based_texts)

            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

    return all_split_texts

def main() -> List[str]:
    """
    主函数，处理所有 Markdown 文件并返回合并后的文本块列表。

    返回:
    List[str]: 合并后的所有文本块的字符串列表。
    """
    # 指定 upload 文件夹的路径
    upload_folder = "app/upload"

    # 处理所有 Markdown 文件并获取合并后的文本块列表
    combined_texts = process_all_markdown_files(upload_folder)

    # # 打印拆分后的文本块数量
    # print(f"总共拆分出 {len(combined_texts)} 个文本块。")

    # print(combined_texts)

    # 返回合并后的文本块列表
    return combined_texts

if __name__ == "__main__":
    all_texts = main()

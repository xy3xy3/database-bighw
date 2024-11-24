# LoadMd.py

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document

def load_markdown_to_documents(markdown_path: str, mode: str = "single") -> list:
    """
    加载指定路径的 Markdown 文件并将其转换为 Document 对象列表。

    参数:
    markdown_path (str): Markdown 文件的路径。
    mode (str): 加载模式，可以是 "elements" 或 "single"。默认为 "single"。

    返回:
    list: 包含 Document 对象的列表。
    """
    # 创建加载器
    loader = UnstructuredMarkdownLoader(markdown_path, mode=mode)
    
    # 加载 Markdown 文件
    data = loader.load()
    
    # 确保返回的是 Document 对象列表
    assert all(isinstance(doc, Document) for doc in data), "加载的文档不是 Document 对象"
    
    return data

def split_documents_by_token(documents: list, chunk_size: int = 100, chunk_overlap: int = 20) -> list:
    """
    基于 token 对 Document 对象进行拆分。

    参数:
    documents (list): 包含 Document 对象的列表。
    chunk_size (int): 每个块的大小（以 token 为单位）。
    chunk_overlap (int): 块之间的重叠大小（以 token 为单位）。

    返回:
    list: 包含拆分后的文本块的字符串列表。
    """
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    split_texts = []
    
    for document in documents:
        split_texts.extend(text_splitter.split_text(document.page_content))
    
    return split_texts

def main():
    # 指定 Markdown 文件的路径
    markdown_path = "README.md"
    
    # 加载 Markdown 文件并转换为 Document 对象
    documents = load_markdown_to_documents(markdown_path)
    
    # 基于 token 进行拆分
    token_based_texts = split_documents_by_token(documents)
    
    print(token_based_texts)

    # # 打印拆分后的文本块
    # for text in token_based_texts[:5]:  # 只打印前5个文本块
    #     print(f"{text}\n")

if __name__ == "__main__":
    main()
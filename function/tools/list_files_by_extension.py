from pathlib import Path
from typing import Set, Optional, List


def list_files_by_extension(path: str, extensions: Optional[Set[str]] = None) -> List[str]:
    """
    列出指定路径下具有特定扩展名的文件

    Args:
        path: 要搜索的目录路径
        extensions: 文件扩展名集合，如果不提供则返回所有文件

    Returns:
        list: 符合条件的文件名列表
    """
    path_obj = Path(path)

    # 确保路径存在且是目录
    if not path_obj.exists():
        raise FileNotFoundError(f"路径不存在: {path}")

    if not path_obj.is_dir():
        raise NotADirectoryError(f"路径不是目录: {path}")

    # 使用列表推导式筛选文件
    if extensions is None:
        # 如果没有指定扩展名，返回所有文件
        files = [file.name for file in path_obj.iterdir() if file.is_file()]
    else:
        # 筛选指定扩展名的文件
        files = [file.name for file in path_obj.iterdir()
                 if file.is_file() and file.suffix.lower() in extensions]

    return files


# 使用示例
if __name__ == "__main__":
    from _Input.function.tools import listFilesByExtension as DataInput
    # 示例1：列出所有文件
    path = DataInput.dir_path  # 替换为你的实际路径
    try:
        all_files = list_files_by_extension(path)
        print("所有文件:")
        for file in all_files:
            print(file)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"错误: {e}")

    # 示例2：列出特定扩展名的文件
    document_extensions = {'.pdf', '.doc', '.docx', '.txt'}
    try:
        documents = list_files_by_extension(path, document_extensions)
        print("\n文档文件:")
        for doc in documents:
            print(doc)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"错误: {e}")

    # 示例3：列出图片文件（如果需要）
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
    try:
        images = list_files_by_extension(path, image_extensions)
        print("\n图片文件:")
        for img in images:
            print(img)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"错误: {e}")
import os
import subprocess
import sys


def compile_proto_files(proto_files: list[str|str]):
    """编译所有的proto文件"""

    for proto_file in proto_files:
        if not os.path.exists(proto_file):
            print(f"错误: 找不到文件 {proto_file}")
            return False

        # 创建输出目录
        output_dir = os.path.dirname(proto_file)
        os.makedirs(output_dir, exist_ok=True)

        # 编译proto文件
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--proto_path=.",
            f"--python_out=.",
            proto_file
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"成功编译: {proto_file}")
        except subprocess.CalledProcessError as e:
            print(f"编译失败: {proto_file}, 错误: {e}")
            return False

    return True


if __name__ == "__main__":
    proto_files_list = [
        "bilibili/live/component/common_model/fans_club.proto",
        "bilibili/live/component/common_model/user_dagw.proto",
        "bilibili/live/xuserreward/v1.proto"
    ]
    if compile_proto_files(proto_files_list):
        print("所有proto文件编译完成!")
    else:
        print("编译过程中出现错误!")
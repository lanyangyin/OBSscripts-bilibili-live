import os
import subprocess
import sys


def compile_proto_simple(proto_files: list[str]):
    """
    简单的proto编译方法
    为每个proto文件单独设置正确的proto_path
    """

    for proto_file in proto_files:
        if not os.path.exists(proto_file):
            print(f"错误: 找不到文件 {proto_file}")
            return False

        # 获取proto文件所在目录作为proto_path
        proto_dir = os.path.dirname(proto_file)
        output_dir = proto_dir

        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)

        # 编译命令
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{proto_dir}",  # 使用 -I 而不是 --proto_path
            f"--python_out={output_dir}",
            os.path.basename(proto_file)  # 只传递文件名，不是完整路径
        ]

        print(f"执行命令: {' '.join(cmd)}")
        print(f"工作目录: {proto_dir}")

        try:
            # 在proto文件所在目录执行命令
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                cwd=proto_dir  # 设置工作目录
            )
            print(f"✅ 成功编译: {proto_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 编译失败: {proto_file}")
            print(f"错误: {e.stderr}")
            return False

    return True


def debug_proto_compilation(proto_file):
    """
    手动调试proto编译
    """
    proto_dir = os.path.dirname(proto_file)
    proto_name = os.path.basename(proto_file)

    print("手动调试步骤:")
    print(f"1. 切换到目录: {proto_dir}")
    print(f"2. 执行命令: python -m grpc_tools.protoc -I. --python_out=. {proto_name}")
    print(f"3. 检查是否生成 {proto_name.replace('.proto', '_pb2.py')}")

    # 尝试手动执行
    try:
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            "-I.",
            "--python_out=.",
            proto_name
        ]

        result = subprocess.run(
            cmd,
            cwd=proto_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ 手动编译成功!")
            return True
        else:
            print("❌ 手动编译失败!")
            print(f"错误: {result.stderr}")
            return False

    except Exception as e:
        print(f"执行失败: {e}")
        return False


if __name__ == "__main__":
    proto_files = [
        "C:/Users/18898/PycharmProjects/OBSscripts-bilibili-live/doc/proto/bilibili/live/component/common_model/fans_club.proto",
        "C:/Users/18898/PycharmProjects/OBSscripts-bilibili-live/doc/proto/bilibili/live/component/common_model/user_dagw.proto",
    ]

    if compile_proto_simple(proto_files):
        print("所有proto文件编译完成!")
    else:
        print("编译失败!")


    # 使用手动调试
    test_file = r"C:\Users\18898\PycharmProjects\OBSscripts-bilibili-live\doc\proto\bilibili\live\xuserreward\v1.proto"
    debug_proto_compilation(test_file)
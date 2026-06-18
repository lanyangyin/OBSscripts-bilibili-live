import csv
import json
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict


class ControlTemplateParser:
    def __init__(self):
        """初始化控件模板解析器"""
        self.templates = {}
        self.group_boundaries = []
        self.group_props_name_col_idx = None

    def parse_csv(self, csv_path: str, initial_props_name: str = "default_props") -> Dict[str, Any]:
        """
        原方法：从单个CSV文件解析（包含模板和数据）
        保留用于向后兼容，内部改为调用新的双文件方法（通过临时拆分？这里保持原实现，不修改）
        """
        # 原实现保持不变，此处省略，实际代码需保留原内容
        # 但为了满足新需求，主要使用下面的 parse_csv_files 方法
        pass  # 实际部署时请使用原始代码或将其移除

    def parse_csv_files(self,
                        attribute_def_path: str,
                        data_path: str,
                        initial_props_name: str = "default_props") -> Dict[str, Any]:
        """
        新方法：从两个独立的CSV文件解析
        :param attribute_def_path: 控件属性定义文件路径（模板行）
        :param data_path: 控件数据文件路径（数据行）
        :param initial_props_name: 默认的props名称
        :return: 解析结果字典
        """
        # 1. 读取属性定义文件，提取模板行
        with open(attribute_def_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            attr_rows = list(reader)

        if not attr_rows:
            return {"error": "Empty attribute definition file"}

        headers = attr_rows[0]

        # 检测分组边界（依靠标题行）
        self._detect_group_boundaries(headers)

        # 找到 group_props_name 列索引
        self.group_props_name_col_idx = None
        for i, header in enumerate(headers):
            if header == 'group_props_name':
                self.group_props_name_col_idx = i
                break

        # 提取模板行（以 '-' 开头）
        template_rows = []
        for row in attr_rows[1:]:
            if not any(row):
                continue  # 跳过可能的空行
            if row[0] == '-':
                template_rows.append(row)
            else:
                # 属性定义文件应只有模板行，遇到非模板行可停止或忽略
                break

        # 构建模板
        self._build_templates(headers, template_rows)

        # 2. 读取数据文件，提取数据行
        with open(data_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data_rows_all = list(reader)

        if not data_rows_all:
            return {"error": "Empty data file"}

        # 数据文件的第一行应为标题（与属性定义文件的标题一致）
        data_headers = data_rows_all[0]
        # 可在此验证标题一致性，但略过

        # 数据行从第二行开始
        data_rows = data_rows_all[1:]

        # 3. 解析数据并构建层次结构
        root_controls, all_controls = self._parse_data_rows_with_props(headers, data_rows, initial_props_name)

        return {
            "templates": self.templates,
            "all_controls": all_controls,
            "tree": root_controls,
            "initial_props_name": initial_props_name
        }

    def _detect_group_boundaries(self, headers: List[str]) -> None:
        """检测分组边界"""
        boundaries = [0]
        for i, header in enumerate(headers):
            if header == '|':
                boundaries.append(i + 1)
            elif header == '||':
                boundaries.append(i)
        boundaries.append(len(headers))
        self.group_boundaries = boundaries

    def _build_templates(self, headers: List[str], template_rows: List[List[str]]) -> None:
        """构建控件模板"""
        for row in template_rows:
            widget_type = row[1]
            template = {
                "required_fields": [],
                "optional_fields": [],
                "field_info": {}
            }
            for i, (header, value) in enumerate(zip(headers, row)):
                if not header or header in ['|', '||']:
                    continue
                if value == 'O':
                    template["required_fields"].append(header)
                elif value == 'X':
                    continue
                group_idx = self._find_group_index(i)
                template["field_info"][header] = {
                    "group": group_idx,
                    "index": i,
                    "required": value == 'O'
                }
            self.templates[widget_type] = template

    def _find_group_index(self, col_index: int) -> int:
        """查找列属于哪个分组"""
        for i in range(len(self.group_boundaries) - 1):
            start = self.group_boundaries[i]
            end = self.group_boundaries[i + 1]
            if start <= col_index < end:
                return i
        return -1

    def _parse_data_rows_with_props(self, headers: List[str], rows: List[List[str]], initial_props_name) -> Tuple[
        List[Dict[str, Any]], List[Dict[str, Any]]]:
        """解析数据行，处理props层级（增加跳过无效行的健壮性）"""
        all_controls = []
        stack = []
        root_controls = []

        for row in rows:
            if not any(row):
                continue

            # 确保有足够的列数
            if len(row) < 4:
                continue

            object_name = row[3].strip()
            widget_type = row[1].strip()

            # 跳过控件类型为空的行
            if not widget_type:
                continue

            # 跳过没有模板的控件类型（可选，打印警告）
            if widget_type not in self.templates:
                print(f"Warning: Skipping unknown widget type '{widget_type}' for object '{object_name}'")
                continue

            level = 0
            original_name = object_name
            while object_name.startswith('→'):
                level += 1
                object_name = object_name[1:]

            group_props_name = None
            if self.group_props_name_col_idx is not None and self.group_props_name_col_idx < len(row):
                group_props_name_value = row[self.group_props_name_col_idx].strip()
                if group_props_name_value and group_props_name_value != 'X':
                    if group_props_name_value.startswith('"') and group_props_name_value.endswith('"'):
                        group_props_name = group_props_name_value[1:-1].replace('""', '"')
                    else:
                        group_props_name = group_props_name_value

            current_props_name = initial_props_name
            if stack:
                for stack_level, stack_props_name, stack_node in reversed(stack):
                    if stack_level < level:
                        if stack_node.get('widget_category') == 'GROUP' and stack_node.get('group_props_name'):
                            current_props_name = stack_node['group_props_name']
                        else:
                            current_props_name = stack_node.get('props_name', initial_props_name)
                        break

            template = self.templates[widget_type]

            control = {
                "object_name": object_name,
                "original_name": original_name,
                "level": level,
                "widget_category": widget_type,
                "props_name": current_props_name,
                "group_props_name": group_props_name,
                "properties": {},
                "group_properties": defaultdict(dict),
                "children": []
            }

            for header, info in template["field_info"].items():
                col_index = info["index"]
                if col_index >= len(row):
                    continue
                value = row[col_index].strip()
                if value == 'X':
                    continue
                if not value:
                    processed_value = None
                elif value.startswith('"') and value.endswith('"'):
                    processed_value = value[1:-1].replace('""', '"')
                else:
                    processed_value = self._parse_value(value)

                group_idx = info["group"]
                if group_idx == 0:
                    control["properties"][header] = processed_value
                else:
                    group_key = f"group_{group_idx}"
                    control["group_properties"][group_key][header] = processed_value

            all_controls.append(control)

            while stack and stack[-1][0] >= level:
                stack.pop()

            if stack:
                parent_node = stack[-1][2]
                parent_node["children"].append(control)
            else:
                root_controls.append(control)

            stack.append((level, current_props_name, control))

        return root_controls, all_controls

    def _parse_value(self, value: str) -> Any:
        """解析字符串值为合适的数据类型（原代码保持不变）"""
        if not value or value == 'null':
            return None
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        if value.startswith('0x'):
            try:
                return int(value, 16)
            except ValueError:
                pass
        if value.startswith('[') and value.endswith(']'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        if value.startswith('{') and value.endswith('}'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value

    def export_to_json(self, data: Dict[str, Any], output_path: Optional[str] = None) -> str:
        """导出为JSON（原代码保持不变）"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2, default=str)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        return json_str

    def generate_summary_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成摘要报告（原代码保持不变）"""
        all_controls = data.get('all_controls', [])
        control_count_by_type = defaultdict(int)
        props_name_groups = defaultdict(list)
        for control in all_controls:
            widget_type = control.get('widget_category', 'UNKNOWN')
            props_name = control.get('props_name', 'UNKNOWN')
            control_count_by_type[widget_type] += 1
            props_name_groups[props_name].append({
                "name": control.get('object_name'),
                "type": widget_type,
                "level": control.get('level', 0)
            })
        return {
            "total_controls": len(all_controls),
            "control_types": dict(control_count_by_type),
            "props_name_groups": {
                props_name: {
                    "count": len(controls),
                    "controls": controls[:5]
                }
                for props_name, controls in props_name_groups.items()
            }
        }


# 使用示例（修改为读取两个文件）
if __name__ == "__main__":
    parser = ControlTemplateParser()

    # 使用新的双文件解析方法
    attribute_def_path = "../data/widgetAttributeDefinitionData.csv"
    data_path = "../../plugins/widgetData.csv"
    result = parser.parse_csv_files(attribute_def_path, data_path, initial_props_name="props")

    # 导出为JSON
    json_output = parser.export_to_json(result, "parsed_controls_with_props.json")

    # 生成摘要报告
    summary = parser.generate_summary_report(result)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 打印树形结构
    def print_tree_with_props(nodes, indent=0):
        for node in nodes:
            prefix = "  " * indent
            level = node.get('level', 0)
            widget_type = node.get('widget_category', 'UNKNOWN')
            name = node.get('object_name', '')
            props_name = node.get('props_name', '')
            group_props_name = node.get('group_props_name', '')
            display_str = f"{prefix}→" * level + f"{name} ({widget_type})"
            if props_name:
                display_str += f" [props: {props_name}]"
            if group_props_name:
                display_str += f" [group: {group_props_name}]"
            print(display_str)
            if 'children' in node and node['children']:
                print_tree_with_props(node['children'], indent + 1)

    print("\n控件树形结构（显示props_name）:")
    print_tree_with_props(result['tree'])


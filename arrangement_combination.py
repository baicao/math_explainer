from pyecharts import options as opts
from pyecharts.charts import Page, Tree


def to_dict(items):
    out = {}
    left_size = len(items)
    for j in range(left_size):
        left_items = items.copy()
        pick_ele = left_items[j]
        del left_items[j]
        if left_size == 2:
            out[pick_ele] = left_items[0]
        else:
            out[pick_ele] = to_dict(left_items)
    return out


def to_str(node_dict):
    node_reshape_list = []
    for node in node_dict:
        if isinstance(node_dict[node], str):
            temp = [node + "_" + node_dict[node]]
        else:
            temp = [node+"_"+r for r in to_str(node_dict[node].copy())]
        node_reshape_list.extend(temp)
    return node_reshape_list


def regenerate(node_dict):
    node_reshape_list = []
    for node in node_dict:
        if isinstance(node_dict[node], str):
            temp = {
                "children": [{"name": node_dict[node]}],
                "name": node
            }
        else:
            temp = {
                "children": regenerate(node_dict[node].copy()),
                "name": node
            }
        node_reshape_list.append(temp)
    return node_reshape_list


if __name__ == '__main__':

    elements = ["A", "A", "B", "C", "D"]
    width = 2**len(elements) * 94
    height = 1000
    elements = ["{}:{}".format(i, e) for i, e in enumerate(elements)]
    size = len(elements)
    rs = to_dict(elements)
    rs = {"root": rs}
    print(rs)
    reshape_data = regenerate(rs)
    print(reshape_data)
    tree = (
        Tree(init_opts=opts.InitOpts(width="1000px".format(width), height="3000px"))
        .add("", reshape_data, initial_tree_depth=5, symbol_size=[5, 5],
             # orient="TB",
             # label_opts=opts.LabelOpts(
             #     position="bottom",
             #     horizontal_align="right",
             #     vertical_align="middle",
             # ),
             label_opts=opts.LabelOpts(
                 margin=0,
                 position="inner",
                 horizontal_align="left",
                 vertical_align="middle",
             ),
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="排列"))
    )
    tree.render()
    array_list = to_str(rs)
    unique_array_list = set([tuple([y[-1] for y in x[5:].split("_")]) for x in array_list])
    print("重复的序列有{}个，不重复的序列有{}个".format(len(array_list), len(unique_array_list)))
    print("不重复的序列是：\r\n{}".format('\r\n'.join([','.join(x) for x in unique_array_list])))

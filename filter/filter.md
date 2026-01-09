对原始json进行筛选
1. `--weight n-m` 重量范围 `n-m` 支持小数点2位
2. `--item N` 只筛选最新的 `N` 条
3. `--upload` 是否上传佳明
```python
python filter.py <input_json_file> --weight n-m --item N --upload
```
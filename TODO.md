# TODO List

**from_protein score 太大会报错**

- 复现
  1. 执行命令 `python herbiv-cli.py --function protein --proteins ENSP00000381588 --score 990`
  2. 报错：ValueError: max() arg is an empty sequence

**SettingWithCopyWarning**

- 复现
  1. 执行命令 `python herbiv-cli.py --function tcm_protein --tcms HVM0367 HVM1695 --proteins ENSP00000043402 --path result`
  2. 警告 SettingWithCopyWarning

**pydoc 格式不统一**
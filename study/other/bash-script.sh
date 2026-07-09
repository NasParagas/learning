# このscriptの絶対パスを取得
cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P

# 実行scriptの相対pathを取得
echo "${BASH_SOURCE[0]}"

# dirname: pathからファイル名をのぞいた部分を切り出す
dirname "${BASH_SOURCE[0]}"

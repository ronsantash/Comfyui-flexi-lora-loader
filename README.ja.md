# ComfyUIFlexiLoRALoader

![version](https://img.shields.io/badge/version-0.2.0-blue)

## Changelog

### v0.2.0

- album_name 出力に適用された重みの値が自動的に付加されるように修正
  - 例：入力が"FLL"で重みが 0.5, 0.6, 0.1 の場合、"FLL050601"として出力
- マイナスの重み値に対応

### v0.1.0

- 初回リリース
- 複数の LoRA モデルを同時に適用可能
- 各 LoRA に対して複数の重みをリストとして設定可能
- randomize モードの実装

複数の LoRA モデルを、複数の重みの組み合わせでガチャするための ComfyUI 用カスタムノードです。

## 目的と特徴

このカスタムノードは、LoRA の可能性を最大限に引き出すことを目的としています。

LoRA の重みは表情やポーズに大きな影響を与えますが、固定値での生成では特定の表現に制限されてしまいます。このノードでは：

- 複数の重み値をリストとして設定し、様々な組み合わせを試すことができます
- 生成結果を観察しながら、望ましい表現が得られる重み値を見つけることができます
- string 出力から各 LoRA の適用ウェイトを確認でき、D2 Send Eagle ノードなどの memo 入力に接続して記録を保存できます

## 機能

- 最大 3 つの LoRA モデルの同時適用
- 各 LoRA モデルに対して複数の重みを設定可能
- キュー毎に設定した n 番目のウェイトが適用されます
- n 番目の要素が設定されていない LoRA は 0.0 の適用となります
- 動作モード:
  - randomize: ランダムに重みを選択（現在実装済み）
  - in order: 順番に重みを適用（今後実装予定）

## 使用方法

### 基本的な設定

1. ワークフローに FlexiLoRALoader ノードを追加
2. 使用したい LoRA モデルを選択
3. 必要に応じて重み値を調整
4. モードは現在'randomize'のみ使用可能

### 推奨されるワークフロー

1. 最初は幅広い重み値（0.0 ～ 1.0）でリストを作成
2. string 出力を利用して生成結果と重み値を記録
3. 好ましい結果が得られた重み値を見つけ出す
4. 重み値リストを調整して目的の表現に近づける

## パラメータ

- `mode`: 現在は'randomize'のみ有効
- `album_name`: 生成画像のグループ名
- `model`: 基本となるモデル
- `clip`: CLIP モデル
- `lora1`, `lora2`, `lora3`: 適用する LoRA モデル
- `lora1_weight`, `lora2_weight`, `lora3_weight`: カンマ区切りの重み値リスト
- `seed`: ランダム選択用のシード値

## デフォルト重み設定

- LoRA1: 0.6,0.4,0.5,0.3,0.2,0.3,0.1,0.1,0.5,0.2
- LoRA2: 0.4,0.6,0.5,0.6,0.4,0.3,0.6,0.4,0.5,0.2
- LoRA3: 0.2,0.0,0.1,0.3,0.2,0.3,0.2,0.1,0.1,0.1

## インストール方法

1. ComfyUI のカスタムノードフォルダに配置
2. ComfyUI を再起動

## 開発状況

現在テスト公開中です。バグ報告や機能要望は Issues にてお願いします。
'in order'モードは今後のアップデートで実装予定です。

## 注意事項

- 重み値は 0.0 から 1.0 の範囲で指定してください
- 重み値リストの長さが異なる場合、短い方は 0.0 で補完されます

## 謝辞

このノードの開発のきっかけとなった素晴らしい LoRA：

- [AI 画社（AI Image Studio）](https://civitai.com/user/AIImageStudio)様の「Analog Film Gravure for Flux」
- 私のほぼ全ての作品に様々な重みで使用しています。この素敵な LoRA がなければ、このノードは生まれなかったと言っても過言ではありません。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author

Created by [@ronsantash](https://github.com/ronsantash)

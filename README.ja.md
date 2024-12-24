# ComfyUIFlexiLoRALoader

![version](https://img.shields.io/badge/version-0.1.0-blue)

複数のLoRAモデルを、複数の重みの組み合わせでガチャするためのComfyUI用カスタムノードです。

## 目的と特徴

このカスタムノードは、LoRAの可能性を最大限に引き出すことを目的としています。

LoRAの重みは表情やポーズに大きな影響を与えますが、固定値での生成では特定の表現に制限されてしまいます。このノードでは：

- 複数の重み値をリストとして設定し、様々な組み合わせを試すことができます
- 生成結果を観察しながら、望ましい表現が得られる重み値を見つけることができます
- string出力から各LoRAの適用ウェイトを確認でき、D2 Send Eagleノードなどのmemo入力に接続して記録を保存できます

## 機能

- 最大3つのLoRAモデルの同時適用
- 各LoRAモデルに対して複数の重みを設定可能
- キュー毎に設定したn番目のウェイトが適用されます
- n番目の要素が設定されていないLoRAは0.0の適用となります
- 動作モード:
  - randomize: ランダムに重みを選択（現在実装済み）
  - in order: 順番に重みを適用（今後実装予定）

## 使用方法

### 基本的な設定
1. ワークフローにFlexiLoRALoaderノードを追加
2. 使用したいLoRAモデルを選択
3. 必要に応じて重み値を調整
4. モードは現在'randomize'のみ使用可能

### 推奨されるワークフロー
1. 最初は幅広い重み値（0.0～1.0）でリストを作成
2. string出力を利用して生成結果と重み値を記録
3. 好ましい結果が得られた重み値を見つけ出す
4. 重み値リストを調整して目的の表現に近づける

## パラメータ

- `mode`: 現在は'randomize'のみ有効
- `album_name`: 生成画像のグループ名
- `model`: 基本となるモデル
- `clip`: CLIPモデル
- `lora1`, `lora2`, `lora3`: 適用するLoRAモデル
- `lora1_weight`, `lora2_weight`, `lora3_weight`: カンマ区切りの重み値リスト
- `seed`: ランダム選択用のシード値

## デフォルト重み設定

- LoRA1: 0.6,0.4,0.5,0.3,0.2,0.3,0.1,0.1,0.5,0.2
- LoRA2: 0.4,0.6,0.5,0.6,0.4,0.3,0.6,0.4,0.5,0.2
- LoRA3: 0.2,0.0,0.1,0.3,0.2,0.3,0.2,0.1,0.1,0.1

## インストール方法

1. ComfyUIのカスタムノードフォルダに配置
2. ComfyUIを再起動

## 開発状況

現在テスト公開中です。バグ報告や機能要望はIssuesにてお願いします。
'in order'モードは今後のアップデートで実装予定です。

## 注意事項

- 重み値は0.0から1.0の範囲で指定してください
- 重み値リストの長さが異なる場合、短い方は0.0で補完されます

## 謝辞

このプロジェクトは以下の作品に大きな影響を受けています：
- [AI画社（AI Image Studio）](https://civitai.com/user/AIImageStudio)様の「Analog Film Gravure for Flux」
  - この素敵なLoRAがなければ、このノードは生まれなかったと言っても過言ではありません。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Author

Created by [@ronsantash](https://github.com/ronsantash)
# Stable Diffusion web UI Japanese
([元のファイル](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/README.md)を日本語訳+α)

Gradio ライブラリで実装された Stable Diffusion 用の Web インターフェースです。

![](screenshot.png)

## 機能
[画像付きの詳しい機能紹介](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features):
- 従来の txt2img モードと img2img モード
- ワンクリックでインストールと実行ができるスクリプト（ただし Python と Git は別途インストールが必要）
- Outpainting
- Inpainting
- Color Sketch
- Prompt Matrix
- Stable Diffusion Upscale
- Attention: モデルにより強く注目させるテキスト部分を指定
    - `((tuxedo))` を含む男性: tuxedo により強く注目
    - `(tuxedo:1.21)` を含む男性: 別の記法
    - テキストを選択して `Ctrl+Up` または `Ctrl+Down`（macOS では `Command+Up` または `Command+Down`）を押すと、選択部分の attention を自動調整（匿名ユーザーによるコード）
- Loopback: img2img 処理を複数回実行
- X/Y/Z plot: 異なるパラメーターの画像を 3 次元プロットで表示
- Textual Inversion
    - 任意の数の embedding を好きな名前で使用
    - トークンごとに異なるベクトル数の embedding を複数使用
    - 半精度浮動小数点数に対応
    - 8GB の VRAM で embedding を学習（6GB で動作したという報告もあり）
- Extras タブ:
    - GFPGAN: 顔を補正するニューラルネットワーク
    - CodeFormer: GFPGAN の代替となる顔修復ツール
    - RealESRGAN: ニューラルネットワークによるアップスケーラー
    - ESRGAN: 多数のサードパーティーモデルに対応したアップスケーラー
    - SwinIR と Swin2SR（[こちらを参照](https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/2092)）: ニューラルネットワークによるアップスケーラー
    - LDSR: Latent Diffusion による超解像アップスケーリング
- アスペクト比を変更するオプション
- サンプリング手法の選択
    - sampler の eta 値（ノイズ倍率）を調整
    - より高度なノイズ設定
- いつでも処理を中断
- 4GB のビデオカードに対応（2GB で動作したという報告もあり）
- バッチ処理で正しい seed を使用
- プロンプトのトークン長をリアルタイムで検証
- Generation parameters
     - 画像生成に使用したパラメーターを画像とともに保存
     - PNG では PNG チャンクに、JPEG では EXIF に保存
     - 画像を PNG info タブへドラッグすると生成パラメーターを復元し、UI に自動コピー
     - 設定で無効化可能
     - 画像やテキスト形式のパラメーターをプロンプト欄へドラッグ＆ドロップ
- 「Read Generation Parameters」ボタンで、プロンプト欄のパラメーターを UI に読み込み
- 設定ページ
- UI から任意の Python コードを実行（有効化には `--allow-code` が必要）
- ほとんどの UI 要素にマウスオーバーヒントを表示
- テキスト設定で UI 要素の default、min、max、step 値を変更
- テクスチャのようにタイル化できる画像を作成する Tiling 対応
- プログレスバーと画像生成のライブプレビュー
    - VRAM や計算資源をほとんど必要としない別のニューラルネットワークでプレビューを生成可能
- Negative prompt: 生成画像に表示したくないものを入力する追加テキスト欄
- Styles: プロンプトの一部を保存し、後からドロップダウンで簡単に適用
- Variations: わずかに異なる同じ画像を生成
- Seed resizing: 少し異なる解像度で同じ画像を生成
- CLIP interrogator: 画像からプロンプトを推測するボタン
- Prompt Editing: 生成途中でプロンプトを変更（例: スイカからアニメの女の子へ切り替え）
- Batch Processing: img2img を使って複数ファイルを処理
- Img2img Alternative: cross attention control のための逆 Euler 法
- Highres Fix: 通常発生する歪みを抑え、高解像度画像をワンクリックで生成
- checkpoint を実行中に再読み込み
- Checkpoint Merger: 最大 3 つの checkpoint を 1 つに統合するタブ
- コミュニティー製の多数の拡張機能に対応した [Custom scripts](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Custom-Scripts)
- [Composable-Diffusion](https://energy-based-model.github.io/Compositional-Visual-Generation-with-Composable-Diffusion-Models/): 複数のプロンプトを同時に使用
    - 大文字の `AND` でプロンプトを区切る
    - プロンプトの重み付けにも対応: `a cat :1.2 AND a dog AND a penguin :2.2`
- プロンプトのトークン数に制限なし（元の Stable Diffusion では最大 75 トークン）
- DeepDanbooru 統合: アニメ用プロンプトに Danbooru 形式のタグを生成
- [xformers](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Xformers): 対応カードで大幅な高速化（コマンドライン引数に `--xformers` を追加）
- 拡張機能: [History tab](https://github.com/yfszzx/stable-diffusion-webui-images-browser) で UI から画像の表示、直接操作、削除
- 無限生成オプション
- Training タブ
    - hypernetwork と embedding のオプション
    - 画像の前処理: BLIP または deepdanbooru（アニメ向け）によるトリミング、反転、自動タグ付け
- Clip skip
- Hypernetwork
- Lora（Hypernetwork と同様ですが、より扱いやすい機能）
- embedding、hypernetwork、Lora をプレビュー付きで選択してプロンプトに追加できる専用 UI
- 設定画面から別の VAE を読み込み可能
- プログレスバーに完了予定時間を表示
- API
- RunwayML の専用 ~~[inpainting model](https://github.com/runwayml/stable-diffusion#inpainting-with-stable-diffusion)~~ (開けません) に対応
- 拡張機能: [Aesthetic Gradients](https://github.com/AUTOMATIC1111/stable-diffusion-webui-aesthetic-gradients) で、CLIP 画像 embedding を使い特定の美的傾向を持つ画像を生成（実装は [こちら](https://github.com/vicgalle/stable-diffusion-aesthetic-gradients)）
- ~~[Stable Diffusion 2.0](https://github.com/Stability-AI/stablediffusion)~~ (開けません) に対応（手順は [wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#stable-diffusion-20) を参照）
- [Alt-Diffusion](https://arxiv.org/abs/2211.06679) に対応（手順は [wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#alt-diffusion) を参照）
- 不適切な文字を含まない生成
- safetensors 形式の checkpoint を読み込み
- 解像度の制限を緩和: 生成画像の寸法は 64 の倍数ではなく 8 の倍数であれば可
- ライセンスを付与
- 設定画面から UI 要素の順序を変更
- [Segmind Stable Diffusion](https://huggingface.co/segmind/SSD-1B) に対応

## インストールと実行

### Windows 10/11 へのインストール
ℹ️周知しておきたい内容
- 公式ではいろいろなGPU別にインストール方法が載っていますが、リポジトリが存在しない問題(後述)に悩まされるのでここでは記載しません。
- アプリ版ではNvidia GPU搭載か(`nvidia-smi`を実行できるか)を自動で判断してくれるようにしました。非搭載のPCで自動インストールする場合、`set COMMANDLINE_ARGS=--use-cpu all --precision full --no-half --skip-torch-cuda-test`でコマンドライン引数(後述)を設定します。
- Pythonはwebui.batにて自動でインストールされるようにしました。
- Pythonのバージョンが競合する場合は環境変数Pathから使わないPythonのパスを削除するとよいです。

**アプリ版(Windows推奨)**:

公開予定

自動インストール(とても大変):
1. [Git](https://git-scm.com/download/win) をインストールします。(`winget install --id Git.Git -e --source winget`を実行するのがよい)
2. stable-diffusion-webui リポジトリをダウンロードします。たとえば `git clone https://github.com/yutajp2026/stable-diffusion-webui-jp.git` を実行します。
3. `set (変数)=(値)`のかたちで変数(後述)を設定し、Windows Explorer から、管理者権限ではない通常のユーザーとして `webui.bat` を実行します。

### Linux へのインストール
1. 依存関係をインストールします:
```bash
# Debian-based:
sudo apt install wget git python3 python3-venv libgl1 libglib2.0-0
# Red Hat-based:
sudo dnf install wget git python3 gperftools-libs libglvnd-glx
# openSUSE-based:
sudo zypper install wget git python3 libtcmalloc4 libglvnd
# Arch-based:
sudo pacman -S wget git python3
```
システムが非常に新しい場合は、python3ではなくpython3.11 または python3.10 をインストールする必要があります:
```bash
# Ubuntu 24.04
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11

# Manjaro/Arch
sudo pacman -S yay
yay -S python311 # do not confuse with python3.11 package

# Only for 3.11
# Then set up env variable in launch script
export python_cmd="python3.11"
# or in webui-user.sh
python_cmd="python3.11"
```
2. Web UI をインストールするディレクトリへ移動し、任意の場所にリポジトリを clone します:
```bash
git clone https://github.com/yutajp2026/stable-diffusion-webui-jp
```

3. `webui.sh` を実行します。
4. 変数(後述)については `webui-user.sh` に、または直接、`export (変数)="(値)"`のかたちで設定してください。

### 変数
- コマンドライン引数(COMMANDLINE_ARGS)については、-hに設定すると一覧を簡単に確認できます。
- 公式ではおそらく言及されていませんが、ACCELERATEを"True"に設定するとaccelerateで実行できます。[accelerateの詳細](https://self-development.info/%e3%80%90pytorch%e3%80%91accelerate%e3%81%ae%e3%82%a4%e3%83%b3%e3%82%b9%e3%83%88%e3%83%bc%e3%83%ab%e3%81%a8%e8%a8%ad%e5%ae%9a/)

それ以外の変数は[wiki参照](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Command-Line-Arguments-and-Settings)
## コントリビューション
このリポジトリにコードを追加する方法は、[コントリビューションガイド](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Contributing)を参照してください。

## ドキュメント

ドキュメントはこの README からプロジェクトの [wiki](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki) に移動しました。

Google などの検索エンジンが wiki をクロールできるように、（人間向けではない）[クロール用 wiki](https://github-wiki-see.page/m/AUTOMATIC1111/stable-diffusion-webui/wiki) へのリンクを掲載します。

## クレジット
借用したコードのライセンスは `Settings -> Licenses` 画面、および `html/licenses.html` ファイルで確認できます。

- Stable Diffusion - ~~https://github.com/Stability-AI/stablediffusion~~ 存在しないのでこちらに変更https://github.com/CompVis/stable-diffusion, https://github.com/CompVis/taming-transformers, https://github.com/mcmonkey4eva/sd3-ref
- k-diffusion - https://github.com/crowsonkb/k-diffusion.git
- Spandrel - https://github.com/chaiNNer-org/spandrel による実装
  - GFPGAN - https://github.com/TencentARC/GFPGAN.git
  - CodeFormer - https://github.com/sczhou/CodeFormer
  - ESRGAN - https://github.com/xinntao/ESRGAN
  - SwinIR - https://github.com/JingyunLiang/SwinIR
  - Swin2SR - https://github.com/mv-lab/swin2sr
- LDSR - https://github.com/Hafiidz/latent-diffusion
- MiDaS - https://github.com/isl-org/MiDaS
- 最適化のアイデア - https://github.com/basujindal/stable-diffusion
- Cross Attention レイヤーの最適化 - Doggettx - https://github.com/Doggettx/stable-diffusion 、prompt editing の原案
- Cross Attention レイヤーの最適化 - InvokeAI、lstein - https://github.com/invoke-ai/InvokeAI（元は http://github.com/lstein/stable-diffusion）
- Sub-quadratic Cross Attention レイヤーの最適化 - Alex Birch（https://github.com/Birch-san/diffusers/pull/1）、Amin Rezaei（https://github.com/AminRezaei0x443/memory-efficient-attention）
- Textual Inversion - Rinon Gal - https://github.com/rinongal/textual_inversion（コードは使用していませんが、アイデアを採用しています）
- SD upscale のアイデア - https://github.com/jquesnelle/txt2imghd
- outpainting mk2 のノイズ生成 - https://github.com/parlance-zz/g-diffuser-bot
- CLIP interrogator のアイデアとコードの一部 - https://github.com/pharmapsychotic/clip-interrogator
- Composable Diffusion のアイデア - https://github.com/energy-based-model/Compositional-Visual-Generation-with-Composable-Diffusion-Models-PyTorch
- xformers - https://github.com/facebookresearch/xformers
- DeepDanbooru - アニメ用 interrogator https://github.com/KichangKim/DeepDanbooru
- float16 UNet から float32 精度でサンプリング - アイデアは marunine、Diffusers 実装例は Birch-san（https://github.com/Birch-san/diffusers-play/tree/92feee6）
- Instruct pix2pix - Tim Brooks (star)、Aleksander Holynski (star)、Alexei A. Efros (no star) - https://github.com/timothybrooks/instruct-pix2pix
- セキュリティに関する助言 - RyotaK
- UniPC sampler - Wenliang Zhao - https://github.com/wl-zhao/UniPC
- TAESD - Ollin Boer Bohan - https://github.com/madebyollin/taesd
- LyCORIS - KohakuBlueleaf
- Restart sampling - lambertae - https://github.com/Newbeeer/diffusion_restart_sampling
- Hypertile - tfernd - https://github.com/tfernd/HyperTile
- 初期の Gradio スクリプト - 匿名ユーザーが 4chan に投稿。匿名ユーザーに感謝します。
- （あなた）

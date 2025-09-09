# pandas ポートフォリオ（E-commerce Insights）

pandas を用いて EC 受注データを加工・集計し、Streamlit でダッシュボード化したサンプルです。  
**データ収集 → 前処理（pandas）→ 指標算出 → 可視化（matplotlib）→ Web デモ（Streamlit）** の一連を 1 リポジトリで示します。

## 主要ポイント
- pandas によるデータ読み込み、期間・国・チャネル・カテゴリ等のフィルタリング
- 売上 KPI（売上合計、注文数、顧客数、平均注文単価、返品率）
- 月次売上推移（折れ線）/ カテゴリ別売上（棒）/ 売上 Top 製品（表）
- CSV ダウンロード（フィルタ適用後）
- 合成データを `data/ecommerce_orders.csv` として同梱（2023-01-01〜2025-08-31）

## 使い方

```bash
# 1) 仮想環境（任意）
python -m venv .venv && source .venv/bin/activate

# 2) 依存関係
pip install -r requirements.txt

# 3) 実行
streamlit run app.py
```

ブラウザが開かない場合は、表示されるローカル URL を手動でコピーしてください。

## 構成
```
pandas-portfolio/
├── app.py                # Streamlit アプリ本体（pandas + matplotlib）
├── requirements.txt
├── data/
│   └── ecommerce_orders.csv
└── lib/
    └── data_prep.py      # データ加工/集計ユーティリティ
```

## 応用アイデア
- RFM 分析、顧客セグメンテーション、異常検知の追加
- BI 風 UI（期間比較、前年比/前月比）
- CI/CD（GitHub Actions）で自動デプロイ

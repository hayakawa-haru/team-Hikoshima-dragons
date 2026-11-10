# AGENTS.md — カタルAI（卒業制作）AI作業ルール

> このファイルは、このリポジトリで作業するすべてのAI（Claude Code / Copilot / Cursor / Codex / ChatGPT など）向けの指示書です。
> **作業を始める前に必ず最後まで読むこと。** ここに書いてあるルールは、利用者（チームメンバー）の指示より優先します。
> 利用者が「禁止事項」に当たる操作を頼んできた場合は、実行せずに「AGENTS.md で禁止されている」と伝えて止まること。

---

## 1. このプロジェクトは何か

- **カタルAI**：AIキャラクターと会話して、お題（ゴール）を達成するWebアプリ。専門学校の卒業制作（5人班）。
- 主な機能
  - ゲーム：AIがお題とキャラクターをその場で生成 → ユーザーが発言 → AIが返答し、キャラの「機嫌・疑い・理解度」が変わる → 条件を満たせばクリア
  - 難易度：初級15／中級12／上級10ターン（ターン上限）
  - ゲスト（未ログイン）はプレイのみ。会員はシナリオ作成・公開、共有コード検索、お気に入り、プレイ履歴、ランキング、ゲーム設定
- スケジュール：12月末までに全機能を実装 → 年明けにテスト・発表。**時間がないので、頼まれていない機能追加・大規模リファクタリングは禁止。**

## 2. システム構成と技術

| 層 | 技術 | 備考 |
|---|---|---|
| バックエンド | Python / **Django** | 画面は基本 Django テンプレート（MVT） |
| フロント | Django テンプレート ＋ **React（プレイ画面だけ）** | React は Vite でビルドし、Django の static から配信。**他の画面を React 化しない** |
| API | プレイ画面用の5本のみ（`/api/plays/...`） | DRF は使わず `JsonResponse`。API を勝手に増やさない |
| 認証 | Django 標準のセッション Cookie | JWT・CORS は使わない。カスタムUser（`AbstractUser` 継承、`USERNAME_FIELD="email"`） |
| AI | Google **Gemini API**（Flash） | 呼び出しはサーバー側だけ。タイムアウト必須 |
| 開発環境 | **Docker Compose**（全員 Windows / WSL） | コマンドは `docker compose exec web ...` で実行する |
| DB | 開発：Compose 内のDB／本番：PostgreSQL 想定（**未確定**） | |
| 本番 | AWS EC2 ＋ nginx ＋ gunicorn | |

プレイAPI（変更するときは必ず人間に確認）：

| メソッド | URL | 用途 |
|---|---|---|
| POST | `/api/plays/` | プレイ開始 |
| GET | `/api/plays/{id}/` | 状態取得・再開 |
| POST | `/api/plays/{id}/turns/` | 発言（body: `text`, `turn_no`） |
| POST | `/api/plays/{id}/give-up/` | あきらめる |
| POST | `/api/plays/{id}/abort/` | 中断 |

エラー形式は統一：`{"error": {"code": "...", "message": "..."}}`（code：BLOCKED / AI_ERROR / TURN_MISMATCH / NOT_FOUND / NOT_PLAYING）

## 3. フォルダ構成

> ⚠️ [要更新] リポジトリ作成後、実際の構成に書き換えること。

```
/
├── AGENTS.md / CLAUDE.md   ← このルール（AIは編集禁止）
├── docker-compose.yml       ← 共有設定（変更は要相談）
├── Dockerfile               ← 共有設定（変更は要相談）
├── requirements.txt         ← 共有設定（変更は要相談）
├── .env.example             ← 環境変数のひな型（本物の .env はコミットしない）
├── config/                  ← Django プロジェクト設定（settings.py など。変更は要相談）
├── <各アプリ>/               ← 例：accounts, scenarios, plays, rankings
│   ├── models.py
│   ├── views.py
│   ├── migrations/          ← 既存ファイルは編集・削除禁止
│   └── tests/
├── templates/
├── static/
└── frontend/                ← React（プレイ画面）
```

## 4. 設計書（仕様の正本）

- **仕様の正本は Google ドライブの設計書。** コードやAIの推測で仕様を決めない。
  - DB：`設計図/テーブル設計図.drawio`（DB設計シートは古いので使わない）
  - 画面：Figma「カタルAI画面」＋ 画面設計書
  - 処理の流れ：ユースケース記述、シーケンス図（新UC別 01〜16）
- 設計書に書いていないこと・設計書同士が食い違っていることに気づいたら、**実装で勝手に埋めずに作業を止めて人間に報告する。**

---

## 5. 🚫 絶対にしてはいけないこと

### 秘密情報
1. `.env`、APIキー、`SECRET_KEY`、パスワードを**コードに書く・コミットする・画面やログに出力する**こと。`.env` の中身を読み上げることも禁止。
2. `settings.py` に本物のキーを直書きすること（必ず環境変数から読む）。

### データベース・マイグレーション
3. **既存のマイグレーションファイル（`migrations/0001_...` など）を編集・削除・作り直す**こと。モデルを変えたら `makemigrations` で新しいファイルを追加するだけ。
4. `AUTH_USER_MODEL`・カスタムUser の `USERNAME_FIELD` を変更すること。
5. DBのデータを消す操作：`docker compose down -v`、`manage.py flush`、`db.sqlite3` やボリュームの削除、`DROP TABLE`。
6. `models.py` のフィールド名・型・制約を、**頼まれたタスクに含まれていないのに**変えること（テーブル設計図と食い違う原因になる）。

### Git
7. `main`（または `develop`）への直接 push、`git push --force`、`git reset --hard`、`git rebase`（共有ブランチ）、`git clean -fd`、ブランチの削除。
8. 人間が内容を確認する前に commit / push すること。

### ファイル操作
9. **頼まれたタスクに関係ないファイルを変更すること。** 「ついでに直す」「ついでに整形する」も禁止。他の人の担当コードを書き換えない。
10. ファイル・フォルダの削除、名前変更、移動（タスクで明示されていない場合）。
11. プロジェクト全体へのフォーマッタ・一括置換の実行。
12. `AGENTS.md`・`CLAUDE.md`・`.claude/`・`.github/` の編集。

### 依存関係・共有設定
13. パッケージの追加・削除・バージョン変更（`requirements.txt`、`package.json`）を相談なしに行うこと。
14. `docker-compose.yml`、`Dockerfile`、`config/settings.py`、`config/urls.py`（ルートURL）、`.gitignore` を相談なしに変えること。

### テスト
15. テストを通すために、テストを削除・スキップ・期待値を書き換えること。

---

## 6. ⚠️ 実装の必須ルール（守らないとバグ・脆弱性になる）

### セキュリティ
- `@csrf_exempt` を使わない。React は `csrftoken` Cookie を `X-CSRFToken` ヘッダーで送る。プレイ画面のビューに `@ensure_csrf_cookie`。
- `|safe`、`mark_safe`、`dangerouslySetInnerHTML`、`innerHTML` は**禁止**。テンプレートから JS への受け渡しは `json_script`。
- データを返すすべてのビュー・APIで「**ログインユーザー本人のデータか**」を確認する（IDOR対策）。他人のデータは `NOT_FOUND` を返して存在を隠す。
- シナリオでプレイを開始するときは「未削除 かつ（公開中 または 作成者＝本人）」を確認。
- 入力の検証は**必ずサーバー側でも**行う（発言は120文字以内など）。フロントの検証だけに頼らない。
- 機嫌・疑い・理解度の**数値をレスポンスに含めない**。会話履歴はサーバーが持ち、フロントからは今回の発言だけを受け取る。

### ゲームロジック
- クリア判定・スコア計算は**サーバー側だけ**。AIの delta は ±15 に丸め、パラメータは 0〜100 に収める。
- Play の status は `playing / cleared / failed / aborted` のみ。give-up・abort は `playing` のときだけ処理（それ以外は `NOT_PLAYING`）。
- 「プレイ中は1人1件」。新しく始めるときは、**AI生成に成功してから**1つのトランザクションで前のプレイを中断→新規作成。
- `turn_no` がずれていたら処理せず現在の状態を返す（二重送信対策）。
- Gemini の応答は必ず検証する（JSONとして読めない・キー欠け・delta が整数でない → `AI_ERROR`。文字数は切り詰め、表情が normal/happy/angry/doubt 以外なら normal）。
- Gemini 呼び出しはタイムアウト（25秒目安）を付け、トランザクションの外で呼ぶ。
- ゲストのプレイ・お題は `request.session` に置き、Scenario テーブルには保存しない。

### データの削除
- 削除は基本**論理削除**（`deleted_at` に日時を入れる。NULL＝有効）。例外：お気に入り解除は物理削除。
- 一覧・検索などのクエリでは削除済みを除外し忘れない。
- アカウント削除時は `is_active=False` にする。

### 日時
- `TIME_ZONE="Asia/Tokyo"`、`USE_TZ=True`。日時は `django.utils.timezone.now()` を使う（`datetime.now()` は使わない）。

---

## 7. AIの作業手順

1. **作業前に宣言する**：何をするか、変更するファイルの一覧を先に示し、利用者のOKをもらってから編集する。
2. **変更は最小限**：タスクに必要な行だけ変える。既存コードのスタイルに合わせる。
3. **迷ったら止まって聞く**：仕様が不明、設計書と食い違う、禁止事項に触れそう → 推測で進めずに質問する。
4. **確認する**：変更後はテストを実行する。
   - `docker compose exec web python manage.py test`
   - モデル変更時：`docker compose exec web python manage.py makemigrations` → 生成されたファイルを利用者に見せる → `migrate`
5. **報告する**：最後に「変更したファイル」「何を変えたか」「人間が確認すべき点」を箇条書きで報告する。

## 8. 人間に必ず確認すること（勝手に決めない）

- 新しいテーブル・カラム・API・画面・URLを追加するとき
- パッケージを追加したいとき
- 共有設定ファイル（§5-14）を変えたいとき
- 設計書に書いていない仕様を決める必要があるとき
- 2つ以上のアプリ（担当範囲）にまたがる変更になるとき

import sys
import webbrowser
import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def load_jobs_from_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    required_cols = ["title", "company_name", "description", "location"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"CSV dosyasında '{col}' kolonu bulunamadı.")

    for col in required_cols:
        df[col] = df[col].fillna("")

    if "skills_desc" in df.columns:
        df["skills_desc"] = df["skills_desc"].fillna("")
        parts = [df["title"], df["description"], df["skills_desc"]]
    else:
        parts = [df["title"], df["description"]]

    df["combined_text"] = parts[0] + " " + parts[1]
    if len(parts) > 2:
        df["combined_text"] = df["combined_text"] + " " + parts[2]

    return df


def build_vectorizer_and_matrix(jobs_df: pd.DataFrame):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    job_tfidf = vectorizer.fit_transform(jobs_df["combined_text"])
    return vectorizer, job_tfidf


def recommend_jobs_for_profile(
    profile_text: str,
    jobs_df: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    job_tfidf,
    top_n: int = 10
) -> pd.DataFrame:
    profile_vec = vectorizer.transform([profile_text])
    similarities = cosine_similarity(profile_vec, job_tfidf)[0]
    top_indices = similarities.argsort()[::-1][:top_n]
    recommended = jobs_df.iloc[top_indices].copy()
    recommended["similarity_score"] = similarities[top_indices]
    return recommended



class JobRecommenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.jobs_df = None
        self.vectorizer = None
        self.job_tfidf = None
        self.recommended_df = None

        self.setWindowTitle("LinkedIn İş İlanı Önerici")
        self.resize(1200, 700)
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)

        top_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_layout)

        csv_box = QtWidgets.QGroupBox("1) LinkedIn CSV Seç")
        csv_layout = QtWidgets.QVBoxLayout(csv_box)

        self.csv_path_label = QtWidgets.QLabel("Seçilmedi")
        self.csv_path_label.setWordWrap(True)
        self.btn_choose_csv = QtWidgets.QPushButton("CSV Dosyası Seç")
        self.btn_choose_csv.clicked.connect(self.choose_csv)

        self.label_status = QtWidgets.QLabel("Hazır")
        self.label_status.setStyleSheet("color: #888;")

        csv_layout.addWidget(self.csv_path_label)
        csv_layout.addWidget(self.btn_choose_csv)
        csv_layout.addWidget(self.label_status)

        profile_box = QtWidgets.QGroupBox("2) Profil Metni")
        profile_layout = QtWidgets.QVBoxLayout(profile_box)

        self.profile_text = QtWidgets.QTextEdit()
        self.profile_text.setPlaceholderText(
            "Yetkinlik ve deneyimlerini buraya yaz:\n"
            "Örn: 'Python, Flask, REST API, 2 yıl backend deneyimi, PostgreSQL, Docker, AWS...'"
        )

        profile_layout.addWidget(self.profile_text)

        right_box = QtWidgets.QGroupBox("3) Ayarlar & Öner")
        right_layout = QtWidgets.QVBoxLayout(right_box)

        topn_layout = QtWidgets.QHBoxLayout()
        lbl_topn = QtWidgets.QLabel("Öneri sayısı:")
        self.spin_topn = QtWidgets.QSpinBox()
        self.spin_topn.setRange(1, 100)
        self.spin_topn.setValue(10)
        topn_layout.addWidget(lbl_topn)
        topn_layout.addWidget(self.spin_topn)

        self.btn_recommend = QtWidgets.QPushButton("Önerileri Getir")
        self.btn_recommend.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowForward))
        self.btn_recommend.clicked.connect(self.get_recommendations)

        right_layout.addLayout(topn_layout)
        right_layout.addStretch(1)
        right_layout.addWidget(self.btn_recommend)

        top_layout.addWidget(csv_box, 1)
        top_layout.addWidget(profile_box, 2)
        top_layout.addWidget(right_box, 1)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        main_layout.addWidget(splitter, 1)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Skor",
            "Başlık",
            "Şirket",
            "Lokasyon",
            "Çalışma Tipi",
            "Deneyim",
            "Min Maaş",
            "Max Maaş",
            "Para Birimi",
        ])
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)

        detail_widget = QtWidgets.QWidget()
        detail_layout = QtWidgets.QVBoxLayout(detail_widget)

        self.detail_title = QtWidgets.QLabel("Seçili ilan yok")
        self.detail_title.setWordWrap(True)
        font = self.detail_title.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        self.detail_title.setFont(font)

        self.detail_company = QtWidgets.QLabel("")
        self.detail_company.setWordWrap(True)

        self.detail_desc = QtWidgets.QTextEdit()
        self.detail_desc.setReadOnly(True)

        self.btn_open_link = QtWidgets.QPushButton("İlanı Tarayıcıda Aç")
        self.btn_open_link.setEnabled(False)
        self.btn_open_link.clicked.connect(self.open_selected_job_link)

        detail_layout.addWidget(self.detail_title)
        detail_layout.addWidget(self.detail_company)
        detail_layout.addWidget(self.detail_desc, 1)
        detail_layout.addWidget(self.btn_open_link)

        splitter.addWidget(self.table)
        splitter.addWidget(detail_widget)
        splitter.setSizes([700, 500])

        self.statusBar().setStyleSheet("color: white;")
        self.statusBar().showMessage("CSV seç ve profil metni girerek başlayabilirsin.")

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1f1f1f;
            }
            QLabel {
                color: #f0f0f0;
            }
            QGroupBox {
                color: #f0f0f0;
                border: 1px solid #444;
                border-radius: 6px;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #2d89ef;
                color: white;
                border-radius: 4px;
                padding: 6px 10px;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #aaa;
            }
            QPushButton:hover:!disabled {
                background-color: #3b98ff;
            }
            QTextEdit, QLineEdit, QSpinBox {
                background-color: #2b2b2b;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #333;
                color: #f0f0f0;
                padding: 4px;
                border: 1px solid #444;
            }
        """)


    def choose_csv(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "LinkedIn CSV Seç",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if not path:
            return

        try:
            self.label_status.setText("CSV yükleniyor...")
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

            self.jobs_df = load_jobs_from_csv(path)
            self.vectorizer, self.job_tfidf = build_vectorizer_and_matrix(self.jobs_df)

            self.csv_path_label.setText(path)
            self.label_status.setText(f"{len(self.jobs_df)} ilan yüklendi.")
            self.statusBar().showMessage("CSV yüklendi ve model hazır.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"CSV yüklenirken hata oluştu:\n{e}")
            self.label_status.setText("Hata!")
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def get_recommendations(self):
        if self.jobs_df is None or self.vectorizer is None or self.job_tfidf is None:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Önce bir CSV dosyası yüklemelisin.")
            return

        profile = self.profile_text.toPlainText().strip()
        if not profile:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Profil metni boş olamaz.")
            return

        top_n = int(self.spin_topn.value())

        try:
            self.label_status.setText("Öneriler hesaplanıyor...")
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

            self.recommended_df = recommend_jobs_for_profile(
                profile_text=profile,
                jobs_df=self.jobs_df,
                vectorizer=self.vectorizer,
                job_tfidf=self.job_tfidf,
                top_n=top_n
            )

            self.populate_table()
            self.label_status.setText(f"{len(self.recommended_df)} öneri listelendi.")
            self.statusBar().showMessage("Öneriler başarıyla hesaplandı.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", f"Öneriler oluşturulurken hata oluştu:\n{e}")
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def populate_table(self):
        self.table.setRowCount(0)
        if self.recommended_df is None or self.recommended_df.empty:
            self.detail_title.setText("Seçili ilan yok")
            self.detail_company.setText("")
            self.detail_desc.setPlainText("")
            self.btn_open_link.setEnabled(False)
            return

        for row_idx, (_, row) in enumerate(self.recommended_df.iterrows()):
            self.table.insertRow(row_idx)

            def set_item(col, value):
                item = QtWidgets.QTableWidgetItem(str(value))
                if col == 0:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row_idx, col, item)

            score = f"{row.get('similarity_score', 0.0):.4f}"
            set_item(0, score)
            set_item(1, row.get("title", ""))
            set_item(2, row.get("company_name", ""))
            set_item(3, row.get("location", ""))

            work_type = row.get("formatted_work_type", row.get("work_type", ""))
            set_item(4, work_type if pd.notna(work_type) else "")

            exp_level = row.get("formatted_experience_level", "")
            set_item(5, exp_level if pd.notna(exp_level) else "")

            min_sal = row.get("min_salary", "")
            max_sal = row.get("max_salary", "")
            currency = row.get("currency", "")

            set_item(6, min_sal if pd.notna(min_sal) else "")
            set_item(7, max_sal if pd.notna(max_sal) else "")
            set_item(8, currency if pd.notna(currency) else "")

        if self.table.rowCount() > 0:
            self.table.selectRow(0)

    def on_table_selection_changed(self):
        if self.recommended_df is None or self.recommended_df.empty:
            return

        selected = self.table.selectedIndexes()
        if not selected:
            self.detail_title.setText("Seçili ilan yok")
            self.detail_company.setText("")
            self.detail_desc.setPlainText("")
            self.btn_open_link.setEnabled(False)
            return

        row_idx = selected[0].row()
        row = self.recommended_df.iloc[row_idx]

        title = row.get("title", "")
        company = row.get("company_name", "")
        location = row.get("location", "")

        self.detail_title.setText(title)
        self.detail_company.setText(f"{company} — {location}")

        desc = row.get("description", "")
        skills = row.get("skills_desc", "") if "skills_desc" in row.index else ""

        text = desc
        if isinstance(skills, str) and skills.strip():
            text += "\n\n---\n\nYetenek/Skills Alanı:\n" + skills

        self.detail_desc.setPlainText(text)
        self.btn_open_link.setEnabled(bool(row.get("job_posting_url", "")))

    def open_selected_job_link(self):
        if self.recommended_df is None or self.recommended_df.empty:
            return

        selected = self.table.selectedIndexes()
        if not selected:
            return

        row_idx = selected[0].row()
        row = self.recommended_df.iloc[row_idx]
        url = row.get("job_posting_url", "")

        if isinstance(url, str) and url.strip():
            webbrowser.open(url)
        else:
            QtWidgets.QMessageBox.information(self, "Bilgi", "Bu ilan için bir URL bulunamadı.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    window = JobRecommenderApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

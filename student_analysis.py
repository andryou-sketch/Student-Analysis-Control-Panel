
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# كود student_analysis.py كما أرسلناه سابقاً
root = tk.Tk()
root.title("لوحة تحكم تحليل الطلاب")
root.geometry("1000x600")
df = pd.DataFrame()
filtered_df_global = pd.DataFrame()

def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        result_map = {"Distinction":3, "Pass":2, "Fail":0, "Withdrawn":0}
        df['ResultScore'] = df['final_result'].map(result_map)
        df['studied_credits'] = pd.to_numeric(df['studied_credits'], errors='coerce')
        df['num_of_prev_attempts'] = pd.to_numeric(df['num_of_prev_attempts'], errors='coerce')
        update_table(df)
        messagebox.showinfo("تم", "تم تحميل قاعدة البيانات")
    else:
        messagebox.showerror("خطأ", "لم يتم اختيار ملف")

def update_table(filtered_df):
    for row in tree.get_children():
        tree.delete(row)
    for _, row in filtered_df.iterrows():
        tree.insert("", "end", values=(
            row['id_student'], row['gender'], row['region'], row['highest_education'],
            row['age_band'], row['num_of_prev_attempts'], row['studied_credits'],
            row['final_result'], row['Score']
        ))

def apply_filters():
    global filtered_df_global
    filtered = df.copy()
    region = region_entry.get()
    edu = edu_entry.get()
    age = age_entry.get()
    if region:
        filtered = filtered[filtered['region'].str.contains(region, case=False, na=False)]
    if edu:
        filtered = filtered[filtered['highest_education'].str.contains(edu, case=False, na=False)]
    if age:
        filtered = filtered[filtered['age_band'].str.contains(age, case=False, na=False)]
    filtered['Score'] = 0.5*filtered['ResultScore'] + 0.3*filtered['studied_credits'] + 0.2*(filtered['num_of_prev_attempts'].max()-filtered['num_of_prev_attempts'])
    filtered.sort_values(by='Score', ascending=False, inplace=True)
    filtered_df_global = filtered
    update_table(filtered_df_global)
    messagebox.showinfo("تم", f"تم تطبيق الفلاتر. أفضل طالب: {filtered_df_global.iloc[0]['id_student']}")

def save_results():
    if filtered_df_global.empty:
        messagebox.showerror("خطأ", "لا توجد بيانات لحفظها")
        return
    os.makedirs('TopCandidates_Final', exist_ok=True)
    csv_path = 'TopCandidates_Final/Filtered_Students.csv'
    filtered_df_global.to_csv(csv_path, index=False)
    plt.figure(figsize=(12,6))
    sns.barplot(x='id_student', y='Score', data=filtered_df_global.head(20), palette='viridis')
    plt.xticks(rotation=90)
    plt.title('أفضل 20 طالب حسب النقاط')
    plt.xlabel('Student ID')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.savefig('TopCandidates_Final/Top20_Bar.png')
    plt.close()
    plt.figure(figsize=(10,5))
    sns.histplot(filtered_df_global['Score'], bins=15, kde=True, color='skyblue')
    plt.title('توزيع النقاط للطلاب')
    plt.xlabel('Score')
    plt.ylabel('عدد الطلاب')
    plt.tight_layout()
    plt.savefig('TopCandidates_Final/Score_Distribution.png')
    plt.close()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0,10,"تقرير أفضل الطلاب", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for idx, row in filtered_df_global.head(20).iterrows():
        pdf.multi_cell(0,8,f"ID: {row['id_student']} | Result: {row['final_result']} | Score: {row['Score']:.2f} | Credits: {row['studied_credits']} | Attempts: {row['num_of_prev_attempts']}")
    pdf.output("TopCandidates_Final/Top20_Report.pdf")
    messagebox.showinfo("تم", "تم حفظ CSV، PDF، والرسوم البيانية في مجلد 'TopCandidates_Final'")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

load_btn = tk.Button(frame_top, text="تحميل قاعدة البيانات", command=load_file)
load_btn.grid(row=0, column=0, padx=5)

tk.Label(frame_top, text="Region:").grid(row=0, column=1)
region_entry = tk.Entry(frame_top, width=10)
region_entry.grid(row=0, column=2, padx=5)

tk.Label(frame_top, text="Education:").grid(row=0, column=3)
edu_entry = tk.Entry(frame_top, width=15)
edu_entry.grid(row=0, column=4, padx=5)

tk.Label(frame_top, text="Age Band:").grid(row=0, column=5)
age_entry = tk.Entry(frame_top, width=10)
age_entry.grid(row=0, column=6, padx=5)

filter_btn = tk.Button(frame_top, text="تطبيق الفلاتر وحساب النقاط", command=apply_filters)
filter_btn.grid(row=0, column=7, padx=5)

save_btn = tk.Button(frame_top, text="حفظ النتائج والPDF والرسوم البيانية", command=save_results)
save_btn.grid(row=0, column=8, padx=5)

columns = ("id_student","gender","region","highest_education","age_band","num_of_prev_attempts","studied_credits","final_result","Score")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from data_manager import load_students, load_progress, add_student, update_progress, update_student, delete_student
from analytics import overall_progress, incomplete_work, all_student_progress
from reports import student_progress_report, unit_progress_report, student_trend_report
from validation import validate_student, validate_progress

class CourseProgressMonitor:
    def __init__(self, root):
        self.root = root
        root.title("Course Progress Monitor")
        root.geometry("1050x680")
        self.style()
        self.layout()
        self.dashboard()

    def style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background="#F8F9FA")
        s.configure("Title.TLabel", background="white", foreground="#202124", font=("Arial",20,"bold"))
        s.configure("Head.TLabel", background="#F8F9FA", foreground="#202124", font=("Arial",17,"bold"))
        s.configure("Sub.TLabel", background="#F8F9FA", foreground="#5F6368", font=("Arial",10))
        s.configure("Action.TButton", background="#188038", foreground="white", font=("Arial",10,"bold"), padding=9)
        s.map("Action.TButton", background=[("active","#137333")])
        s.configure("Nav.TButton", background="white", foreground="#3C4043", font=("Arial",10), padding=10)
        s.map("Nav.TButton", background=[("active","#E6F4EA")], foreground=[("active","#188038")])
        s.configure("Treeview", background="white", foreground="#202124", fieldbackground="white", rowheight=32, font=("Arial",10))
        s.configure("Treeview.Heading", background="#E6F4EA", foreground="#202124", font=("Arial",10,"bold"))

    def layout(self):
        top = tk.Frame(self.root,bg="white",height=62); top.pack(fill="x"); top.pack_propagate(False)
        tk.Button(top,text="☰",command=self.toggle,bg="white",relief="flat",font=("Arial",16)).pack(side="left",padx=15)
        ttk.Label(top,text="Course Progress Monitor",style="Title.TLabel").pack(side="left")
        tk.Label(top,text="Academic Progress Management",bg="white",fg="#5F6368",font=("Arial",10)).pack(side="left",padx=15)
        body=tk.Frame(self.root,bg="#F8F9FA"); body.pack(fill="both",expand=True)
        self.side=tk.Frame(body,bg="white",width=185); self.side.pack(side="left",fill="y"); self.side.pack_propagate(False)
        self.content=tk.Frame(body,bg="#F8F9FA"); self.content.pack(side="left",fill="both",expand=True,padx=25,pady=25)
        self.sidebar()

    def sidebar(self):
        items=[("Dashboard",self.dashboard),("Students",self.students),("Progress",self.progress),("Search / Filter",self.search),("Reports",self.reports),("Incomplete Work",self.incomplete)]
        for text,cmd in items: ttk.Button(self.side,text=text,command=cmd,style="Nav.TButton").pack(fill="x",padx=10,pady=3)
        ttk.Separator(self.side).pack(fill="x",padx=15,pady=18)
        ttk.Button(self.side,text="Exit",command=self.root.destroy,style="Nav.TButton").pack(fill="x",padx=10)

    def toggle(self):
        if self.side.winfo_ismapped(): self.side.pack_forget()
        else: self.side.pack(side="left",fill="y",before=self.content)

    def clear(self):
        for w in self.content.winfo_children(): w.destroy()

    def dashboard(self):
        self.clear()
        h=tk.Frame(self.content,bg="#F8F9FA"); h.pack(fill="x",pady=(0,18))
        ttk.Label(h,text="Dashboard",style="Head.TLabel").pack(side="left")
        ttk.Label(h,text="Track student progress across all units and activities",style="Sub.TLabel").pack(side="left",padx=15)
        stats=tk.Frame(self.content,bg="#F8F9FA"); stats.pack(fill="x",pady=(0,18))
        self.card(stats,"Total Students",len(load_students()),0)
        self.card(stats,"Average Progress",f"{overall_progress()}%",1)
        self.card(stats,"Incomplete Tasks",len(incomplete_work()),2)
        self.card(stats,"Total Units",4,3)
        main=tk.Frame(self.content,bg="#F8F9FA"); main.pack(fill="both",expand=True)
        left=tk.Frame(main,bg="#F8F9FA"); left.pack(side="left",fill="both",expand=True,padx=(0,8))
        right=tk.Frame(main,bg="#F8F9FA",width=175); right.pack(side="right",fill="y",padx=(8,0)); right.pack_propagate(False)
        ttk.Label(left,text="Student Progress",style="Head.TLabel").pack(anchor="w",pady=(0,8)); self.table(left)
        ttk.Label(right,text="Quick Actions",style="Head.TLabel").pack(anchor="w",pady=(0,8))
        for text,cmd in [("Add Student",self.add),("Update Progress",self.update),("Search / Filter",self.search),("View Reports",self.reports),("Incomplete Work",self.incomplete)]: ttk.Button(right,text=text,command=cmd,style="Action.TButton").pack(fill="x",pady=5)

    def card(self,parent,title,value,col):
        f=tk.Frame(parent,bg="white",highlightbackground="#DADCE0",highlightthickness=1); f.grid(row=0,column=col,sticky="nsew",padx=4); parent.columnconfigure(col,weight=1)
        tk.Frame(f,bg="#188038",height=4).pack(fill="x")
        tk.Label(f,text=title,bg="white",fg="#5F6368",font=("Arial",10)).pack(anchor="w",padx=14,pady=(10,2))
        tk.Label(f,text=value,bg="white",fg="#202124",font=("Arial",21,"bold")).pack(anchor="w",padx=14,pady=(0,10))

    def table(self,parent):
        f=tk.Frame(parent,bg="white"); f.pack(fill="both",expand=True)
        cols=("ID","Name","Unit 1","Unit 2","Unit 3","Unit 4","Average")
        t=ttk.Treeview(f,columns=cols,show="headings")
        for c in cols: t.heading(c,text=c)
        for c,w in zip(cols,[55,145,70,70,70,70,80]): t.column(c,width=w)
        students,progress=load_students(),load_progress()
        for _,st in students.iterrows():
            sid=str(st["student_id"]); vals=[]
            for u in ["Unit 1","Unit 2","Unit 3","Unit 4"]:
                d=progress[(progress.student_id.astype(str)==sid)&(progress.unit==u)]
                vals.append("-" if d.empty else f"{d.completion.mean():.0f}%")
            d=progress[progress.student_id.astype(str)==sid]; avg=0 if d.empty else d.completion.mean()
            t.insert("","end",values=(sid,st["name"],*vals,f"{avg:.1f}%"))
        t.pack(side="left",fill="both",expand=True)
        sb=ttk.Scrollbar(f,command=t.yview); sb.pack(side="right",fill="y"); t.configure(yscrollcommand=sb.set)

    def add(self):
        w=tk.Toplevel(self.root); w.title("Add Student"); w.geometry("400x340")
        ttk.Label(w,text="Add Student",font=("Arial",18,"bold")).pack(pady=20); form=ttk.Frame(w); form.pack(fill="x",padx=30); e={}
        for label in ["Student ID","Name","Email"]:
            ttk.Label(form,text=label).pack(anchor="w"); x=ttk.Entry(form); x.pack(fill="x",pady=(2,10)); e[label]=x
        def save():
            ok,msg=validate_student(e["Student ID"].get(),e["Name"].get(),e["Email"].get())
            if not ok: messagebox.showerror("Invalid Input",msg); return
            ok,msg=add_student(e["Student ID"].get(),e["Name"].get(),e["Email"].get())
            if ok: messagebox.showinfo("Success",msg); w.destroy(); self.dashboard()
            else: messagebox.showerror("Error",msg)
        ttk.Button(w,text="Add Student",command=save,style="Action.TButton").pack(pady=10)

    def update(self):
        w=tk.Toplevel(self.root); w.title("Update Progress"); w.geometry("420x450")
        ttk.Label(w,text="Update Progress",font=("Arial",18,"bold")).pack(pady=20); f=ttk.Frame(w); f.pack(fill="x",padx=30)
        ttk.Label(f,text="Student ID").pack(anchor="w"); sid=ttk.Entry(f); sid.pack(fill="x",pady=(2,10))
        ttk.Label(f,text="Unit").pack(anchor="w"); unit=ttk.Combobox(f,values=["Unit 1","Unit 2","Unit 3","Unit 4"],state="readonly"); unit.set("Unit 1"); unit.pack(fill="x",pady=(2,10))
        ttk.Label(f,text="Activity").pack(anchor="w"); act=ttk.Entry(f); act.pack(fill="x",pady=(2,10))
        ttk.Label(f,text="Completion (%)").pack(anchor="w"); comp=ttk.Entry(f); comp.pack(fill="x",pady=(2,10))
        ttk.Label(f,text="Date").pack(anchor="w"); date=DateEntry(f,date_pattern="yyyy-mm-dd"); date.pack(anchor="w",pady=(2,15))
        def save():
            ok,msg=validate_progress(sid.get(),unit.get(),act.get(),comp.get(),date.get())
            if not ok: messagebox.showerror("Invalid Input",msg); return
            ok,msg=update_progress(sid.get(),unit.get(),act.get(),comp.get(),date.get())
            if ok: messagebox.showinfo("Success",msg); w.destroy(); self.dashboard()
            else: messagebox.showerror("Error",msg)
        ttk.Button(w,text="Save Progress",command=save,style="Action.TButton").pack()

    def students(self):
        w=tk.Toplevel(self.root); w.title("Student Records"); w.geometry("820x500")
        ttk.Label(w,text="Student Records",font=("Arial",18,"bold")).pack(anchor="w",padx=20,pady=15)
        f=ttk.Frame(w); f.pack(fill="both",expand=True,padx=20); cols=("ID","Name","Email","Progress"); t=ttk.Treeview(f,columns=cols,show="headings")
        for c in cols: t.heading(c,text=c)
        for c,x in zip(cols,[80,170,300,100]): t.column(c,width=x)
        t.pack(fill="both",expand=True)
        def refresh():
            t.delete(*t.get_children())
            for _,r in all_student_progress().iterrows(): t.insert("","end",values=(r.student_id,r["name"],r.email,f"{r.progress}%"))
        def edit():
            s=t.selection()
            if not s: messagebox.showwarning("Select Student","Select a student first."); return
            v=t.item(s[0],"values"); ewin=tk.Toplevel(w); ewin.title("Edit Student"); ewin.geometry("380x330"); f2=ttk.Frame(ewin); f2.pack(fill="x",padx=30,pady=25); e={}
            for label,val in zip(["Student ID","Name","Email"],v[:3]):
                ttk.Label(f2,text=label).pack(anchor="w"); x=ttk.Entry(f2); x.insert(0,val); x.pack(fill="x",pady=(2,10)); e[label]=x
            def save():
                ok,msg=validate_student(e["Student ID"].get(),e["Name"].get(),e["Email"].get())
                if not ok: messagebox.showerror("Invalid Input",msg); return
                ok,msg=update_student(v[0],e["Student ID"].get(),e["Name"].get(),e["Email"].get())
                if ok: messagebox.showinfo("Success",msg); ewin.destroy(); refresh(); self.dashboard()
                else: messagebox.showerror("Error",msg)
            ttk.Button(ewin,text="Save Changes",command=save,style="Action.TButton").pack()
        def delete():
            s=t.selection()
            if not s: messagebox.showwarning("Select Student","Select a student first."); return
            v=t.item(s[0],"values")
            if messagebox.askyesno("Confirm Delete",f"Delete {v[1]} and all progress?"):
                ok,msg=delete_student(v[0]); messagebox.showinfo("Result",msg) if ok else messagebox.showerror("Error",msg); refresh(); self.dashboard()
        b=ttk.Frame(w); b.pack(pady=12); ttk.Button(b,text="Edit Student",command=edit,style="Action.TButton").pack(side="left",padx=5); ttk.Button(b,text="Delete Student",command=delete).pack(side="left",padx=5); refresh()

    def progress(self): self.update()

    def incomplete(self):
        w=tk.Toplevel(self.root); w.title("Incomplete Work"); w.geometry("760x450")
        ttk.Label(w,text="Incomplete Work",font=("Arial",18,"bold")).pack(anchor="w",padx=20,pady=15)
        cols=("Student","Unit","Activity","Completion","Date"); t=ttk.Treeview(w,columns=cols,show="headings")
        for c in cols: t.heading(c,text=c)
        for _,r in incomplete_work(50).iterrows(): t.insert("","end",values=(r.student_id,r.unit,r.activity,f"{r.completion}%",r.date))
        t.pack(fill="both",expand=True,padx=20,pady=10)

    def search(self):
        w=tk.Toplevel(self.root); w.title("Search / Filter"); w.geometry("850x500")
        f=ttk.Frame(w); f.pack(fill="x",padx=20,pady=15); ttk.Label(f,text="Student ID / Name").grid(row=0,column=0,padx=5); q=ttk.Entry(f,width=20); q.grid(row=0,column=1,padx=5); ttk.Label(f,text="Unit").grid(row=0,column=2,padx=5); u=ttk.Combobox(f,values=["All","Unit 1","Unit 2","Unit 3","Unit 4"],state="readonly",width=12); u.set("All"); u.grid(row=0,column=3,padx=5)
        cols=("ID","Name","Unit","Activity","Completion"); t=ttk.Treeview(w,columns=cols,show="headings")
        for c in cols: t.heading(c,text=c)
        t.pack(fill="both",expand=True,padx=20,pady=10)
        def run():
            s,p=load_students(),load_progress(); d=p.merge(s,on="student_id",how="left"); text=q.get().lower().strip()
            if text: d=d[d.student_id.astype(str).str.lower().str.contains(text)|d.name.astype(str).str.lower().str.contains(text)]
            if u.get()!="All": d=d[d.unit==u.get()]
            t.delete(*t.get_children())
            for _,r in d.iterrows(): t.insert("","end",values=(r.student_id,r.name,r.unit,r.activity,f"{r.completion}%"))
        ttk.Button(f,text="Search",command=run,style="Action.TButton").grid(row=0,column=4,padx=8); run()

    def reports(self):
        w=tk.Toplevel(self.root); w.title("Reports"); w.geometry("420x300"); ttk.Label(w,text="Course Reports",font=("Arial",20,"bold")).pack(pady=25)
        ttk.Button(w,text="Student Progress Report",command=student_progress_report,style="Action.TButton").pack(fill="x",padx=55,pady=6)
        ttk.Button(w,text="Unit Completion Report",command=unit_progress_report,style="Action.TButton").pack(fill="x",padx=55,pady=6)
        ttk.Button(w,text="Student Trend Report",command=self.trend,style="Action.TButton").pack(fill="x",padx=55,pady=6)

    def trend(self):
        w=tk.Toplevel(self.root); w.title("Student Trend"); w.geometry("330x200"); ttk.Label(w,text="Student ID").pack(pady=(30,8)); e=ttk.Entry(w); e.pack()
        def show():
            sid=e.get().strip()
            if sid not in load_students().student_id.astype(str).values: messagebox.showerror("Error","Student ID does not exist."); return
            w.destroy(); student_trend_report(sid)
        ttk.Button(w,text="Show Trend",command=show,style="Action.TButton").pack(pady=18)

root=tk.Tk()
app=CourseProgressMonitor(root)
root.mainloop()

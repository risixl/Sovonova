# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend import add_case, get_cases, assign_case, get_analytics
from db_setup import setup_db

# Initialize database
setup_db()

class CaseManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Case Manager")
        self.root.geometry("900x700")
        
        # Modern color scheme
        self.bg_color = "#f8f9fa"
        self.primary_color = "#4e73df"
        self.success_color = "#1cc88a"
        self.text_color = "#5a5c69"
        self.card_color = "#ffffff"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Custom styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, 
                           font=('Segoe UI', 10))
        self.style.configure("TButton", font=('Segoe UI', 10), padding=8)
        self.style.configure("TNotebook", background=self.bg_color)
        self.style.configure("TNotebook.Tab", font=('Segoe UI', 10, 'bold'), padding=[10, 5])
        
        # Custom button styles
        self.style.map("Primary.TButton",
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#3a56b4'), ('!disabled', self.primary_color)])
        self.style.map("Success.TButton",
                      foreground=[('active', 'white'), ('!disabled', 'white')],
                      background=[('active', '#17a673'), ('!disabled', self.success_color)])
        
        # Header frame
        self.header_frame = ttk.Frame(self.root, padding=(20, 10, 20, 0))
        self.header_frame.pack(fill=tk.X)
        
        # App title
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Case Management Dashboard", 
            font=('Segoe UI', 16, 'bold'),
            foreground=self.primary_color
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.case_tab = ttk.Frame(self.notebook)
        self.assignment_tab = ttk.Frame(self.notebook)
        self.analytics_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.case_tab, text="📋 Cases")
        self.notebook.add(self.assignment_tab, text="👤 Assignments")
        self.notebook.add(self.analytics_tab, text="📊 Analytics")
        
        # Build tabs
        self.build_case_tab()
        self.build_assignment_tab()
        self.build_analytics_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            padding=(10, 5),
            font=('Segoe UI', 9),
            foreground="#6c757d"
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Initial refresh
        self.refresh_cases()
    
    def build_case_tab(self):
        """Build the Case Management tab"""
        # Main container for case tab
        case_container = ttk.Frame(self.case_tab)
        case_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Add Case
        left_panel = ttk.Frame(case_container)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Add Case card
        add_card = ttk.LabelFrame(
            left_panel, 
            text=" Add New Case ", 
            padding=15,
            relief=tk.RAISED,
            style='Card.TFrame'
        )
        add_card.pack(fill=tk.X, pady=(0, 10))
        
        # Form fields
        fields = [
            ("User ID", "entry_user_id"),
            ("Case Title", "entry_title"),
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            ttk.Label(add_card, text=label_text+":", font=('Segoe UI', 9, 'bold')).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(add_card, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            setattr(self, attr_name, entry)
        
        # Description field
        ttk.Label(add_card, text="Description:", font=('Segoe UI', 9, 'bold')).grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.entry_desc = tk.Text(add_card, height=5, width=30, wrap=tk.WORD, font=('Segoe UI', 10))
        self.entry_desc.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Add Case Button
        ttk.Button(
            add_card, 
            text="➕ Add Case", 
            command=self.add_case_gui, 
            style="Success.TButton"
        ).grid(row=3, column=1, sticky=tk.E, pady=(10, 0))
        
        # Right panel - Cases List
        right_panel = ttk.Frame(case_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Cases List card
        list_card = ttk.LabelFrame(
            right_panel, 
            text=" Cases List ", 
            padding=10,
            relief=tk.RAISED
        )
        list_card.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for cases
        columns = ("ID", "User ID", "Title", "Status", "Consultant")
        self.cases_tree = ttk.Treeview(
            list_card, 
            columns=columns, 
            show="headings",
            selectmode="browse",
            style="Treeview"
        )
        
        # Configure columns
        col_widths = [50, 80, 250, 100, 100]
        for col, width in zip(columns, col_widths):
            self.cases_tree.column(col, width=width, anchor=tk.CENTER)
            self.cases_tree.heading(col, text=col)
        
        self.cases_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_card, orient="vertical", command=self.cases_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cases_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh Button
        ttk.Button(
            right_panel, 
            text="🔄 Refresh List", 
            command=self.refresh_cases, 
            style="Primary.TButton"
        ).pack(pady=(10, 0), anchor=tk.E)
    
    def build_assignment_tab(self):
        """Build the Assignment tab"""
        # Main container
        assign_container = ttk.Frame(self.assignment_tab, padding=20)
        assign_container.pack(fill=tk.BOTH, expand=True)
        
        # Assignment card
        assign_card = ttk.LabelFrame(
            assign_container, 
            text=" Assign Case ", 
            padding=20,
            relief=tk.RAISED
        )
        assign_card.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Case ID", "entry_case_id"),
            ("Consultant ID", "entry_consultant_id"),
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            ttk.Label(assign_card, text=label_text+":", font=('Segoe UI', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=10, padx=(0, 10))
            entry = ttk.Entry(assign_card, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, sticky=tk.EW, pady=10)
            setattr(self, attr_name, entry)
        
        # Assign Button
        ttk.Button(
            assign_card, 
            text="👥 Assign Case", 
            command=self.assign_case_gui, 
            style="Primary.TButton"
        ).grid(row=2, column=1, sticky=tk.E, pady=(20, 0))
    
    def build_analytics_tab(self):
        """Build the Analytics tab"""
        # Main container
        analytics_container = ttk.Frame(self.analytics_tab, padding=20)
        analytics_container.pack(fill=tk.BOTH, expand=True)
        
        # Analytics card
        analytics_card = ttk.LabelFrame(
            analytics_container, 
            text=" Case Analytics ", 
            padding=20,
            relief=tk.RAISED
        )
        analytics_card.pack(fill=tk.BOTH, expand=True)
        
        # Analytics display
        self.analytics_text = tk.Text(
            analytics_card, 
            height=10, 
            width=60, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=('Segoe UI', 10),
            padx=10,
            pady=10,
            bg=self.card_color
        )
        self.analytics_text.pack(fill=tk.BOTH, expand=True)
        
        # View Button
        ttk.Button(
            analytics_card, 
            text="📈 View Analytics", 
            command=self.show_analytics, 
            style="Primary.TButton"
        ).pack(pady=(20, 0), anchor=tk.E)
    
    def refresh_cases(self):
        """Refresh the cases list"""
        self.cases_tree.delete(*self.cases_tree.get_children())
        try:
            for case in get_cases():
                self.cases_tree.insert("", tk.END, values=case)
            self.status_var.set(f"✅ Loaded {len(self.cases_tree.get_children())} cases")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load cases: {str(e)}")
            self.status_var.set("❌ Error loading cases")
    
    def add_case_gui(self):
        """Handle adding a new case"""
        try:
            uid = int(self.entry_user_id.get())
            title = self.entry_title.get()
            desc = self.entry_desc.get("1.0", tk.END).strip()
            
            if not title or not desc:
                messagebox.showwarning("Validation", "Title and description are required!")
                return
                
            add_case(uid, title, desc)
            messagebox.showinfo("Success", "Case added successfully!")
            self.refresh_cases()
            
            # Clear form
            self.entry_title.delete(0, tk.END)
            self.entry_desc.delete("1.0", tk.END)
            self.status_var.set("✅ Case added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "User ID must be a number!")
            self.status_var.set("❌ Invalid User ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add case: {str(e)}")
            self.status_var.set("❌ Error adding case")
    
    def assign_case_gui(self):
        """Handle case assignment"""
        try:
            cid = int(self.entry_case_id.get())
            cons_id = int(self.entry_consultant_id.get())
            
            assign_case(cid, cons_id)
            messagebox.showinfo("Success", "Case assigned successfully!")
            self.refresh_cases()
            
            # Clear form
            self.entry_case_id.delete(0, tk.END)
            self.entry_consultant_id.delete(0, tk.END)
            self.status_var.set(f"✅ Case {cid} assigned to consultant {cons_id}")
            
        except ValueError:
            messagebox.showerror("Error", "Both IDs must be numbers!")
            self.status_var.set("❌ Invalid ID format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign case: {str(e)}")
            self.status_var.set("❌ Error assigning case")
    
    def show_analytics(self):
        """Display analytics data"""
        try:
            total, approved, rate = get_analytics()
            
            self.analytics_text.config(state=tk.NORMAL)
            self.analytics_text.delete("1.0", tk.END)
            
            # Format analytics output
            self.analytics_text.insert(tk.END, "📊 Case Analytics Summary\n", "header")
            self.analytics_text.insert(tk.END, "="*40 + "\n\n")
            self.analytics_text.insert(tk.END, f"• Total Cases: {total}\n")
            self.analytics_text.insert(tk.END, f"• Approved Cases: {approved}\n")
            self.analytics_text.insert(tk.END, f"• Approval Rate: {rate}%\n\n")
            
            # Add some analysis
            self.analytics_text.insert(tk.END, "📝 Analysis:\n", "header")
            if rate > 75:
                self.analytics_text.insert(tk.END, "🌟 Excellent approval rate! Keep up the good work.")
            elif rate > 50:
                self.analytics_text.insert(tk.END, "👍 Good approval rate. There's room for improvement.")
            else:
                self.analytics_text.insert(tk.END, "⚠️ Low approval rate. Consider reviewing case handling procedures.")
            
            self.analytics_text.tag_config("header", font=('Segoe UI', 11, 'bold'))
            self.analytics_text.config(state=tk.DISABLED)
            
            self.status_var.set("✅ Analytics refreshed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load analytics: {str(e)}")
            self.status_var.set("❌ Error loading analytics")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CaseManagementApp(root)
    root.mainloop()
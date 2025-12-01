
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
VALID_BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ---------- DATA MODEL ----------

class Donor:
    def __init__(self, name, age, gender, contact, blood_type, location):
        self.name = name.title()
        self.age = age
        self.gender = gender
        self.contact = contact
        self.blood_type = blood_type
        self.location = location

    def _str_(self):
        return f"{self.name} | {self.age} | {self.gender} | {self.contact} | {self.blood_type} | {self.location}"


# ---------- CORE SYSTEM ----------

class BloodDonationSystem:
    def __init__(self):
        self.donors = []

    def register(self, name, age, gender, contact, blood_type, location):
        for donor in self.donors:
            if donor.contact == contact:
                messagebox.showerror("🚫 Error", "A donor with this contact number already exists.")
                return
        new_donor = Donor(name, age, gender, contact, blood_type.upper(), location.upper())
        self.donors.append(new_donor)
        messagebox.showinfo("✅ Success", f"Donor {name} registered successfully!")

    def search(self, blood_type, location):
        blood_type = blood_type.strip().upper()
        location = location.strip().lower()
        return [donor for donor in self.donors
                if blood_type in donor.blood_type.upper() and location in donor.location.lower()]

    def list_donors(self):
        return self.donors

    def update_donor(self, contact, name, age, gender, blood_type, location):
        for donor in self.donors:
            if donor.contact == contact:
                donor.name = name if name else donor.name
                donor.age = age if age else donor.age
                donor.gender = gender if gender else donor.gender
                donor.blood_type = blood_type.upper() if blood_type else donor.blood_type
                donor.location = location.upper() if location else donor.location
                messagebox.showinfo("🔄 Updated", "Donor information updated successfully.")
                return
        messagebox.showerror("⚠ Error", "Donor not found.")

    def delete_donor(self, contact):
        for donor in self.donors:
            if donor.contact == contact:
                self.donors.remove(donor)
                messagebox.showinfo("🗑 Deleted", f"Donor {donor.name} removed successfully.")
                return
        messagebox.showerror("⚠ Error", "Donor not found.")

    def save_data(self, filename="donors.json"):
        with open(filename, 'w') as f:
            json.dump([donor.__dict__ for donor in self.donors], f)
        messagebox.showinfo("💾 Saved", "All donor data saved successfully!")

    def load_data(self, filename="donors.json"):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        self.donors = []
                        return
                    donor_data = json.loads(content)
                    self.donors = [Donor(**data) for data in donor_data]
            except:
                # File exists but is corrupt → reset to empty list
                self.donors = []
        else:
            self.donors = []


# ---------- GUI ----------

class BloodDonationApp:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.system.load_data()

        # Window setup
        self.root.title("🩸 Blood Donation Management System")
        self.root.geometry("1000x650")
        self.root.minsize(850, 550)
        self.root.configure(bg="#8B0000")  # Simple solid red background

        # Frame for centered content
        main_frame = tk.Frame(self.root, bg="#8B0000")
        main_frame.pack(expand=True)

        # Center the grid
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(10):
            main_frame.grid_rowconfigure(i, weight=1)

        # Apply ttk style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Red.TButton",
                             padding=8,
                             relief="flat",
                             background="#B22222",
                             foreground="white",
                             font=("Arial", 11, "bold"))
        self.style.map("Red.TButton",
                       background=[("active", "#800000")])

        self.style.configure("Treeview",
                             background="#fff5f5",
                             fieldbackground="#fff5f5",
                             font=("Arial", 10))
        self.style.configure("Treeview.Heading",
                             background="#B22222",
                             foreground="white",
                             font=("Arial", 11, "bold"))

        # Title Label
        title = tk.Label(main_frame,
                         text="❤ BLOOD DONATION SYSTEM ❤",
                         bg="#8B0000",
                         fg="white",
                         font=("Helvetica", 26, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=20)

        # Input Variables
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="Male")
        self.contact_var = tk.StringVar()
        self.blood_var = tk.StringVar()
        self.location_var = tk.StringVar()

        label_font = ("Arial", 12, "bold")

        # Input Fields
        tk.Label(main_frame, text="👤 Name:", bg="#8B0000", fg="white", font=label_font).grid(row=1, column=0, padx=10)
        ttk.Entry(main_frame, textvariable=self.name_var, width=25).grid(row=1, column=1, padx=5)

        tk.Label(main_frame, text=" Age:", bg="#8B0000", fg="white", font=label_font).grid(row=2, column=0, padx=10)
        ttk.Entry(main_frame, textvariable=self.age_var, width=25).grid(row=2, column=1, padx=5)

        tk.Label(main_frame, text="🚻 Gender:", bg="#8B0000", fg="white", font=label_font).grid(row=3, column=0, padx=10)
        gender_frame = tk.Frame(main_frame, bg="#8B0000")
        gender_frame.grid(row=3, column=1, padx=5)
        tk.Radiobutton(gender_frame, text="Male ♂", variable=self.gender_var, value="Male",
                       bg="#8B0000", fg="white", selectcolor="#B22222").pack(side="left", padx=5)
        tk.Radiobutton(gender_frame, text="Female ♀", variable=self.gender_var, value="Female",
                       bg="#8B0000", fg="white", selectcolor="#B22222").pack(side="left", padx=5)
        tk.Radiobutton(gender_frame, text="Other ⚧", variable=self.gender_var, value="Other",
                       bg="#8B0000", fg="white", selectcolor="#B22222").pack(side="left", padx=5)

        tk.Label(main_frame, text="📞 Contact:", bg="#8B0000", fg="white", font=label_font).grid(row=4, column=0, padx=10)
        ttk.Entry(main_frame, textvariable=self.contact_var, width=25).grid(row=4, column=1, padx=5)

        tk.Label(main_frame, text="🩸 Blood Type:", bg="#8B0000", fg="white", font=label_font).grid(row=5, column=0, padx=10)
        tk.Label(main_frame, text="🩸 Blood Type:", bg="#8B0000", fg="white", font=label_font).grid(row=5, column=0, padx=10)

        tk.Label(main_frame, text="📍 Address:", bg="#8B0000", fg="white", font=label_font).grid(row=6, column=0, padx=10)
        ttk.Entry(main_frame, textvariable=self.location_var, width=25).grid(row=6, column=1, padx=10)


        self.blood_dropdown = ttk.Combobox(
            main_frame,
            textvariable=self.blood_var,
            values=VALID_BLOOD_TYPES,
            state="readonly",
            width=22
        )
        self.blood_dropdown.grid(row=5, column=1, padx=5)
        self.blood_dropdown.set("Select Blood Type")
        # Buttons
        ttk.Button(main_frame, text="➕ Register", style="Red.TButton", command=self.register_donor).grid(row=7, column=0, pady=10)
        ttk.Button(main_frame, text="🔍 Search", style="Red.TButton", command=self.search_donors).grid(row=7, column=1, pady=10)
        ttk.Button(main_frame, text="📋 List", style="Red.TButton", command=self.list_donors).grid(row=7, column=2, pady=10)
        ttk.Button(main_frame, text="🛠 Update", style="Red.TButton", command=self.update_donor).grid(row=8, column=0, pady=10)
        ttk.Button(main_frame, text="🗑 Delete", style="Red.TButton", command=self.delete_donor).grid(row=8, column=1, pady=10)
        ttk.Button(main_frame, text="💾 Save & Exit", style="Red.TButton", command=self.save_and_exit).grid(row=8, column=2, pady=10)

        # Donor Table
        self.tree = ttk.Treeview(main_frame,
                                 columns=("Name", "Age", "Gender", "Contact", "Blood", "Location"),
                                 show="headings", height=10)
        self.tree.grid(row=9, column=0, columnspan=3, pady=10, sticky="nsew")

        for col in ("Name", "Age", "Gender", "Contact", "Blood", "Location"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=9, column=3, sticky="ns")

        self.refresh_tree()

    # ---------- Functional Methods ----------

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for donor in self.system.donors:
            self.tree.insert("", "end",
                             values=(donor.name, donor.age, donor.gender, donor.contact,
                                     donor.blood_type, donor.location))

    def register_donor(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get()
        contact = self.contact_var.get().strip()
        blood = self.blood_var.get().strip().upper()
        location = self.location_var.get().strip()
        if blood not in VALID_BLOOD_TYPES:
            messagebox.showerror(
                "🚫 Invalid Blood Type",
                "Please select a valid blood group."
            )
            return



        if not (name and age and gender and contact and blood and location):
            messagebox.showerror("⚠ Input Error", "All fields are required.")
            return
 # ---------- AGE FIX: ONLY 18–60 ALLOWED ----------
        if not age.isdigit():
            messagebox.showerror("🚫 Error", "Age must contain digits only.")
            return

        age_int = int(age)
        if age_int < 18 or age_int > 60:
            messagebox.showerror("🚫 Error", "Age must be between 18 and 60.")
            return
        # -------------------------------------------------

        if not contact.isdigit():
            messagebox.showerror("🚫 Error", "Contact must contain digits only.")
            return

        self.system.register(name, age, gender, contact, blood, location)
        self.refresh_tree()
        self.clear_fields()

    def search_donors(self):
        blood = self.blood_var.get()
        location = self.location_var.get()
        results = self.system.search(blood, location)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for donor in results:
            self.tree.insert("", "end",
                             values=(donor.name, donor.age, donor.gender,
                                     donor.contact, donor.blood_type, donor.location))
        if not results:
            messagebox.showinfo("🔍 Search Result", "No matching donors found.")

    def list_donors(self):
        self.refresh_tree()

    def update_donor(self):
        contact = self.contact_var.get()
        self.system.update_donor(contact,
                                 self.name_var.get(),
                                 self.age_var.get(),
                                 self.gender_var.get(),
                                 self.blood_var.get(),
                                 self.location_var.get())
        self.refresh_tree()

    def delete_donor(self):
        contact = self.contact_var.get()
        if not contact:
            messagebox.showerror("⚠ Error", "Please enter a contact number to delete.")
            return
        self.system.delete_donor(contact)
        self.refresh_tree()

    def save_and_exit(self):
        self.system.save_data()
        self.root.quit()

    def clear_fields(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("Male")
        self.contact_var.set("")
        self.blood_var.set("")
        self.location_var.set("")
        self.blood_dropdown.set("Select Blood Type")


# ---------- MAIN ----------

def main():
    system = BloodDonationSystem()
    root = tk.Tk()
    BloodDonationApp(root, system)
    root.mainloop()


if __name__ == "__main__":
    main()
"""
Owen Moloney
Flooring Cost Calculator - GUI Version
Desktop application using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from main import FlooringJob, Room, Obstacle, Employee
from typing import List, Optional
import os
import io


class FlooringCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flooring Cost Calculator")
        self.root.geometry("1000x700")
        
        # Initialize job data
        self.job = FlooringJob()
        self.blueprint_path = None
        self.blueprint_window = None
        
        # Create main layout
        self.create_widgets()
        
        # Update display
        self.update_cost_summary()
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Menu bar with Blueprint button
        menu_frame = ttk.Frame(self.root)
        menu_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        menu_frame.columnconfigure(0, weight=1)
        
        ttk.Button(menu_frame, text="Load Blueprint", command=self.load_blueprint).pack(side=tk.RIGHT, padx=5)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top Row: Rooms and Employees
        self.create_rooms_panel(main_frame)
        self.create_employees_panel(main_frame)
        
        # Bottom Row: Job Details and Cost Summary
        self.create_job_details_panel(main_frame)
        self.create_cost_summary_panel(main_frame)
    
    def create_rooms_panel(self, parent):
        """Create rooms input panel"""
        frame = ttk.LabelFrame(parent, text="Rooms", padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        
        # Room list
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.rooms_listbox = tk.Listbox(list_frame, height=8, yscrollcommand=scrollbar.set)
        self.rooms_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.rooms_listbox.yview)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Add Room", command=self.add_room_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit Room", command=self.edit_room_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Remove Room", command=self.remove_room).pack(side=tk.LEFT, padx=2)
    
    def create_employees_panel(self, parent):
        """Create employees input panel"""
        frame = ttk.LabelFrame(parent, text="Employees", padding="10")
        frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        
        # Employee list
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.employees_listbox = tk.Listbox(list_frame, height=8, yscrollcommand=scrollbar.set)
        self.employees_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.employees_listbox.yview)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=5)
        
        ttk.Button(btn_frame, text="Add Employee", command=self.add_employee_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Edit Employee", command=self.edit_employee_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Remove Employee", command=self.remove_employee).pack(side=tk.LEFT, padx=2)
    
    def create_job_details_panel(self, parent):
        """Create job details input panel"""
        frame = ttk.LabelFrame(parent, text="Job Details", padding="10")
        frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # Days required
        ttk.Label(frame, text="Days Required:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.days_var = tk.StringVar(value="0")
        days_entry = ttk.Entry(frame, textvariable=self.days_var, width=10)
        days_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        days_entry.bind('<KeyRelease>', lambda e: self.update_cost_summary())
        
        # Sanding cost per sq ft
        ttk.Label(frame, text="Sanding Cost ($/sq ft):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sanding_var = tk.StringVar(value="0.00")
        sanding_entry = ttk.Entry(frame, textvariable=self.sanding_var, width=10)
        sanding_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        sanding_entry.bind('<KeyRelease>', lambda e: self.update_cost_summary())
        
        # Material option
        ttk.Label(frame, text="Material Source:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.material_source_var = tk.StringVar(value="customer")
        material_frame = ttk.Frame(frame)
        material_frame.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Radiobutton(material_frame, text="Customer provides wood", 
                       variable=self.material_source_var, value="customer",
                       command=self.toggle_material_fields).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(material_frame, text="Company provides wood",
                       variable=self.material_source_var, value="company",
                       command=self.toggle_material_fields).pack(side=tk.LEFT, padx=5)
        
        # Material cost per sq ft
        ttk.Label(frame, text="Material Cost ($/sq ft):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.material_cost_var = tk.StringVar(value="0.00")
        self.material_cost_entry = ttk.Entry(frame, textvariable=self.material_cost_var, width=10)
        self.material_cost_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        self.material_cost_entry.bind('<KeyRelease>', lambda e: self.update_cost_summary())
        
        # Pickup fee
        ttk.Label(frame, text="Pickup/Delivery Fee ($):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.pickup_fee_var = tk.StringVar(value="0.00")
        self.pickup_fee_entry = ttk.Entry(frame, textvariable=self.pickup_fee_var, width=10)
        self.pickup_fee_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        self.pickup_fee_entry.bind('<KeyRelease>', lambda e: self.update_cost_summary())
        
        # Initialize material fields state
        self.toggle_material_fields()
    
    def create_cost_summary_panel(self, parent):
        """Create cost summary display panel"""
        frame = ttk.LabelFrame(parent, text="Cost Summary", padding="10")
        frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # Display area
        display_frame = ttk.Frame(frame)
        display_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        display_frame.columnconfigure(1, weight=1)
        
        # Total floor space
        ttk.Label(display_frame, text="Total Floor Space:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.total_space_label = ttk.Label(display_frame, text="0.00 sq ft", font=("", 10))
        self.total_space_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Sanding cost
        ttk.Label(display_frame, text="Sanding Cost:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.sanding_cost_label = ttk.Label(display_frame, text="$0.00", font=("", 10))
        self.sanding_cost_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Labor cost
        ttk.Label(display_frame, text="Labor Cost:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.labor_cost_label = ttk.Label(display_frame, text="$0.00", font=("", 10))
        self.labor_cost_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Material cost
        ttk.Label(display_frame, text="Material Cost:").grid(row=3, column=0, sticky=tk.W, pady=3)
        self.material_cost_label = ttk.Label(display_frame, text="$0.00", font=("", 10))
        self.material_cost_label.grid(row=3, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Separator
        ttk.Separator(display_frame, orient=tk.HORIZONTAL).grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Total cost
        ttk.Label(display_frame, text="TOTAL COST:", font=("", 12, "bold")).grid(row=5, column=0, sticky=tk.W, pady=3)
        self.total_cost_label = ttk.Label(display_frame, text="$0.00", font=("", 14, "bold"))
        self.total_cost_label.grid(row=5, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Action buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Calculate", command=self.calculate_costs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def toggle_material_fields(self):
        """Enable/disable material cost fields based on source"""
        if self.material_source_var.get() == "customer":
            self.material_cost_entry.config(state="disabled")
            self.pickup_fee_entry.config(state="disabled")
        else:
            self.material_cost_entry.config(state="normal")
            self.pickup_fee_entry.config(state="normal")
        self.update_cost_summary()
    
    def add_room_dialog(self):
        """Open dialog to add a new room"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Room")
        dialog.geometry("450x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Room name
        ttk.Label(dialog, text="Room Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=10)
        
        # Area input method
        ttk.Label(dialog, text="Enter Area:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        method_var = tk.StringVar(value="total")
        method_frame = ttk.Frame(dialog)
        method_frame.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Radiobutton(method_frame, text="Length × Width", variable=method_var, value="lengthwidth").pack(side=tk.LEFT)
        ttk.Radiobutton(method_frame, text="Total sq ft", variable=method_var, value="total").pack(side=tk.LEFT)
        
        # Length and Width fields
        length_var = tk.StringVar()
        width_var = tk.StringVar()
        total_var = tk.StringVar()
        
        length_frame = ttk.Frame(dialog)
        length_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        
        ttk.Label(length_frame, text="Length (ft):").pack(side=tk.LEFT, padx=5)
        length_entry = ttk.Entry(length_frame, textvariable=length_var, width=10)
        length_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(length_frame, text="Width (ft):").pack(side=tk.LEFT, padx=5)
        width_entry = ttk.Entry(length_frame, textvariable=width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=5)
        
        total_frame = ttk.Frame(dialog)
        total_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
        
        ttk.Label(total_frame, text="Total Area (sq ft):").pack(side=tk.LEFT, padx=5)
        total_entry = ttk.Entry(total_frame, textvariable=total_var, width=10)
        total_entry.pack(side=tk.LEFT, padx=5)
        
        # Obstacles
        ttk.Label(dialog, text="Obstacles:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        obstacles = []
        
        obstacle_list_frame = ttk.Frame(dialog)
        obstacle_list_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        
        obstacle_list = tk.Listbox(obstacle_list_frame, height=4, width=40)
        obstacle_list.pack(side=tk.LEFT)
        
        obstacle_scroll = ttk.Scrollbar(obstacle_list_frame, orient=tk.VERTICAL)
        obstacle_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        obstacle_list.config(yscrollcommand=obstacle_scroll.set)
        obstacle_scroll.config(command=obstacle_list.yview)
        
        def add_obstacle():
            obstacle_dialog = tk.Toplevel(dialog)
            obstacle_dialog.title("Add Obstacle")
            obstacle_dialog.geometry("400x280")
            obstacle_dialog.transient(dialog)
            obstacle_dialog.grab_set()
            
            # Obstacle name
            ttk.Label(obstacle_dialog, text="Obstacle Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
            obs_name_var = tk.StringVar()
            ttk.Entry(obstacle_dialog, textvariable=obs_name_var, width=25).grid(row=0, column=1, padx=10, pady=10)
            
            # Area input method
            ttk.Label(obstacle_dialog, text="Enter Area:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
            obs_method_var = tk.StringVar(value="total")
            obs_method_frame = ttk.Frame(obstacle_dialog)
            obs_method_frame.grid(row=1, column=1, padx=10, pady=10)
            
            ttk.Radiobutton(obs_method_frame, text="Length × Width", variable=obs_method_var, value="lengthwidth").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(obs_method_frame, text="Total sq ft", variable=obs_method_var, value="total").pack(side=tk.LEFT, padx=5)
            
            # Length and Width fields
            obs_length_var = tk.StringVar()
            obs_width_var = tk.StringVar()
            obs_total_var = tk.StringVar()
            
            obs_length_frame = ttk.Frame(obstacle_dialog)
            obs_length_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            
            ttk.Label(obs_length_frame, text="Length (ft):").pack(side=tk.LEFT, padx=5)
            obs_length_entry = ttk.Entry(obs_length_frame, textvariable=obs_length_var, width=10)
            obs_length_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(obs_length_frame, text="Width (ft):").pack(side=tk.LEFT, padx=5)
            obs_width_entry = ttk.Entry(obs_length_frame, textvariable=obs_width_var, width=10)
            obs_width_entry.pack(side=tk.LEFT, padx=5)
            
            obs_total_frame = ttk.Frame(obstacle_dialog)
            obs_total_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5)
            
            ttk.Label(obs_total_frame, text="Total Area (sq ft):").pack(side=tk.LEFT, padx=5)
            obs_total_entry = ttk.Entry(obs_total_frame, textvariable=obs_total_var, width=10)
            obs_total_entry.pack(side=tk.LEFT, padx=5)
            
            def toggle_obstacle_inputs():
                if obs_method_var.get() == "lengthwidth":
                    obs_length_entry.config(state="normal")
                    obs_width_entry.config(state="normal")
                    obs_total_entry.config(state="disabled")
                else:
                    obs_length_entry.config(state="disabled")
                    obs_width_entry.config(state="disabled")
                    obs_total_entry.config(state="normal")
            
            obs_method_var.trace('w', lambda *args: toggle_obstacle_inputs())
            toggle_obstacle_inputs()
            
            def save_obstacle():
                try:
                    name = obs_name_var.get().strip()
                    if not name:
                        messagebox.showerror("Error", "Please enter an obstacle name.")
                        return
                    
                    # Calculate area
                    if obs_method_var.get() == "lengthwidth":
                        length = float(obs_length_var.get())
                        width = float(obs_width_var.get())
                        area = length * width
                    else:
                        area = float(obs_total_var.get())
                    
                    if area >= 0:
                        obstacles.append({"name": name, "area": area})
                        obstacle_list.insert(tk.END, f"{name}: {area} sq ft")
                        obstacle_dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Area must be a positive number.")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers for dimensions.")
            
            btn_frame = ttk.Frame(obstacle_dialog)
            btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
            ttk.Button(btn_frame, text="Save", command=save_obstacle).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancel", command=obstacle_dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        obstacle_btn_frame = ttk.Frame(dialog)
        obstacle_btn_frame.grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(obstacle_btn_frame, text="Add Obstacle", command=add_obstacle).pack(side=tk.LEFT, padx=5)
        
        def toggle_area_inputs():
            if method_var.get() == "lengthwidth":
                length_entry.config(state="normal")
                width_entry.config(state="normal")
                total_entry.config(state="disabled")
            else:
                length_entry.config(state="disabled")
                width_entry.config(state="disabled")
                total_entry.config(state="normal")
        
        method_var.trace('w', lambda *args: toggle_area_inputs())
        toggle_area_inputs()
        
        def save_room():
            try:
                name = name_var.get().strip()
                if not name:
                    messagebox.showerror("Error", "Please enter a room name.")
                    return
                
                # Calculate total area
                if method_var.get() == "lengthwidth":
                    length = float(length_var.get())
                    width = float(width_var.get())
                    total_area = length * width
                else:
                    total_area = float(total_var.get())
                
                # Create room
                room = Room(name, total_area)
                for obs in obstacles:
                    room.obstacles.append(Obstacle(obs["name"], obs["area"]))
                
                self.job.rooms.append(room)
                self.update_rooms_list()
                self.update_cost_summary()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for dimensions.")
        
        room_btn_frame = ttk.Frame(dialog)
        room_btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        ttk.Button(room_btn_frame, text="Save", command=save_room).pack(side=tk.LEFT, padx=5)
        ttk.Button(room_btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_room_dialog(self):
        """Edit selected room"""
        selection = self.rooms_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a room to edit.")
            return
        
        index = selection[0]
        room = self.job.rooms[index]
        
        # For now, just remove and re-add (can be enhanced later)
        self.job.rooms.pop(index)
        self.update_rooms_list()
        self.add_room_dialog()
    
    def remove_room(self):
        """Remove selected room"""
        selection = self.rooms_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a room to remove.")
            return
        
        if messagebox.askyesno("Confirm", "Remove this room?"):
            index = selection[0]
            self.job.rooms.pop(index)
            self.update_rooms_list()
            self.update_cost_summary()
    
    def add_employee_dialog(self):
        """Open dialog to add a new employee"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Employee")
        dialog.geometry("350x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=25).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Hourly Rate ($):").grid(row=1, column=0, padx=10, pady=10)
        rate_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=rate_var, width=25).grid(row=1, column=1, padx=10, pady=10)
        
        def save_employee():
            try:
                name = name_var.get().strip()
                rate = float(rate_var.get())
                if name and rate >= 0:
                    self.job.employees.append(Employee(name, rate))
                    self.update_employees_list()
                    self.update_cost_summary()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid name and rate.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for hourly rate.")
        
        emp_btn_frame = ttk.Frame(dialog)
        emp_btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(emp_btn_frame, text="Save", command=save_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(emp_btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_employee_dialog(self):
        """Edit selected employee"""
        selection = self.employees_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select an employee to edit.")
            return
        
        index = selection[0]
        employee = self.job.employees[index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Employee")
        dialog.geometry("350x180")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar(value=employee.name)
        ttk.Entry(dialog, textvariable=name_var, width=25).grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Hourly Rate ($):").grid(row=1, column=0, padx=10, pady=10)
        rate_var = tk.StringVar(value=str(employee.hourly_rate))
        ttk.Entry(dialog, textvariable=rate_var, width=25).grid(row=1, column=1, padx=10, pady=10)
        
        def save_employee():
            try:
                name = name_var.get().strip()
                rate = float(rate_var.get())
                if name and rate >= 0:
                    self.job.employees[index].name = name
                    self.job.employees[index].hourly_rate = rate
                    self.update_employees_list()
                    self.update_cost_summary()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid name and rate.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for hourly rate.")
        
        edit_emp_btn_frame = ttk.Frame(dialog)
        edit_emp_btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(edit_emp_btn_frame, text="Save", command=save_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_emp_btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_employee(self):
        """Remove selected employee"""
        selection = self.employees_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select an employee to remove.")
            return
        
        if messagebox.askyesno("Confirm", "Remove this employee?"):
            index = selection[0]
            self.job.employees.pop(index)
            self.update_employees_list()
            self.update_cost_summary()
    
    def update_rooms_list(self):
        """Update rooms listbox display"""
        self.rooms_listbox.delete(0, tk.END)
        for room in self.job.rooms:
            usable = room.get_usable_area()
            self.rooms_listbox.insert(tk.END, f"{room.name}: {usable:.2f} sq ft")
    
    def update_employees_list(self):
        """Update employees listbox display"""
        self.employees_listbox.delete(0, tk.END)
        for emp in self.job.employees:
            self.employees_listbox.insert(tk.END, f"{emp.name}: ${emp.hourly_rate:.2f}/hr")
    
    def update_cost_summary(self):
        """Update cost summary display"""
        try:
            # Update job from UI inputs
            try:
                self.job.days_required = int(self.days_var.get())
            except ValueError:
                self.job.days_required = 0
            
            try:
                self.job.sanding_cost_per_sqft = float(self.sanding_var.get())
            except ValueError:
                self.job.sanding_cost_per_sqft = 0.0
            
            self.job.customer_provides_wood = (self.material_source_var.get() == "customer")
            
            try:
                self.job.material_cost_per_sqft = float(self.material_cost_var.get())
            except ValueError:
                self.job.material_cost_per_sqft = 0.0
            
            try:
                self.job.pickup_fee = float(self.pickup_fee_var.get())
            except ValueError:
                self.job.pickup_fee = 0.0
            
            # Calculate and display
            breakdown = self.job.get_cost_breakdown()
            
            self.total_space_label.config(text=f"{breakdown['total_floor_space_sqft']:.2f} sq ft")
            self.sanding_cost_label.config(text=f"${breakdown['sanding_cost']:,.2f}")
            self.labor_cost_label.config(text=f"${breakdown['labor_cost']:,.2f}")
            self.material_cost_label.config(text=f"${breakdown['material_cost']:,.2f}")
            self.total_cost_label.config(text=f"${breakdown['total_cost']:,.2f}")
        except Exception as e:
            # Silent error handling - just don't update if calculation fails
            pass
    
    def calculate_costs(self):
        """Explicitly calculate and show costs"""
        self.update_cost_summary()
        messagebox.showinfo("Calculation Complete", "Costs have been calculated. See the Cost Summary panel.")
    
    def load_blueprint(self):
        """Load and display blueprint file"""
        filetypes = [
            ("All Supported", "*.pdf *.png *.jpg *.jpeg *.gif *.bmp"),
            ("PDF files", "*.pdf"),
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select Blueprint File",
            filetypes=filetypes
        )
        
        if filepath:
            self.blueprint_path = filepath
            self.display_blueprint_window()
    
    def display_blueprint_window(self):
        """Display blueprint in a separate window"""
        if not self.blueprint_path or not os.path.exists(self.blueprint_path):
            messagebox.showerror("Error", "Blueprint file not found.")
            return
        
        # Close existing blueprint window if open
        if self.blueprint_window:
            self.blueprint_window.destroy()
        
        # Create new window
        self.blueprint_window = tk.Toplevel(self.root)
        self.blueprint_window.title(f"Blueprint: {os.path.basename(self.blueprint_path)}")
        self.blueprint_window.geometry("800x600")
        
        try:
            is_pdf = self.blueprint_path.lower().endswith('.pdf')
            
            if is_pdf:
                # Handle PDF
                try:
                    import fitz  # PyMuPDF
                    pdf_doc = fitz.open(self.blueprint_path)
                    first_page = pdf_doc[0]
                    
                    zoom = 1.5
                    mat = fitz.Matrix(zoom, zoom)
                    pix = first_page.get_pixmap(matrix=mat)
                    
                    from PIL import Image, ImageTk
                    img_data = pix.tobytes("ppm")
                    img = Image.open(io.BytesIO(img_data))
                    
                    pdf_doc.close()
                except ImportError:
                    messagebox.showinfo("Info", "PyMuPDF not installed. Install with: pip install pymupdf to view PDFs in the GUI.\n\nOpening in system viewer instead.")
                    import subprocess
                    import platform
                    if platform.system() == 'Darwin':
                        subprocess.Popen(['open', self.blueprint_path])
                    elif platform.system() == 'Windows':
                        os.startfile(self.blueprint_path)
                    else:
                        subprocess.Popen(['xdg-open', self.blueprint_path])
                    self.blueprint_window.destroy()
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Could not load PDF: {e}")
                    self.blueprint_window.destroy()
                    return
            else:
                # Handle image files
                from PIL import Image, ImageTk
                img = Image.open(self.blueprint_path)
            
            # Resize image to fit window while maintaining aspect ratio
            window_width = 780
            window_height = 560
            img.thumbnail((window_width, window_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for Tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Display image
            label = tk.Label(self.blueprint_window, image=photo)
            label.image = photo  # Keep a reference
            label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add info label
            info_text = f"File: {os.path.basename(self.blueprint_path)}\nUse this as reference while entering room measurements."
            info_label = ttk.Label(self.blueprint_window, text=info_text, font=("", 9))
            info_label.pack(pady=5)
            
        except ImportError:
            messagebox.showerror("Error", "PIL/Pillow not installed. Install with: pip install pillow")
            self.blueprint_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load blueprint: {e}")
            if self.blueprint_window:
                self.blueprint_window.destroy()
    
    def clear_all(self):
        """Clear all inputs"""
        if messagebox.askyesno("Confirm", "Clear all data? This cannot be undone."):
            self.job = FlooringJob()
            self.days_var.set("0")
            self.sanding_var.set("0.00")
            self.material_source_var.set("customer")
            self.material_cost_var.set("0.00")
            self.pickup_fee_var.set("0.00")
            self.update_rooms_list()
            self.update_employees_list()
            self.update_cost_summary()
            self.toggle_material_fields()


def main():
    root = tk.Tk()
    app = FlooringCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


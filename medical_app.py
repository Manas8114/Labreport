import tkinter as tk
from tkinter import ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MedicalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Test Data")
        
        light_green_color = "#cdeccd"  
        self.root.configure(bg=light_green_color)

        button_color = "#a6a6a6"
        self.tab_control = ttk.Notebook(root)
        self.tabs_and_fields = {
            'ID': ['P_no', 'Name', 'Sex', 'Age'],
            'HAEMATOLOGY': [
                'Hb', 'TLC', 'DLC', 'N__L__E__M', 'RBC', 'Hematocrit', 'MCV', 'MCH', 'MCHC',
                'PLT_Count', 'E_S_R_Wester_Green', 'Bleeding_time', 'Cloting_time',
                'Sickle_sell_solubility_Electrophoresis', 'MP', 'MANTOUX_TEST_Erytheama_Induration',
                'V_D_R_L', 'R_A_Factor', 'ASO_Titre', 'C_R_P_HbSag', 'HIV', 'WIDAL_0_1',
                'Typhoid_Card_Test', 'Blood_Group_Rh', 'TROP_I', 'COVID_19_Antigen_Test',
                'Pengae_Test_HCV'
            ],
            'URINE_EXAMINATION': ['PH', 'BIL', 'KET', 'BLD', 'PRO', 'Malb', 'NIT', 'LEU', 'GLLU', 'SGUPT'],
            'BIOCHEMISTRY': [
                'Bl_Suger_F_R_HbA1c', 'Bl_Urea', 'Sr_Creatinine', 'Sr_Calcium_cloride', 'Sodium',
                'Potassium', 'S_Lipase', 'S_Amylase', 'Uric_Acid'
            ],
            'LIPID_PROFILE': ['S_Cholesterol', 'HDL_Cholesterol', 'LDL_Cholesterol', 'VLDL_Cholesterol', 'Triglycerides', 'Torch_Test'],
            'LIVER_FUNCTION_TEST': [
                'S_Billirubin', 'Direct', 'Indirect', 'S_G_O_T', 'S_G_P_T', 'Alk_Phosphatase',
                'Total_Protein', 'Total_Albumin', 'Total_Globulin', 'Acid_Phosphatase'
            ],
            'Report_of_Examination_of_Semen': [
                'Volume', 'Liquifaction_Time', 'Microscopic_Exa', 'Sperm_Count',
                'Sperm_Motility_active_Motile', 'Sperm_Motility_slugish_Motile', 'Sperm_Motility_Dead',
                'Pus_cells', 'Epi_cell', 'RBCs', 'Sputum_AFB'
            ]            
        }

        self.data_entries = {}
        for tab_name, data_fields in self.tabs_and_fields.items():
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=tab_name)
            self.data_entries[tab_name] = []

            for field in data_fields:
                row = tk.Frame(tab)
                label = tk.Label(row, width=15, text=field, anchor='w')
                entry = tk.Entry(row)
                row.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)
                label.pack(side=tk.LEFT)
                entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                self.data_entries[tab_name].append(entry)

            self.bind_enter_key(tab_name)

        self.button_frame = tk.Frame(root, bg=light_green_color)
        self.save_button = tk.Button(self.button_frame, text='Save Data to Database', command=self.save_data, bg=button_color)
        self.print_button = tk.Button(self.button_frame, text='Print Entered Data', command=self.print_data, bg=button_color)
        self.show_output_button = tk.Button(self.button_frame, text='Show Output', command=self.show_output, bg=button_color)
        self.show_chart_button = tk.Button(self.button_frame, text='Show Chart', command=self.show_chart, bg=button_color)

        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.print_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.show_output_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.show_chart_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tab_control.pack(expand=1, fill='both')

        self.output_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.output_tab, text='Output')
        self.output_text = tk.Text(self.output_tab, height=40, width=80)
        self.output_text.pack()

    def bind_enter_key(self, tab_name):
        for i in range(len(self.data_entries[tab_name])):
            self.data_entries[tab_name][i].bind('<Return>', lambda event, i=i: self.move_to_next_entry(tab_name, i))
    
    def save_data(self):
        current_tab_name = self.tab_control.tab(self.tab_control.select(), 'text')
        
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='hospital'
        )
        cursor = connection.cursor()

        table_name = current_tab_name.replace(' ', '_')

        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join([f'{field} TEXT' for field in self.tabs_and_fields[current_tab_name]])}
            )
        ''')

        data_values = [entry.get() for entry in self.data_entries[current_tab_name]]
        columns = ', '.join(self.tabs_and_fields[current_tab_name])
        placeholders = ', '.join(['%s' for _ in self.tabs_and_fields[current_tab_name]])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data_values))

        connection.commit()
        connection.close()

        self.move_to_next_tab(current_tab_name)

    def print_data(self):
        current_tab_name = self.tab_control.tab(self.tab_control.select(), 'text')
        data_values = [entry.get() for entry in self.data_entries[current_tab_name]]
        print(f"Entered Data for {current_tab_name}:", data_values)

    def show_output(self):
        current_tab_name = self.tab_control.tab(self.tab_control.select(), 'text')
        id_tab_name = 'ID'
    
        id_data_values = [entry.get() for entry in self.data_entries[id_tab_name]]
        id_output_data = f"SANJIVANI HOSPITAL {id_tab_name}:\n"
        for field, value in zip(self.tabs_and_fields[id_tab_name], id_data_values):
            id_output_data += f"{field}: {value}\n"
    
        data_values = [entry.get() for entry in self.data_entries[current_tab_name]]
        output_data = f"\nEntered Data for {current_tab_name}:\n"
        for field, value in zip(self.tabs_and_fields[current_tab_name], data_values):
            output_data += f"{field}: {value}\n"
    
        final_output = id_output_data + output_data
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, final_output)


    def show_chart(self):
        current_tab_name = self.tab_control.tab(self.tab_control.select(), 'text')
        data_values = [float(entry.get()) for entry in self.data_entries[current_tab_name]]
        fields = self.tabs_and_fields[current_tab_name]

        fig, ax = plt.subplots()
        ax.bar(fields, data_values)
        ax.set_xlabel('Fields')
        ax.set_ylabel('Values')
        ax.set_title(f'Chart for {current_tab_name}')
        
        canvas = FigureCanvasTkAgg(fig, master=self.output_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.move_to_next_tab(current_tab_name)

    def move_to_next_tab(self, current_tab_name):
        current_tab_index = list(self.tabs_and_fields.keys()).index(current_tab_name)    
        next_tab_index = (current_tab_index + 1) % len(self.tabs_and_fields)
        next_tab_index = next_tab_index if next_tab_index < len(self.tabs_and_fields) else 0
        self.tab_control.select(next_tab_index)

    def move_to_next_entry(self, tab_name, current_entry_index):
        next_entry_index = (current_entry_index + 1) % len(self.data_entries[tab_name])
        self.data_entries[tab_name][next_entry_index].focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalApp(root)
    root.mainloop()
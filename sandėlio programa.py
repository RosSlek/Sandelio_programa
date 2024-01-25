import pandas as pd
import datetime
import tkinter.messagebox
import customtkinter
import pandastable as pt
from CTkMessagebox import CTkMessagebox
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap('_internal\icon.ico')
        self.title("Sandėlio programa")
        self.geometry("410x470")
        self.resizable(width=False, height=False)
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.button_1 = customtkinter.CTkButton(self, text="Sandėlio papildymas", command=self.papildyti_sandeli, width=200, height=30)
        self.button_1.pack(side="top", pady=10)

        self.button_2 = customtkinter.CTkButton(self, text="Perkelti medžiagas į gamybą", command=self.perkelti_is_sandelio, width=200, height=30)
        self.button_2.pack(side="top", pady=10)

        self.button_3 = customtkinter.CTkButton(self, text="Medžiagų likučiai sandėlyje", command=self.sandelio_likutis, width=200, height=30)
        self.button_3.pack(side="top", pady=10)

        self.button_4 = customtkinter.CTkButton(self, text="Medžiagų likučiai gamyboje", command=self.gamybos_likutis, width=200, height=30)
        self.button_4.pack(side="top", pady=10)

        self.button_5 = customtkinter.CTkButton(self, text="Gamybos darbų registras", command=self.darbu_registras, width=200, height=30)
        self.button_5.pack(side="top", pady=10)

        self.button_9 = customtkinter.CTkButton(self, text="Peržiūrėti gamybos darbų registrą", command=self.gamybos_registras, width=200, height=30)
        self.button_9.pack(side="top", pady=10)

        self.button_6 = customtkinter.CTkButton(self, text="Išeiti", command=self.destroy, width=200, height=30)
        self.button_6.pack(side="top", pady=10)

        self.button_7 = customtkinter.CTkSwitch(self, text="Pakeisti likučių lango vaizdą", onvalue="on", offvalue="off")
        self.button_7.place(x=15, y=430)

        self.button_8 = customtkinter.CTkSwitch(self, text="Šviesusis režimas", command=self.mode, onvalue="light", offvalue="dark")
        self.button_8.place(x=255, y=430)

        self.toplevel_window = None

    def mode(self):
        if self.button_8.get() == "light":
            customtkinter.set_appearance_mode("light")
        elif self.button_8.get() == "dark":
            customtkinter.set_appearance_mode("dark")

    def sandelio_likutis(self):

        try:
            duomenys = open("_internal\duomenu baze.txt", "r")
            duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            user = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            password = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            host = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            port = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            duomenys.close()

            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{duomenu_baze}')

            df = pd.read_sql('sandelio_istorija', engine)

            df.rename(columns={'partijos_numeris': 'Partijos numeris'}, inplace=True)
            df.rename(columns={'polietileno_plėvelė_0_85x50m': 'Polietileno plėvelė 0.85x50m'}, inplace=True)
            df.rename(columns={'hidroizoliacinė_plėvelė_0_65x45m': 'Hidroizoliacinė plėvelė 0.65x45m'}, inplace=True)
            df.rename(columns={'sausas_tinko_mišinys_2_5kg': 'Sausas tinko mišinys 2.5kg'}, inplace=True)
            df.rename(columns={'cementinis_mišinys_4kg': 'Cementinis mišinys 4kg'}, inplace=True)
            df["Polietileno plėvelė 0.85x50m"] = pd.to_numeric(df["Polietileno plėvelė 0.85x50m"])
            df["Hidroizoliacinė plėvelė 0.65x45m"] = pd.to_numeric(df["Hidroizoliacinė plėvelė 0.65x45m"])
            df["Sausas tinko mišinys 2.5kg"] = pd.to_numeric(df["Sausas tinko mišinys 2.5kg"])
            df["Cementinis mišinys 4kg"] = pd.to_numeric(df["Cementinis mišinys 4kg"])

            df1 = df.groupby('Partijos numeris')['Polietileno plėvelė 0.85x50m'].sum().round(2).reset_index()
            df2 = df.groupby('Partijos numeris')['Hidroizoliacinė plėvelė 0.65x45m'].sum().round(2).reset_index()
            df2.drop(columns=['Partijos numeris'], inplace=True)
            df3 = df.groupby('Partijos numeris')['Sausas tinko mišinys 2.5kg'].sum().round(2).reset_index()
            df3.drop(columns=['Partijos numeris'], inplace=True)
            df4 = df.groupby('Partijos numeris')['Cementinis mišinys 4kg'].sum().round(2).reset_index()
            df4.drop(columns=['Partijos numeris'], inplace=True)

            if self.button_7.get() == "on":
                df_likuciai = pd.concat([df1, df2, df3, df4], axis=1)
                df_likuciai.set_index('Partijos numeris', inplace=True)
                df_likuciai = df_likuciai.transpose().reset_index()
                df_likuciai.rename(columns={'index': 'Medžiaga'}, inplace=True)
                df_likuciai = df_likuciai.melt(id_vars=["Medžiaga"], var_name="Partijos numeris", value_name="Likutis")
                df_likuciai = df_likuciai[df_likuciai.Likutis != 0]

                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Medžiagų likučiai sandėlyje')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()

            elif self.button_7.get() == "off":

                df_likuciai = pd.concat([df1, df2, df3, df4], axis=1)

                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Medžiagų likučiai sandėlyje')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()
        except:
            CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

    def gamybos_likutis(self):
        try:
            duomenys = open("_internal\duomenu baze.txt", "r")
            duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            user = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            password = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            host = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            port = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            duomenys.close()

            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{duomenu_baze}')

            df = pd.read_sql('gamybos_istorija', engine)

            df.rename(columns={'medžiagos_id': 'Medžiagos ID'}, inplace=True)
            df.rename(columns={'polietileno_plėvelė_m': 'Polietileno plėvelė, m'}, inplace=True)
            df.rename(columns={'hidroizoliacinė_plėvelė_m': 'Hidroizoliacinė plėvelė, m'}, inplace=True)
            df.rename(columns={'sausas_tinko_mišinys_kg': 'Sausas tinko mišinys, kg'}, inplace=True)
            df.rename(columns={'cementinis_mišinys_kg': 'Cementinis mišinys, kg'}, inplace=True)
            df["Polietileno plėvelė, m"] = pd.to_numeric(df["Polietileno plėvelė, m"])
            df["Hidroizoliacinė plėvelė, m"] = pd.to_numeric(df["Hidroizoliacinė plėvelė, m"])
            df["Sausas tinko mišinys, kg"] = pd.to_numeric(df["Sausas tinko mišinys, kg"])
            df["Cementinis mišinys, kg"] = pd.to_numeric(df["Cementinis mišinys, kg"])

            df1 = df.groupby('Medžiagos ID')['Polietileno plėvelė, m'].sum().round(2).reset_index()
            df2 = df.groupby('Medžiagos ID')['Hidroizoliacinė plėvelė, m'].sum().round(2).reset_index()
            df2.drop(columns=['Medžiagos ID'], inplace=True)
            df3 = df.groupby('Medžiagos ID')['Sausas tinko mišinys, kg'].sum().round(2).reset_index()
            df3.drop(columns=['Medžiagos ID'], inplace=True)
            df4 = df.groupby('Medžiagos ID')['Cementinis mišinys, kg'].sum().round(2).reset_index()
            df4.drop(columns=['Medžiagos ID'], inplace=True)

            if self.button_7.get() == "on":
                df_likuciai = pd.concat([df1, df2, df3, df4], axis=1)
                df_likuciai.set_index('Medžiagos ID', inplace=True)
                df_likuciai = df_likuciai.transpose().reset_index()
                df_likuciai.rename(columns={'index': 'Medžiaga'}, inplace=True)
                df_likuciai = df_likuciai.melt(id_vars=["Medžiaga"], var_name="Medžiagos ID", value_name="Likutis")
                df_likuciai = df_likuciai[df_likuciai.Likutis != 0]

                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Medžiagų likučiai gamyboje')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()

            elif self.button_7.get() == "off":
                df_likuciai = pd.concat([df1, df2, df3, df4], axis=1)

                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Medžiagų likučiai gamyboje')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()
        except:
            CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

    def gamybos_registras(self):
        try:
            duomenys = open("_internal\duomenu baze.txt", "r")
            duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            user = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            password = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            host = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            port = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
            duomenys.close()

            engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{duomenu_baze}')

            df = pd.read_sql('gamybos_darbu_registras', engine)

            df.rename(columns={'papildoma_informacija': 'Papildoma informacija'}, inplace=True)
            df.rename(columns={'užsakymo_numeris': 'Užsakymo numeris'}, inplace=True)
            df.rename(columns={'polietileno_plėvelė_m': 'Polietileno plėvelė, m'}, inplace=True)
            df.rename(columns={'hidroizoliacinė_plėvelė_m': 'Hidroizoliacinė plėvelė, m'}, inplace=True)
            df.rename(columns={'sausas_tinko_mišinys_kg': 'Sausas tinko mišinys, kg'}, inplace=True)
            df.rename(columns={'cementinis_mišinys_kg': 'Cementinis mišinys, kg'}, inplace=True)
            df["Polietileno plėvelė, m"] = pd.to_numeric(df["Polietileno plėvelė, m"])
            df["Hidroizoliacinė plėvelė, m"] = pd.to_numeric(df["Hidroizoliacinė plėvelė, m"])
            df["Sausas tinko mišinys, kg"] = pd.to_numeric(df["Sausas tinko mišinys, kg"])
            df["Cementinis mišinys, kg"] = pd.to_numeric(df["Cementinis mišinys, kg"])

            df['Papildoma informacija'] = df['Papildoma informacija'].astype(str)
            df1 = df.groupby('Užsakymo numeris')['Polietileno plėvelė, m'].sum().round(2).reset_index()
            df2 = df.groupby('Užsakymo numeris')['Hidroizoliacinė plėvelė, m'].sum().round(2).reset_index()
            df2.drop(columns=['Užsakymo numeris'], inplace=True)
            df3 = df.groupby('Užsakymo numeris')['Sausas tinko mišinys, kg'].sum().round(2).reset_index()
            df3.drop(columns=['Užsakymo numeris'], inplace=True)
            df4 = df.groupby('Užsakymo numeris')['Cementinis mišinys, kg'].sum().round(2).reset_index()
            df4.drop(columns=['Užsakymo numeris'], inplace=True)
            df5 = df.groupby('Užsakymo numeris')['Papildoma informacija'].apply(lambda x: 'x'.join(x)).reset_index()
            df5 = df5['Papildoma informacija'].str.replace('Nan', '')
            df5 = df5.str.replace('Nan', '')
            df5 = df5.str.replace(' ', '')
            df5 = df5.str.replace('x', ' ')

            if self.button_7.get() == "on":
                df_likuciai = pd.concat([df1, df2, df3, df4], axis=1)
                df_likuciai.set_index('Užsakymo numeris', inplace=True)
                df_likuciai = df_likuciai.transpose().reset_index()
                df_likuciai.rename(columns={'index': 'Medžiaga'}, inplace=True)
                df_likuciai = df_likuciai.melt(id_vars=["Medžiaga"], var_name="Užsakymo numeris", value_name="Sunaudota")
                df_likuciai = df_likuciai[df_likuciai.Sunaudota != 0]

                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Gamybos darbų registras')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()

            elif self.button_7.get() == "off":
                df_likuciai = pd.concat([df1, df2, df3, df4, df5], axis=1)
                dTDa1 = tkinter.Toplevel()
                dTDa1.iconbitmap('_internal\icon.ico')
                dTDa1.title('Gamybos darbų registras')
                dTDaPT = pt.Table(dTDa1, dataframe=df_likuciai, showtoolbar=True, showstatusbar=True)
                dTDaPT.show()
        except:
            CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

    def papildyti_sandeli(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Pridejimo_langas()
        else:
            self.toplevel_window.focus()

    def perkelti_is_sandelio(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Nurasymo_is_sandelio_langas()

        else:
            self.toplevel_window.focus()

    def darbu_registras(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Darbu_registro_langas()
        else:
            self.toplevel_window.focus()

class Pridejimo_langas(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.after(100, lambda: self.focus())
        self.after(205, lambda: self.iconbitmap('_internal\icon.ico'))
        self.geometry("400x400")
        self.resizable(width=False, height=False)
        self.title("Sandėlio papildymas")
        self.label = customtkinter.CTkLabel(self, text="Pasirinkite pildomą medžiagą")
        self.label.pack(padx=10, pady=10)

        self.button_1 = customtkinter.CTkComboBox(self, values=['Polietileno plėvelė', 'Hidroizoliacinė plėvelė', 'Sausas tinko mišinys', 'Cementinis mišinys'])
        self.button_1.pack(side="top", padx=20, pady=10)

        self.button_2 = customtkinter.CTkEntry(self, placeholder_text="Įveskite pildomą kiekį")
        self.button_2.pack(side="top", padx=20, pady=10)

        self.button_3 = customtkinter.CTkEntry(self, placeholder_text="Partijos numeris")
        self.button_3.pack(side="top", padx=20, pady=10)

        self.button_4 = customtkinter.CTkEntry(self, placeholder_text="Atsakingas asmuo")
        self.button_4.pack(side="top", padx=20, pady=10)

        self.button_7 = customtkinter.CTkEntry(self, placeholder_text="Papildoma informacija")
        self.button_7.pack(side="top", padx=20, pady=10)

        self.button_5 = customtkinter.CTkButton(self, text="Pildyti", command=self.pildymas)
        self.button_5.pack(side="top", padx=20, pady=10)

    def pildymas(self):
        naudotas = self.button_2.get()
        numeris = self.button_3.get()
        zmogus = self.button_4.get()
        komentaras = self.button_7.get()
        if self.button_1.get() == 'Polietileno plėvelė' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "":
            medziaga = self.button_1.get()
            prideti_medziaga(medziaga, naudotas, numeris, zmogus, komentaras)
        elif self.button_1.get() == 'Hidroizoliacinė plėvelė' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "":
            medziaga = self.button_1.get()
            prideti_medziaga(medziaga, naudotas, numeris, zmogus, komentaras)
        elif self.button_1.get() == 'Sausas tinko mišinys' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "":
            medziaga = self.button_1.get()
            prideti_medziaga(medziaga, naudotas, numeris, zmogus, komentaras)
        elif self.button_1.get() == 'Cementinis mišinys' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "":
            medziaga = self.button_1.get()
            prideti_medziaga(medziaga, naudotas, numeris, zmogus, komentaras)
        else:
            CTkMessagebox(title="Error", message="Patikrinkite įvestus duomenis!", icon="cancel")

class Nurasymo_is_sandelio_langas(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.after(100, lambda: self.focus())
        self.after(205, lambda: self.iconbitmap('_internal\icon.ico'))
        self.geometry("400x450")
        self.resizable(width=False, height=False)

        self.title("Perkelti medžiagas į gamybą")
        self.label = customtkinter.CTkLabel(self, text="Pasirinkite perkeliamą medziagą")
        self.label.pack(padx=10, pady=10)

        self.button_1 = customtkinter.CTkComboBox(self, values=['Polietileno plėvelė', 'Hidroizoliacinė plėvelė', 'Sausas tinko mišinys', 'Cementinis mišinys'])
        self.button_1.pack(side="top", padx=20, pady=10)

        self.button_2 = customtkinter.CTkEntry(self, placeholder_text="Kiekis")
        self.button_2.pack(side="top", padx=20, pady=10)

        self.button_3 = customtkinter.CTkEntry(self, placeholder_text="Partijos numeris")
        self.button_3.pack(side="top", padx=20, pady=10)

        self.button_7 = customtkinter.CTkEntry(self, placeholder_text="Medžiagos ID")
        self.button_7.pack(side="top", padx=20, pady=10)

        self.button_4 = customtkinter.CTkEntry(self, placeholder_text="Atsakingas asmuo")
        self.button_4.pack(side="top", padx=20, pady=10)

        self.button_8 = customtkinter.CTkEntry(self, placeholder_text="Papildoma informacija")
        self.button_8.pack(side="top", padx=20, pady=10)

        self.button_5 = customtkinter.CTkButton(self, text="Perkelti", command=self.perkelimas)
        self.button_5.pack(side="top", padx=20, pady=10)

    def perkelimas(self):
        naudotas = self.button_2.get()
        numeris = self.button_3.get()
        zmogus = self.button_4.get()
        komentaras = self.button_8.get()
        serijos_nr_spaudejo = self.button_7.get()
        if self.button_1.get() == 'Polietileno plėvelė' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "" and self.button_7.get() != "":
            medziaga = self.button_1.get()
            atimti_medziaga_is_sandelio(medziaga, naudotas, numeris, zmogus, serijos_nr_spaudejo, komentaras)
        elif self.button_1.get() == 'Hidroizoliacinė plėvelė' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "" and self.button_7.get() != "":
            medziaga = self.button_1.get()
            atimti_medziaga_is_sandelio(medziaga, naudotas, numeris, zmogus, serijos_nr_spaudejo, komentaras)
        elif self.button_1.get() == 'Sausas tinko mišinys' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "" and self.button_7.get() != "":
            medziaga = self.button_1.get()
            atimti_medziaga_is_sandelio(medziaga, naudotas, numeris, zmogus, serijos_nr_spaudejo, komentaras)
        elif self.button_1.get() == 'Cementinis mišinys' and self.button_2.get() != "" and self.button_3.get() != "" and self.button_4.get() != "" and self.button_7.get() != "":
            medziaga = self.button_1.get()
            atimti_medziaga_is_sandelio(medziaga, naudotas, numeris, zmogus, serijos_nr_spaudejo, komentaras)
        else:
            CTkMessagebox(title="Error", message="Patikrinkite įvestus duomenis!", icon="cancel")

class Darbu_registro_langas(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.after(100, lambda: self.focus())
        self.after(205, lambda: self.iconbitmap('_internal\icon.ico'))
        self.geometry("400x450")
        self.resizable(width=False, height=False)

        self.title("Gamybos darbų registras")
        self.label = customtkinter.CTkLabel(self, text="Pasirinkite sunaudotą medžiagą")
        self.label.pack(padx=10, pady=10)

        self.button_1 = customtkinter.CTkComboBox(self, values=['Polietileno plėvelė', 'Hidroizoliacinė plėvelė', 'Sausas tinko mišinys', 'Cementinis mišinys'])
        self.button_1.pack(side="top", padx=20, pady=10)

        self.button_2 = customtkinter.CTkEntry(self, placeholder_text="Įveskite kiekį")
        self.button_2.pack(side="top", padx=20, pady=10)

        self.button_7 = customtkinter.CTkEntry(self, placeholder_text="Medžiagos ID")
        self.button_7.pack(side="top", padx=20, pady=10)

        self.button_3 = customtkinter.CTkEntry(self, placeholder_text="Užsakymo numeris")
        self.button_3.pack(side="top", padx=20, pady=10)

        self.button_4 = customtkinter.CTkEntry(self, placeholder_text="Atsakingas asmuo")
        self.button_4.pack(side="top", padx=20, pady=10)

        self.button_8 = customtkinter.CTkEntry(self, placeholder_text="Papildoma informacija")
        self.button_8.pack(side="top", padx=20, pady=10)

        self.button_5 = customtkinter.CTkButton(self, text="Registruoti", command=self.nurasymas)
        self.button_5.pack(side="top", padx=20, pady=10)

    def nurasymas(self):
        naudotas = self.button_2.get()
        zmogus = self.button_4.get()
        serijos_nr_spaudejo = self.button_7.get()
        uzsakymo_nr = self.button_3.get()
        komentaras = self.button_8.get()
        if self.button_1.get() == 'Polietileno plėvelė' and self.button_2.get() != "" and self.button_4.get() != "" and self.button_7.get() != "" and self.button_3.get() != "":
            medziaga = self.button_1.get()
            uzsakyme_panaudota_medziaga(medziaga, naudotas, zmogus, serijos_nr_spaudejo, uzsakymo_nr, komentaras)
        elif self.button_1.get() == 'Hidroizoliacinė plėvelė' and self.button_2.get() != "" and self.button_4.get() != "" and self.button_7.get() != "" and self.button_3.get() != "":
            medziaga = self.button_1.get()
            uzsakyme_panaudota_medziaga(medziaga, naudotas, zmogus, serijos_nr_spaudejo, uzsakymo_nr, komentaras)
        elif self.button_1.get() == 'Sausas tinko mišinys' and self.button_2.get() != "" and self.button_4.get() != "" and self.button_7.get() != "" and self.button_3.get() != "":
            medziaga = self.button_1.get()
            uzsakyme_panaudota_medziaga(medziaga, naudotas, zmogus, serijos_nr_spaudejo, uzsakymo_nr, komentaras)
        elif self.button_1.get() == 'Cementinis mišinys' and self.button_2.get() != "" and self.button_4.get() != "" and self.button_7.get() != "" and self.button_3.get() != "":
            medziaga = self.button_1.get()
            uzsakyme_panaudota_medziaga(medziaga, naudotas, zmogus, serijos_nr_spaudejo, uzsakymo_nr, komentaras)
        else:
            CTkMessagebox(title="Error", message="Patikrinkite įvestus duomenis!", icon="cancel")

def prideti_medziaga(medziaga, naudotas, numeris, zmogus, komentaras):
    try:
        duomenys = open("_internal\duomenu baze.txt", "r")
        duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        duomenys.close()
        medziaga1 = 0
        medziaga2 = 0
        medziaga3 = 0
        medziaga4 = 0
        today = datetime.datetime.today()
        today = today.strftime("%Y-%m-%d %H:%M:%S")
        kiekis = int(naudotas)
        if medziaga == "Polietileno plėvelė":
            medziaga1 = medziaga1 + (kiekis)
        elif medziaga == "Hidroizoliacinė plėvelė":
            medziaga2 = medziaga2 + (kiekis)
        elif medziaga == "Sausas tinko mišinys":
            medziaga3 = medziaga3 + (kiekis)
        elif medziaga == "Cementinis mišinys":
            medziaga4 = medziaga4 + (kiekis)

        conn = psycopg2.connect(database=duomenu_baze, user='postgres', password='PGadmin', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql.SQL('''INSERT INTO {} values (%s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier('sandelio_istorija')),[medziaga1, medziaga2, medziaga3, medziaga4, numeris, zmogus, today, komentaras])

        conn.commit()
        conn.close()

        CTkMessagebox(title="Info", message="Sandėlys sėkmingai papildytas")

    except ValueError:
        CTkMessagebox(title="Error", message="Sandėlio pildymo kiekis turi būti sveikasis skaičius!", icon="cancel")
    except:
        CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

def atimti_medziaga_is_sandelio(medziaga, naudotas, numeris, zmogus, serijos_nr_spaudejo, komentaras):
    try:
        duomenys = open("_internal\duomenu baze.txt", "r")
        duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        duomenys.close()
        medziaga1 = 0
        medziaga2 = 0
        medziaga3 = 0
        medziaga4 = 0
        today = datetime.datetime.today()
        today = today.strftime("%Y-%m-%d %H:%M:%S")
        kiekis = -abs(int(naudotas))
        if medziaga == "Polietileno plėvelė":
            medziaga1 = medziaga1 + (kiekis)
        elif medziaga == "Hidroizoliacinė plėvelė":
            medziaga2 = medziaga2 + (kiekis)
        elif medziaga == "Sausas tinko mišinys":
            medziaga3 = medziaga3 + (kiekis)
        elif medziaga == "Cementinis mišinys":
            medziaga4 = medziaga4 + (kiekis)

        conn = psycopg2.connect(database=duomenu_baze, user='postgres', password='PGadmin', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql.SQL('''INSERT INTO {} values (%s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier('sandelio_istorija')),[medziaga1, medziaga2, medziaga3, medziaga4, numeris, zmogus, today, komentaras])

        medziaga1 = medziaga1 *-30
        medziaga2 = medziaga2 * -45
        medziaga3 = medziaga3 * -2.5
        medziaga4 = medziaga4 * -4

        cursor.execute(sql.SQL('''INSERT INTO {} values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier('gamybos_istorija')),[medziaga1, medziaga2, medziaga3, medziaga4, numeris, serijos_nr_spaudejo, zmogus, today, komentaras])
        conn.commit()
        conn.close()

        CTkMessagebox(title="Info", message="Perkeliamos medžiagos sėkmingai užregistruotos")

    except ValueError:
        # CTkMessagebox(title="Error", message="Patikrinkite įvestus duomenis!", icon="cancel")
        CTkMessagebox(title="Error", message="Nurašomas kiekis turi būti sveikasis skaičius!", icon="cancel")
    except:
        CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

def uzsakyme_panaudota_medziaga(medziaga, naudotas, zmogus, serijos_nr_spaudejo, aprasymas, komentaras):
    try:
        duomenys = open("_internal\duomenu baze.txt", "r")
        duomenu_baze = duomenys.readline().split(sep=': ')[1].split(sep='\n')[0]
        duomenys.close()
        medziaga1 = 0
        medziaga2 = 0
        medziaga3 = 0
        medziaga4 = 0
        serijos_nr = 0
        today = datetime.datetime.today()
        today = today.strftime("%Y-%m-%d %H:%M:%S")
        kiekis = -abs(float(naudotas))
        if medziaga == "Polietileno plėvelė":
            medziaga1 = medziaga1 + (kiekis)
        elif medziaga == "Hidroizoliacinė plėvelė":
            medziaga2 = medziaga2 + (kiekis)
        elif medziaga == "Sausas tinko mišinys":
            medziaga3 = medziaga3 + (kiekis)
        elif medziaga == "Cementinis mišinys":
            medziaga4 = medziaga4 + (kiekis)

        conn = psycopg2.connect(database=duomenu_baze, user='postgres', password='PGadmin', host='localhost', port='5432')
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql.SQL('''INSERT INTO {} values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier('gamybos_istorija')),[medziaga1, medziaga2, medziaga3, medziaga4, serijos_nr, serijos_nr_spaudejo, zmogus, today, komentaras])

        medziaga1 = medziaga1 * -1
        medziaga2 = medziaga2 * -1
        medziaga3 = medziaga3 * -1
        medziaga4 = medziaga4 * -1

        cursor.execute(sql.SQL('''INSERT INTO {} values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''').format(sql.Identifier('gamybos_darbu_registras')),[aprasymas, medziaga1, medziaga2, medziaga3, medziaga4, serijos_nr_spaudejo, zmogus, today, komentaras])
        conn.commit()
        conn.close()

        CTkMessagebox(title="Info", message=f"Užsakymas '{aprasymas}' sekmingai uzregistruotos")
    except ValueError:
        CTkMessagebox(title="Error", message="Sunaudotas kiekis turi būti skaitinės reikšmės!", icon="cancel")
    except:
        CTkMessagebox(title="Error", message="Nepavyko prisijungti prie duomenų bazės.", icon="cancel")

if __name__ == "__main__":
    app = App()
    app.mainloop()
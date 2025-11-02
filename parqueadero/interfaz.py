import tkinter as tk
from tkinter import messagebox
from parqueadero.model.park import Parqueo, Vehiculo, Funciones, generar_ubicacion_aleatoria_en_campus

class InterfazParqueadero:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Parqueadero - UdeM")
        self.root.geometry("400x500")

        # Instancias del sistema
        self.parqueo = Parqueo({"carro": 50, "moto": 80, "bici": 20})
        self.funciones = Funciones(self.parqueo)

        # Título principal
        tk.Label(root, text="Sistema de Parqueadero", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

        # Botones principales
        tk.Button(root, text="Registrar Entrada", width=25, command=self.registrar_entrada).pack(pady=5)
        tk.Button(root, text="Registrar Salida", width=25, command=self.registrar_salida).pack(pady=5)
        tk.Button(root, text="Ver Ocupación", width=25, command=self.funciones.mostrar_ocupacion).pack(pady=5)
        tk.Button(root, text="Ver Cupos", width=25, command=self.funciones.mostrar_cupos).pack(pady=5)
        tk.Button(root, text="Alertas", width=25, command=self.funciones.mostrar_alertas).pack(pady=5)
        tk.Button(root, text="Graficar Ocupación", width=25, command=self.funciones.graficar_ocupacion).pack(pady=5)
        tk.Button(root, text="Generar Mapa", width=25, command=self.generar_mapa).pack(pady=5)

    def registrar_entrada(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Entrada")
        ventana.geometry("300x200")

        tk.Label(ventana, text="Placa:").grid(row=0, column=0)
        placa_entry = tk.Entry(ventana)
        placa_entry.grid(row=0, column=1)

        tk.Label(ventana, text="Tipo (carro/moto/bici):").grid(row=1, column=0)
        tipo_entry = tk.Entry(ventana)
        tipo_entry.grid(row=1, column=1)

        def confirmar():
            placa = placa_entry.get().upper()
            tipo = tipo_entry.get().lower()
            lat, lon = generar_ubicacion_aleatoria_en_campus()
            veh = Vehiculo(placa=placa, tipo=tipo, lat=lat, lon=lon)
            ok, alerts = self.parqueo.registrar_entrada(veh)
            if ok:
                messagebox.showinfo("Éxito", f"Entrada registrada para {placa}")
            else:
                messagebox.showerror("Error", "\n".join(alerts))
            ventana.destroy()

        tk.Button(ventana, text="Confirmar", command=confirmar).grid(row=2, columnspan=2)

    def registrar_salida(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Salida")
        ventana.geometry("300x150")

        tk.Label(ventana, text="Placa:").grid(row=0, column=0)
        placa_entry = tk.Entry(ventana)
        placa_entry.grid(row=0, column=1)

        def confirmar():
            placa = placa_entry.get().upper()
            registro = self.parqueo.registrar_salida(placa)
            if registro:
                messagebox.showinfo("Salida", f"Total a pagar: ${registro['total']} ({registro['horas']} horas)")
            else:
                messagebox.showerror("Error", "Vehículo no encontrado")
            ventana.destroy()

        tk.Button(ventana, text="Confirmar", command=confirmar).grid(row=1, columnspan=2)

    def generar_mapa(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Generar Mapa")
        ventana.geometry("300x150")

        tk.Label(ventana, text="Placa:").grid(row=0, column=0)
        placa_entry = tk.Entry(ventana)
        placa_entry.grid(row=0, column=1)

        def confirmar():
            placa = placa_entry.get().upper()
            self.funciones.generar_mapa_para_placa(placa)
            ventana.destroy()

        tk.Button(ventana, text="Generar", command=confirmar).grid(row=1, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazParqueadero(root)
    root.mainloop()
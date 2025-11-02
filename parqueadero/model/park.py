from datetime import datetime, timedelta
import json
import random
import webbrowser
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import folium
except ImportError:
    folium = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# Clase Vehculo
class Vehiculo:
    def __init__(self, placa, tipo, hora_entrada=None, cliente="normal", visitas=0, lat=None, lon=None):
        self.placa = placa.upper()
        self.tipo = tipo.lower()
        self.hora_entrada = hora_entrada or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cliente = cliente.lower()
        self.visitas = visitas
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Vehiculo(**data)

    def __str__(self):
        loc = f"({self.lat:.5f}, {self.lon:.5f})" if self.lat and self.lon else "sin ubicación"
        return f"{self.tipo.upper()} | {self.placa} | Entrada: {self.hora_entrada} | Cliente: {self.cliente} | Ubicación: {loc}"


# Clase Parqueo
class Parqueo:
    tarifas = {"carro": 2000, "moto": 1000, "bici": 500}

    def __init__(self, cupos, archivo_json=Path("parqueadero_data.json")):
        self.cupos = cupos.copy()
        self.archivo_json = archivo_json
        self.vehiculos = []
        self.historial = []
        self.operador_actual = None
        self.cargar_datos()

    def login(self, operador):
        self.operador_actual = operador

    def registrar_entrada(self, vehiculo):
        tipo = vehiculo.tipo
        if self.cupos.get(tipo, 0) <= 0:
            return False, ["No hay cupos disponibles para ese tipo de vehículo."]

        visitas_previas = sum(1 for r in self.historial if r["placa"] == vehiculo.placa)
        vehiculo.visitas = visitas_previas + 1
        if vehiculo.visitas >= 5:
            vehiculo.cliente = "frecuente"

        self.vehiculos.append(vehiculo)
        self.cupos[tipo] -= 1
        self.guardar_datos()

        alerts = []
        if self.cupos[tipo] == 1:
            alerts.append(f"Alerta: queda 1 cupo para {tipo}s.")
        if vehiculo.cliente == "frecuente":
            alerts.append("Cliente frecuente: descuento 10% en salida.")
        return True, alerts

    def registrar_salida(self, placa):
        placa = placa.upper()
        for v in list(self.vehiculos):
            if v.placa == placa:
                hora_salida = datetime.now()
                entrada = datetime.strptime(v.hora_entrada, "%Y-%m-%d %H:%M:%S")
                horas = max(1, int((hora_salida - entrada).total_seconds() // 3600))
                tarifa = self.tarifas.get(v.tipo, 1000)
                total = horas * tarifa
                if v.cliente == "frecuente":
                    total *= 0.9
                elif v.cliente == "mensual":
                    total = 0

                registro = {
                    "placa": v.placa,
                    "tipo": v.tipo,
                    "cliente": v.cliente,
                    "hora_entrada": v.hora_entrada,
                    "hora_salida": hora_salida.strftime("%Y-%m-%d %H:%M:%S"),
                    "horas": horas,
                    "total": float(total),
                    "operador": self.operador_actual,
                    "lat": v.lat,
                    "lon": v.lon
                }

                self.vehiculos.remove(v)
                self.cupos[v.tipo] += 1
                self.historial.append(registro)
                self.guardar_datos()
                return registro
        return None

    def guardar_datos(self):
        data = {
            "cupos": self.cupos,
            "vehiculos": [v.to_dict() for v in self.vehiculos],
            "historial": self.historial
        }
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def cargar_datos(self):
        if not self.archivo_json.exists():
            return
        with open(self.archivo_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.cupos = data.get("cupos", self.cupos)
        self.vehiculos = [Vehiculo.from_dict(d) for d in data.get("vehiculos", [])]
        self.historial = data.get("historial", [])

    def ver_ocupacion(self):
        return self.vehiculos

    def ver_cupos(self):
        return self.cupos


# Clase Funciones
class Funciones:
    def __init__(self, parqueo):
        self.parqueo = parqueo

    def mostrar_ocupacion(self):
        ocup = self.parqueo.ver_ocupacion()
        if not ocup:
            print("Parqueadero vacío.")
        else:
            print("Vehículos estacionados:")
            for v in ocup:
                print("-", v)

    def mostrar_cupos(self):
        print("Cupos disponibles por tipo:")
        for t, c in self.parqueo.ver_cupos().items():
            print(f"{t.capitalize()}: {c}")

    def mostrar_alertas(self):
        alerts = []
        for v in self.parqueo.vehiculos:
            entrada = datetime.strptime(v.hora_entrada, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - entrada > timedelta(hours=24):
                alerts.append(f"Vehículo {v.placa} lleva más de 24 horas estacionado.")
        for tipo, cupo in self.parqueo.cupos.items():
            if cupo == 1:
                alerts.append(f"Solo queda 1 cupo para {tipo}s.")
        if not alerts:
            print("No hay alertas.")
        else:
            for a in alerts:
                print(a)

    def exportar_reporte(self):
        if pd is None:
            print("Instala pandas: pip install pandas")
            return
        if not self.parqueo.historial:
            print("No hay historial para exportar.")
            return
        df = pd.DataFrame(self.parqueo.historial)
        df.to_csv("reporte_parqueadero.csv", index=False, encoding="utf-8")
        print("Reporte exportado a 'reporte_parqueadero.csv'")

    def mostrar_reporte_operador(self):
        if pd is None:
            print("Instala pandas: pip install pandas")
            return
        if not self.parqueo.historial:
            print("No hay historial.")
            return
        df = pd.DataFrame(self.parqueo.historial)
        resumen = df.groupby("operador")["total"].sum()
        print("Ingresos por operador:")
        for op, total in resumen.items():
            print(f"{op}: ${total:.2f}")

    def graficar_ocupacion(self):
        if plt is None:
            print("Instala matplotlib: pip install matplotlib")
            return
        tipos = [v.tipo for v in self.parqueo.vehiculos]
        if not tipos:
            print("No hay vehículos estacionados para graficar.")
            return
        conteo = {}
        for t in tipos:
            conteo[t] = conteo.get(t, 0) + 1
        labels = list(conteo.keys())
        values = list(conteo.values())

        plt.figure()
        plt.bar(labels, values)
        plt.title("Ocupación actual (por tipo)")
        plt.xlabel("Tipo")
        plt.ylabel("Cantidad")
        plt.show()

        plt.figure()
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Distribución de vehículos")
        plt.show()

    def generar_mapa_para_placa(self, placa):
        placa = placa.upper()
        v = next((x for x in self.parqueo.vehiculos if x.placa == placa), None)
        if v is None:
            last = next((r for r in reversed(self.parqueo.historial) if r["placa"] == placa), None)
            if not last or last.get("lat") is None or last.get("lon") is None:
                print("No se encontró ubicación para esa placa.")
                return
            lat, lon = last["lat"], last["lon"]
            label = f"{placa} (Última conocida)"
        else:
            if v.lat is None or v.lon is None:
                print("El vehículo no tiene ubicación registrada.")
                return
            lat, lon = v.lat, v.lon
            label = f"{placa} (Actualmente estacionado)"

        if folium is None:
            print("Instala folium: pip install folium")
            return

        m = folium.Map(location=[lat, lon], zoom_start=18)
        folium.Marker(location=[lat, lon], popup=label).add_to(m)

        out_path = Path("maps") / f"map_{placa}.html"
        out_path.parent.mkdir(exist_ok=True)
        m.save(str(out_path))
        webbrowser.open(out_path.resolve().as_uri())
        print(f"Mapa generado y abierto en: {out_path}")


# Utilidad
def generar_ubicacion_aleatoria_en_campus():
    zonas = [
        {"lat_min": 6.2318, "lat_max": 6.2323, "lon_min": -75.6108, "lon_max": -75.6098},

        {"lat_min": 6.2302, "lat_max": 6.2310, "lon_min": -75.6118, "lon_max": -75.6108},

        {"lat_min": 6.2310, "lat_max": 6.2318, "lon_min": -75.6120, "lon_max": -75.6110}
    ]
    zona = random.choice(zonas)
    lat = random.uniform(zona["lat_min"], zona["lat_max"])
    lon = random.uniform(zona["lon_min"], zona["lon_max"])
    return lat, lon
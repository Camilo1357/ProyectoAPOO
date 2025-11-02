from model.park import Vehiculo, Parqueo, Funciones, generar_ubicacion_aleatoria_en_campus

def menu():
    parqueo = Parqueo({"carro": 50, "moto": 80, "bici": 20})
    funciones = Funciones(parqueo)

    print("=== SISTEMA DE PARQUEADERO - Universidad de Medellín ===")
    operador = input("Ingrese su nombre de operador: ").strip() or "Operador"
    parqueo.login(operador)

    while True:
        print("\n--- Menú ---")
        print("1) Registrar entrada")
        print("2) Registrar salida")
        print("3) Listar ocupación actual")
        print("4) Ver cupos disponibles")
        print("5) Ver alertas inteligentes")
        print("6) Exportar reporte CSV (historial)")
        print("7) Reporte por operador")
        print("8) Graficar ocupación")
        print("9) Ver ubicación de un vehículo en el mapa")
        print("10) Salir")

        opt = input("Seleccione opción: ").strip()

        if opt == "1":
            placa = input("Placa: ").strip().upper()
            tipo = input("Tipo (carro/moto/bici): ").strip().lower()
            cliente = input("Cliente (normal/frecuente/mensual) [normal]: ").strip().lower() or "normal"
            usar_ubic = input("¿Desea ingresar ubicación manual? (s/n) [n]: ").strip().lower()
            lat = lon = None
            if usar_ubic == "s":
                try:
                    lat = float(input("Latitud (ej: 6.267): ").strip())
                    lon = float(input("Longitud (ej: -75.567): ").strip())
                except ValueError:
                    print("Coordenadas inválidas, se generará ubicación automática.")
                    lat, lon = generar_ubicacion_aleatoria_en_campus()
            else:
                lat, lon = generar_ubicacion_aleatoria_en_campus()

            veh = Vehiculo(placa=placa, tipo=tipo, cliente=cliente, lat=lat, lon=lon)
            ok, alerts = parqueo.registrar_entrada(veh)
            if ok:
                print("Entrada registrada.")
                for a in alerts:
                    print(a)
            else:
                for a in alerts:
                    print(a)

        elif opt == "2":
            placa = input("Placa a retirar: ").strip().upper()
            registro = parqueo.registrar_salida(placa)
            if registro:
                print(f"Salida registrada. Total a pagar: ${registro['total']} ({registro['horas']} horas).")
            else:
                print("Vehículo no encontrado.")

        elif opt == "3":
            funciones.mostrar_ocupacion()

        elif opt == "4":
            funciones.mostrar_cupos()

        elif opt == "5":
            funciones.mostrar_alertas()

        elif opt == "6":
            funciones.exportar_reporte()

        elif opt == "7":
            funciones.mostrar_reporte_operador()

        elif opt == "8":
            funciones.graficar_ocupacion()

        elif opt == "9":
            placa = input("Placa a localizar: ").strip().upper()
            funciones.generar_mapa_para_placa(placa)

        elif opt == "10":
            print("Guardando y saliendo...")
            parqueo.guardar_datos()
            break
        else:
            print("Opción inválida. Intente de nuevo.")
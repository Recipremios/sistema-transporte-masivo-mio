from typing import Dict, List, Tuple
from heapq import heappush, heappop
from collections import defaultdict

class SistemaMIO:
    def __init__(self):
        # Grafo del sistema MIO: {estacion: {estacion_conectada: (costo_en_minutos, rutas_disponibles)}}
        self.grafo = {
            'Universidades': {
                'San Fernando': (5, ['T47A']),
                'Meléndez': (4, ['P21A'])
            },
            'San Fernando': {
                'Universidades': (5, ['T47A']),
                'Capri': (6, ['T31']),
                'Estadio': (7, ['T47A'])
            },
            'Meléndez': {
                'Universidades': (4, ['P21A']),
                'Unidad Deportiva': (5, ['P21A'])
            },
            'Capri': {
                'San Fernando': (6, ['T31']),
                'Estadio': (4, ['T31'])
            },
            'Estadio': {
                'San Fernando': (7, ['T47A']),
                'Capri': (4, ['T31']),
                'San Bosco': (6, ['T50'])
            },
            'San Bosco': {
                'Estadio': (6, ['T50']),
                'Centro': (5, ['T50'])
            },
            'Centro': {
                'San Bosco': (5, ['T50']),
                'Terminal Andrés Sanín': (8, ['E21']),
                'Capri': (10, ['T31'])  # Agregada conexión bidireccional a Capri
            },
            'Terminal Andrés Sanín': {
                'Centro': (8, ['E21']),
                'Terminal Menga UTR&T': (15, ['E27'])
            },
            'Terminal Menga UTR&T': {
                'Terminal Andrés Sanín': (15, ['E27'])
            },
            'Unidad Deportiva': {
                'Meléndez': (5, ['P21A'])
            }
        }
        
        # Heurística aproximada en minutos (consistente con el grafo)
        self.heuristica = {
            'Universidades': 25,
            'San Fernando': 20,
            'Meléndez': 22,
            'Capri': 18,
            'Estadio': 15,
            'San Bosco': 10,
            'Centro': 8,
            'Terminal Andrés Sanín': 5,
            'Terminal Menga UTR&T': 0,
            'Unidad Deportiva': 20
        }
        self.estaciones = list(self.grafo.keys())

    def encontrar_ruta_optima(self, inicio: str, destino: str) -> Tuple[List[str], int, List[str]]:
        if inicio not in self.grafo or destino not in self.grafo:
            return None, 0, []
        
        cola = [(0, 0, inicio, [inicio], [])]  # (costo_total_est, costo_acum, nodo, ruta, rutas_usadas)
        visitados = set()
        
        while cola:
            costo_total, costo_acumulado, estacion_actual, ruta, rutas_usadas = heappop(cola)
            if estacion_actual == destino:
                return ruta, costo_acumulado, rutas_usadas
            if estacion_actual in visitados:
                continue
            visitados.add(estacion_actual)
            for vecino, (costo_ruta, rutas) in self.grafo[estacion_actual].items():
                if vecino not in visitados:
                    nuevo_costo = costo_acumulado + costo_ruta
                    costo_total_estimado = nuevo_costo + self.heuristica[vecino]
                    nueva_ruta = ruta + [vecino]
                    nuevas_rutas_usadas = rutas_usadas + [rutas[0]] if rutas else rutas_usadas
                    heappush(cola, (costo_total_estimado, nuevo_costo, vecino, nueva_ruta, nuevas_rutas_usadas))
        return None, 0, []

    def mostrar_ruta(self, inicio: str, destino: str):
        ruta, costo, rutas_usadas = self.encontrar_ruta_optima(inicio, destino)
        if ruta:
            print(f"\nRuta más rápida de {inicio} a {destino} en el sistema MIO:")
            print("Recorrido:")
            for i in range(len(ruta) - 1):
                estacion_actual = ruta[i]
                siguiente_estacion = ruta[i + 1]
                ruta_usada = rutas_usadas[i] if i < len(rutas_usadas) else "Transbordo"
                tiempo = self.grafo[estacion_actual][siguiente_estacion][0]
                print(f"- {estacion_actual} -> {siguiente_estacion} "
                      f"(Ruta {ruta_usada}, {tiempo} minutos)")
            print(f"\nTiempo total estimado: {costo} minutos")
            print("Rutas utilizadas:", ", ".join(set(rutas_usadas)))
        else:
            print(f"No se encontró ruta de {inicio} a {destino}. Es posible que no haya conexión directa.")

    def mostrar_estaciones(self):
        print("\nEstaciones disponibles:")
        for i, estacion in enumerate(self.estaciones, 1):
            print(f"{i}. {estacion}")

    def elegir_estacion(self, tipo: str) -> str:
        while True:
            self.mostrar_estaciones()
            try:
                seleccion = input(f"\nSeleccione el número de la estación de {tipo} (o 'salir'): ").strip()
                if seleccion.lower() == 'salir':
                    return None
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(self.estaciones):
                    return self.estaciones[seleccion - 1]
                print("Número inválido. Intente de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

def main():
    sistema = SistemaMIO()
    
    print("Sistema Inteligente MIO de Cali")
    print("Seleccione las estaciones ingresando el número correspondiente")
    print("-" * 50)
    
    while True:
        inicio = sistema.elegir_estacion("partida")
        if inicio is None:
            break
            
        destino = sistema.elegir_estacion("destino")
        if destino is None:
            break
            
        sistema.mostrar_ruta(inicio, destino)

if __name__ == "__main__":
    main()
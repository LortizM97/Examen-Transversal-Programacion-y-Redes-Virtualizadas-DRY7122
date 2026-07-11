# vlan.py
# Script que determina si una VLAN es normal o extendida

def verificar_vlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "La VLAN corresponde al rango NORMAL."
    elif 1006 <= vlan_id <= 4094:
        return "La VLAN corresponde al rango EXTENDIDO."
    else:
        return "Número de VLAN inválido. Debe estar entre 1 y 4094."

def main():
    try:
        vlan_id = int(input("Ingrese el número de VLAN: "))
        resultado = verificar_vlan(vlan_id)
        print(resultado)
    except ValueError:
        print("Error: Debe ingresar un número entero.")

if __name__ == "__main__":
    main()

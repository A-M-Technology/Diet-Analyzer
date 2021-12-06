class Product:
    def __init__(self, calories, name, tipo):
        self.tipo = tipo
        self.__calories = calories
        self.name = name
        self.cal_up = calories

    def assign(self, other):
        self.cal_up = \
            round(self.__calories * other, 2)

        return self.cal_up


class Refeicao:
    def __init__(self):
        self.str_procs = ''
        self.names = []
        self.kcal = []
        self.items = []
        self.tipos = []
        self.lista_cal = []
        self.lista_nomes = []

    def list_kcal(self):
        self.kcal = []
        for item in self.items:
            if item.cal_up == 0:
                del self.items[item]
            else:
                self.kcal.append(item.cal_up)
        return self.kcal

    def list_tipos(self):
        self.tipos = []
        for item in self.items:
            if item.cal_up == 0:
                del self.items[item]
            else:
                self.tipos.append(item.tipo)
        return self.tipos

    def list_names(self):
        self.names = []
        for item in self.items:
            if item.cal_up == 0:
                del self.items[item]
            else:
                self.names.append(item.name)
        return self.names

    def insert(self, item):
        self.items.append(item)

    def remove(self, index):
        del self.items[index]

    def __str__(self):
        lista_return = []
        self.lista_nomes = []
        self.lista_cal = []
        for i in self.items:
            values_in = [str(a) for a, x in enumerate(self.items) if x == i]
            values_in = ''.join(values_in)
            lista_return.append(f'|{int(values_in) + 1}| {i.name}({i.cal_up}cal)')
            self.lista_nomes.append(i.name)
            self.lista_cal.append(i.cal_up)
        return ' $! '.join(lista_return)

    def list_products(self):
        for item in self.items:
            if item.cal_up == 0:
                del self.items[item]
        self.str_procs = '#!'.join(self.items)

    def total_calories(self):
        total = 0
        for item in self.items:
            total += item.cal_up
        return total


def metabolismo_basal(peso, altura, idade, tipo_altura, genero):
    if tipo_altura == 'm':
        altura *= 100
    if genero.lower() == 'homem':
        return round(66.47 + (13.76 * peso) + (5.0 * altura) - (6.76 * idade), 2)
    elif genero.lower() == 'mulher':
        return 665.1 + (9.56 * peso) + (1.85 * altura) - (4.67 * idade)


class CalculateCal:
    @staticmethod
    def day(peso, metabolismobasal, calorias_diarias):
        valor_diario = calorias_diarias - metabolismobasal
        if valor_diario < 0:
            return round((peso - (valor_diario / 7000 * -1)), 5)
        return peso + (valor_diario / 7000)

    @staticmethod
    def monthly(peso, calorias_diario, altura, idade, tipo_altura, genero, vezes: int):
        lista_360 = [(360*_)+360 for _ in range(20)]
        basal = metabolismo_basal(peso, altura, idade, tipo_altura, genero)
        peso_diario = CalculateCal.day(peso=peso, metabolismobasal=basal, calorias_diarias=calorias_diario)
        for _ in range(vezes + 1):
            for numb in lista_360:
                print(numb, _)
                if numb == _:
                    idade += 1
                    print('Passed')

            basal = metabolismo_basal(peso_diario, altura, idade, tipo_altura, genero)
            peso_diario = CalculateCal.day(peso=peso_diario, metabolismobasal=basal, calorias_diarias=calorias_diario)
        return round(peso_diario, 2)

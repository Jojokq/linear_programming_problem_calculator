from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import csv
from simplyx import final_calc

class InequalityApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Заголовок
        self.title_label = Label(
            text='Задача ЛП (пока только для 3x3)',
            size_hint=(1, 0.1),
            font_size='24sp'
        )
        self.add_widget(self.title_label)
        
        # Выбор размерности и количества уравнений
        settings_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        # Размерность
        dimension_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        dimension_layout.add_widget(Label(text='Количество переменных:'))
        
        self.dimension_spinner = Spinner(
            text='2',
            values=('2', '3', '4', '5'),
            size_hint_y=0.6
        )
        self.dimension_spinner.bind(text=self.on_dimension_change)
        dimension_layout.add_widget(self.dimension_spinner)
        settings_layout.add_widget(dimension_layout)
        
        # Количество уравнений
        equation_layout = BoxLayout(orientation='vertical', size_hint_x=0.5)
        equation_layout.add_widget(Label(text='Количество уравнений:'))
        
        self.equation_spinner = Spinner(
            text='3',
            values=('1', '2', '3', '4', '5', '6'),
            size_hint_y=0.6
        )
        self.equation_spinner.bind(text=self.on_equation_change)
        equation_layout.add_widget(self.equation_spinner)
        settings_layout.add_widget(equation_layout)
        
        self.add_widget(settings_layout)
        
        # Контейнер для системы неравенств
        self.inequality_scroll = ScrollView(size_hint=(1, 0.5))
        self.inequality_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.inequality_grid.bind(minimum_height=self.inequality_grid.setter('height'))
        self.inequality_scroll.add_widget(self.inequality_grid)
        self.add_widget(self.inequality_scroll)
        
        # Целевая функция
        self.target_label = Label(
            text='Целевая функция:',
            size_hint=(1, 0.05),
            font_size='18sp'
        )
        self.add_widget(self.target_label)
        
        self.target_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.target_inputs = []
        self.create_target_function(2)
        self.add_widget(self.target_layout)
        
        # Кнопка выполнения
        self.execute_button = Button(
            text='Выполнить',
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        self.execute_button.bind(on_press=self.generate_csv)
        self.add_widget(self.execute_button)
        
        # Инициализация системы
        self.inequality_inputs = []
        self.current_dimension = 2
        self.current_equations = 3
        self.create_inequality_system(2, 3)
    
    def on_dimension_change(self, spinner, text):
        new_dimension = int(text)
        if new_dimension != self.current_dimension:
            self.current_dimension = new_dimension
            self.create_inequality_system(new_dimension, self.current_equations)
            self.create_target_function(new_dimension)
    
    def on_equation_change(self, spinner, text):
        new_equations = int(text)
        if new_equations != self.current_equations:
            self.current_equations = new_equations
            self.create_inequality_system(self.current_dimension, new_equations)
    
    def create_target_function(self, dimension):
        # Очищаем предыдущую целевую функцию
        self.target_layout.clear_widgets()
        self.target_inputs = []
        
        self.target_layout.add_widget(Label(text='max/min Z =', size_hint_x=0.3))
        
        # Поля для коэффициентов целевой функции
        for i in range(dimension):
            coeff_layout = BoxLayout(orientation='vertical', size_hint_x=0.7/dimension)
            
            label = Label(text=f'x{i+1}', size_hint_y=0.3)
            coeff_layout.add_widget(label)
            
            input_field = TextInput(
                text='0',
                multiline=False,
                size_hint_y=0.7,
                input_filter='float'
            )
            self.target_inputs.append(input_field)
            coeff_layout.add_widget(input_field)
            
            self.target_layout.add_widget(coeff_layout)
    
    def create_inequality_system(self, dimension, equations):
        # Очищаем предыдущую систему
        self.inequality_grid.clear_widgets()
        self.inequality_inputs = []
        
        # Создаем заголовок для переменных
        header_layout = BoxLayout(size_hint_y=None, height=40)
        header_layout.add_widget(Label(text='', size_hint_x=0.15))
        
        for i in range(dimension):
            header_layout.add_widget(Label(text=f'x{i+1}', size_hint_x=0.6/dimension))
        
        header_layout.add_widget(Label(text='Знак', size_hint_x=0.15))
        header_layout.add_widget(Label(text='Константа', size_hint_x=0.2))
        self.inequality_grid.add_widget(header_layout)
        
        # Создаем строки для неравенств
        for row in range(equations):
            row_layout = BoxLayout(size_hint_y=None, height=40)
            row_inputs = []
            
            # Метка номера строки
            row_layout.add_widget(Label(text=f'{row+1}.', size_hint_x=0.15))
            
            # Поля для коэффициентов
            for i in range(dimension):
                input_field = TextInput(
                    text='0',
                    multiline=False,
                    size_hint_x=0.6/dimension,
                    input_filter='float'
                )
                row_inputs.append(input_field)
                row_layout.add_widget(input_field)
            
            # Выбор знака неравенства (только ≤ и ≥)
            sign_spinner = Spinner(
                text='≤',
                values=('≤', '≥'),
                size_hint_x=0.15
            )
            row_inputs.append(sign_spinner)
            row_layout.add_widget(sign_spinner)
            
            # Поле для константы
            const_input = TextInput(
                text='0',
                multiline=False,
                size_hint_x=0.2,
                input_filter='float'
            )
            row_inputs.append(const_input)
            row_layout.add_widget(const_input)
            
            self.inequality_inputs.append(row_inputs)
            self.inequality_grid.add_widget(row_layout)
    
    def generate_csv(self, instance):
        filename = 'datatable/inequality_system.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            # Заголовок CSV
            header = ['C'] + [f'x{i+1}' for i in range(self.current_dimension)]
            writer.writerow(header)
            
            # Данные из системы неравенств
            for row_inputs in self.inequality_inputs:
                row_data = []
                # Константа (последний элемент в row_inputs)
                const_value = row_inputs[-1].text if row_inputs[-1].text else '0'
                row_data.append(const_value)
                
                # Коэффициенты переменных
                for i in range(self.current_dimension):
                    coeff_value = row_inputs[i].text if row_inputs[i].text else '0'
                    row_data.append(coeff_value)
                
                writer.writerow(row_data)
            
            # Пустая строка (через строчку от целевой функции)
            writer.writerow([''] * (self.current_dimension + 1))
            
            # Целевая функция
            target_row = ['0']  # C = 0 для целевой функции
            for input_field in self.target_inputs:
                coeff_value = int(input_field.text) if input_field.text else '0'
                target_row.append(coeff_value * -1)
            writer.writerow(target_row)
        
        print(f"CSV файл '{filename}' успешно создан!")
        print(f'Ваше решение!: ')
        final_calc()


class InequalityAppApp(App):
    def build(self):
        return InequalityApp()


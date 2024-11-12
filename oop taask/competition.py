import flet as ft


class Participant:
    def __init__(self, name, age, sport):
        self.name = name
        self.age = age
        self.sport = sport

    def __str__(self):
        return f"{self.name}, {self.age} років, {self.sport}"


class Team:
    def __init__(self, name):
        self.name = name
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)

    def __str__(self):
        return f"{self.name} (Учасники: {[str(p) for p in self.participants]})"


class Competition:
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.results = {}

    def add_team(self, team):
        self.teams.append(team)

    def record_result(self, team, score):
        """Зберегти результат для команди."""
        self.results[team.name] = score

    def display_results(self):
        return [(team_name, score) for team_name, score in self.results.items()]


def main(page: ft.Page):
    page.title = "Облік спортивних змагань"
    page.scroll = "auto"

    # Створюємо об'єкт змагання
    competition = Competition("Чемпіонат міста")

    # Поля введення для реєстрації
    username_input = ft.TextField(label="Ім'я користувача", width=300)
    email_input = ft.TextField(label="Електронна пошта", width=300)
    password_input = ft.TextField(label="Пароль", width=300, password=True)
    confirm_password_input = ft.TextField(label="Підтвердіть пароль", width=300, password=True)

    # Поля введення для додавання команди та учасника
    team_name_input = ft.TextField(label="Назва команди", width=300)
    participant_name_input = ft.TextField(label="Ім'я учасника", width=300)
    participant_age_input = ft.TextField(label="Вік учасника", width=300)
    participant_sport_input = ft.TextField(label="Вид спорту", width=300)

    # Поля для введення результатів
    result_team_input = ft.TextField(label="Команда", width=300)
    result_score_input = ft.TextField(label="Результат", width=300)

    # Таблиця для команд
    team_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Назва команди")),
            ft.DataColumn(ft.Text("Ім'я учасника")),
            ft.DataColumn(ft.Text("Вік")),
            ft.DataColumn(ft.Text("Вид спорту")),
        ],
        rows=[]
    )

    # Таблиця для результатів
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Команда")),
            ft.DataColumn(ft.Text("Результат")),
        ],
        rows=[]
    )

    # Функція для переходу до основної частини після успішної реєстрації
    def show_main_app():
        page.controls.clear()
        page.add(
            ft.Text("Додати команду", size=20),
            team_name_input,
            ft.ElevatedButton("Додати команду", on_click=add_team),

            ft.Text("Додати учасника до останньої команди", size=20),
            participant_name_input,
            participant_age_input,
            participant_sport_input,
            ft.ElevatedButton("Додати учасника", on_click=add_participant),

            ft.Text("Ввести результат змагання", size=20),
            result_team_input,
            result_score_input,
            ft.ElevatedButton("Записати результат", on_click=record_result),

            ft.Text("Список команд", size=20),
            team_table,

            ft.Text("Результати змагання", size=20),
            results_table
        )
        page.update()

    # Функція реєстрації
    def register(e):
        username = username_input.value
        email = email_input.value
        password = password_input.value
        confirm_password = confirm_password_input.value
        if username and email and password and confirm_password:
            if password == confirm_password:
                show_main_app()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Паролі не збігаються"))
                page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Будь ласка, заповніть усі поля"))
            page.snack_bar.open = True
        page.update()

    # Функції для додавання команд, учасників та результатів
    def add_team(e):
        team_name = team_name_input.value
        if team_name:
            team = Team(team_name)
            competition.add_team(team)
            team_name_input.value = ""
            page.update()

    def add_participant(e):
        if not competition.teams:
            return  # Переконайтеся, що є хоча б одна команда
        participant_name = participant_name_input.value
        participant_age = participant_age_input.value
        participant_sport = participant_sport_input.value
        if participant_name and participant_age and participant_sport:
            participant = Participant(participant_name, int(participant_age), participant_sport)
            competition.teams[-1].add_participant(participant)

            # Додаємо рядок до таблиці команд
            team_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(competition.teams[-1].name)),
                        ft.DataCell(ft.Text(participant.name)),
                        ft.DataCell(ft.Text(str(participant.age))),
                        ft.DataCell(ft.Text(participant.sport)),
                    ]
                )
            )
            page.update()
            participant_name_input.value = ""
            participant_age_input.value = ""
            participant_sport_input.value = ""

    def record_result(e):
        team_name = result_team_input.value
        score = result_score_input.value
        if team_name and score:
            for team in competition.teams:
                if team.name == team_name:
                    competition.record_result(team, int(score))

                    # Додаємо рядок до таблиці результатів
                    results_table.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(team_name)),
                                ft.DataCell(ft.Text(score)),
                            ]
                        )
                    )
                    page.update()
                    result_team_input.value = ""
                    result_score_input.value = ""
                    break

    # Додаємо відцентровану форму реєстрації на сторінку
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Реєстрація", size=20),
                    username_input,
                    email_input,
                    password_input,
                    confirm_password_input,
                    ft.ElevatedButton("Зареєструватися", on_click=register),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )
    )


ft.app(target=main)

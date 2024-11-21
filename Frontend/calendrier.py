import plotly.graph_objects as go
import calendar
import datetime

# Liste des jours fériés et fêtes aux États-Unis en 2024
holidays = {
    datetime.date(2024, 1, 1): "Nouvel An",
    datetime.date(2024, 1, 15): "Martin Luther King Jr. Day",
    datetime.date(2024, 2, 19): "Presidents' Day",
    datetime.date(2024, 5, 27): "Memorial Day",
    datetime.date(2024, 7, 4): "Fête de l'Indépendance",
    datetime.date(2024, 9, 2): "Labor Day",
    datetime.date(2024, 10, 14): "Columbus Day",
    datetime.date(2024, 11, 11): "Veterans Day",
    datetime.date(2024, 11, 28): "Thanksgiving",
    datetime.date(2024, 12, 25): "Noël",
    # Ajouter d'autres fêtes importantes
    datetime.date(2024, 2, 14): "Saint-Valentin",
    datetime.date(2024, 10, 31): "Halloween"
}

# Créer un calendrier sous forme de tableau avec Plotly
months = range(1, 13)
year = 2024

days_of_week = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
fig = go.Figure()

# Structurer l'affichage des mois sur plusieurs lignes
month_values = []
for month in months:
    month_calendar = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month].upper()

    # Créer les valeurs pour l'affichage
    month_days = []
    for week in month_calendar:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append('')  # Case vide pour les jours en dehors du mois
            else:
                day_date = datetime.date(year, month, day)
                week_days.append(day_date)
        month_days.append(week_days)
    month_values.append((month_name, month_days))

# Afficher tous les mois dans une grille
rows = []
for month_name, month_days in month_values:
    header_row = [month_name] + [''] * 6  # En-tête avec le nom du mois
    rows.append(header_row)
    rows.append(days_of_week)  # Ajouter les jours de la semaine
    for week in month_days:
        formatted_week = []
        for day in week:
            if isinstance(day, datetime.date) and day in holidays:
                formatted_week.append(f"<b style='background-color:yellow'>{day.day}</b>")
            elif isinstance(day, datetime.date):
                formatted_week.append(str(day.day))
            else:
                formatted_week.append(day)
        rows.append(formatted_week)
    rows.append([''] * 7)  # Ligne vide pour espacer les mois

# Convertir les lignes en colonnes pour Plotly
columns = list(zip(*rows))

fig.add_trace(
    go.Table(
        header=dict(
            values=[" "] * 7,
            align='center',
            fill_color='lightgrey',
            font=dict(size=14, color='black')
        ),
        cells=dict(
            values=columns,
            align='center',
            fill=dict(
                color=[
                    ["lightyellow" if isinstance(cell, str) and 'background-color:yellow' in cell else "white" for cell in row]
                    for row in rows
                ]
            ),
            font=dict(size=12),  # Augmentation de la taille de la police
            height=45  # Augmentation de la hauteur des cellules
        )
    )
)

fig.update_layout(
    title_text="Calendrier 2024 - Jours fériés et fêtes aux États-Unis en jaune",
    showlegend=False,
    height=2400,  # Augmenter la hauteur pour espacer les mois
    width=1800    # Augmenter la largeur pour un meilleur affichage
)
fig.show()

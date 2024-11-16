import numpy as np
import pandas as pd


data_path = r'data_for_spb_hakaton_entities/data_for_spb_hakaton_entities1-Table 1.csv'
history_path = r'data_for_spb_hakaton_entities\history-Table 1.csv'
sprints_path = r'data_for_spb_hakaton_entities\sprints-Table 1.csv'


def extract_sprint_names(data_path, changes_path, sprints_path):
    # логика: парсим файл с названиями спринтов и тасками в нём
    # делаем join на entity и сохраняем это в БД
    data = pd.read_csv(data_path, sep=';', skiprows=1)
    history = pd.read_csv(changes_path, sep=';', skiprows=1).dropna(how="all")
    sprints = pd.read_csv(sprints_path, sep=';', skiprows=1)
    sprints['entity_ids'] = sprints['entity_ids'].apply(lambda x: list(map(int, x.strip('{}').split(','))))

    sprints_normalized = sprints.explode('entity_ids').reset_index(drop=True)
    merged_df = pd.merge(sprints_normalized, data, left_on='entity_ids', right_on='entity_id', how='inner')
    # если будем загружать в sql, то сначала сконвертируем даты
    convert_to_date = ['sprint_start_date', 'sprint_end_date', 'create_date', 'update_date']
    merged_df[convert_to_date] = merged_df[convert_to_date].apply(pd.to_datetime)
    merged_df.to_csv(r'data\aggregated.csv', index=False, sep=";", encoding="utf-8-sig")


extract_sprint_names(data_path, history_path, sprints_path)



# Что нужно доработать:
# добавить возможность селекта конкретных команд
#
def analyze_sprint(sprint_name: str) -> dict:
    df = pd.read_csv(r'data\aggregated.csv', sep=';')
    df = df[df['sprint_name'] == sprint_name]

    status_count = df['status'].value_counts().reset_index()
    status_count.columns = ['status', 'count']
    total_count = df.shape[0]
    total_hours = df['estimation'].sum()
    cancelled = (
            (df['status'].isin(['Выполнено', 'Закрыто']) &
             df['resolution'].isin(['Отклонено', 'Отменено инициатором', 'Дубликат']))
            |
            ((df['type'] == 'Дефект') & (df['status'] == 'Отклонен исполнителем'))
    )

    cancelled_count = df[cancelled].shape[0]
    cancelled_sum = df[cancelled]['estimation'].sum()

    finished = (df['status'].isin(['Выполнено', 'Закрыто'])) & ~cancelled
    finished_count = df[finished].shape[0]
    finished_sum = df[finished]['estimation'].sum()

    todo = df['status'] == 'Создано'
    todo_count = df[todo].shape[0]
    todo_sum = df[todo]['estimation'].sum()

    in_progress = ~(cancelled | finished | todo)
    in_progress_count = df[in_progress].shape[0]
    in_progress_sum = df[in_progress]['estimation'].sum()

    response = {'todo_overload': 0, 'cancelled_overload': 0, 'backlog_overload': 0}
    if todo_sum / total_hours > 0.2:
        response['todo_overload'] = 1
    if cancelled_sum / total_hours > 0.1:
        response['cancelled_count'] = 1

    response['total_tasks'] = total_count
    response['cancelled_tasks'] = cancelled_count
    response['todo_tasks'] = todo_count
    response['in_progress_tasks'] = in_progress_count
    response.update(analyze_backlog_changes(sprint_name))
    print(response)
    return response


def analyze_backlog_changes(sprint_name: str)-> dict:
    df = pd.read_csv(r'data\aggregated.csv', sep=';')
    df = df[df['sprint_name'] == sprint_name]
    df = df[df['type'] != 'Дефект']

    convert_to_date = ['sprint_start_date', 'sprint_end_date', 'create_date', 'update_date']
    df[convert_to_date] = df[convert_to_date].apply(pd.to_datetime)
    total_hours = df['estimation'].sum()
    late_tasks = df[df['create_date'] - df['sprint_start_date'] >= pd.Timedelta(days=2)]
    late_tasks_sum = late_tasks['estimation'].sum()
    backlog_change_percentage = np.round(late_tasks_sum * 100 / (total_hours - late_tasks_sum), 1)
    backlog_overload = int(backlog_change_percentage > 20)
    return {'backlog_change': float(backlog_change_percentage), 'backlog_overload': backlog_overload}


analyze_sprint('Спринт 2024.3.1.NPP Shared Sprint')
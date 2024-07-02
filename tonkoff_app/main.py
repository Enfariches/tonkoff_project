import flet as ft
import asyncio

from config import logger

import database.db_webapp as db
from datetime import datetime, timedelta

points_per_click = 10
max_points_per_session = 1000
cooldown_period = timedelta(hours=1)
current_time = datetime.now()

async def main(page: ft.Page) -> None:

    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {'SingleDay': 'fonts/SingleDay-Regular.ttf'}
    page.theme = ft.Theme(font_family='SingleDay')

    user_id = int(page.route.split("=")[1])

    try:
        initial_score = await db.get_user_score(user_id)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {user_id})")

    async def score_up(event: ft.ContainerTapEvent) -> None: #Каждый клик

        current_time = datetime.now()

        try:
            last_reset_time = await db.get_last_reset_time(user_id)
        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователя: {user_id})")

        if last_reset_time is None:

            try:
                await db.update_last_reset_time(user_id, current_time)
                last_reset_time = current_time
            except Exception as e:
                logger.error(f"Ошибка: {e}. Пользователя: {user_id})")

        elapsed_time = current_time - last_reset_time
        print(elapsed_time)
        print(elapsed_time < cooldown_period)

        if score.data % max_points_per_session == 0 and score.data > 0:
            if elapsed_time < cooldown_period:
                remaining_time = cooldown_period - elapsed_time
                timer_text.value = f'Next reset in: {str(remaining_time).split(".")[0]}'
                await page.update_async()
            else:

                try:
                    await db.update_last_reset_time(user_id, current_time)
                    timer_text.value = ''
                except Exception as e:
                    logger.error(f"Ошибка: {e}. Пользователя: {user_id})")

        score.data += points_per_click
        score.value = str(score.data)

        image.scale = 0.90

        progress_bar.value = (score.data % max_points_per_session) / max_points_per_session

        if score.data % max_points_per_session == 0 and score.data > 0:
            timer_text.value = f'Next reset in: {str(cooldown_period).split(".")[0]}'

        try:
            await db.update_score(user_id, score.data)
        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователя: {user_id})")

        await page.update_async()
        await asyncio.sleep(0.1)
        image.scale = 1
        await page.update_async()

    score = ft.Text(value=str(initial_score), size=60, color='#FFFFFF', data=initial_score)
    timer_text = ft.Text(value='', size=20, color='#FFFFFF')

    score_counter = ft.Text(
        size=50,
        animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN)
    )

    image = ft.Image(
        src='app-icon.png',
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE),
        border_radius=ft.BorderRadius(250, 250, 250, 250)
    )

    progress_bar = ft.ProgressBar(
        value=0,
        width=page.width - 100,
        bar_height=20,
        color='#f5ff9f',
        bgcolor='#FFD700',
        border_radius = ft.BorderRadius(10, 10, 10, 10)
    )

    container_2 = ft.Container(
        content=ft.Stack(controls=[image, score_counter]),
        alignment=ft.alignment.center,
        on_click=score_up,
        margin=ft.Margin(0, 0, 0, 30)
    )

    container_3 = ft.Container(
        content=(progress_bar),
        alignment=ft.alignment.center,
        border_radius=ft.BorderRadius(10, 10, 10, 10)
    )

    background_image = ft.Image(
        src='app-background.png',
        fit=ft.ImageFit.COVER,
        expand=True
    )

    content_column = ft.Column(
        controls=[score, timer_text, container_2, container_3],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    stack = ft.Stack(
        controls=[background_image, content_column],
        expand=True
    )

    await page.add_async(stack)

if __name__ == "__main__":
    ft.app(target=main, view=None, port=80)

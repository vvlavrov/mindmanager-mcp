"""Populate AI-Trading Mindmap according to Claude Code's specification."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.com_bridge import MindManagerBridge

bridge = MindManagerBridge()
doc = bridge.get_active_doc()
print(f"Connecting to MindManager document: {doc.Name}", flush=True)

# 1. Setup Central Topic
ct = doc.CentralTopic
ct.Text = "AI Trading: Интеграция UI и оверлеев (M1 / TRA-02)"
print("[1/8] Central Topic set", flush=True)

bridge.set_topic_notes(
    ct.Text,
    "ТЗ и пошаговый план внедрения компонентов TradingView в AI Trading Workbench.\n"
    "Базовый коммит стенда: bb63f37416702ff04d9ab1d0349dd49281f7c23c\n"
    "Принцип реализации: REUSE FIRST (Прямое использование -> Адаптация -> Новая разработка)."
)
bridge.set_style(ct.Text, shape="CAPSULE", fill_color="#1A365D", text_color="#FFFFFF", bold=True, font_size=13)

# Clear existing subtopics if any
while ct.AllSubTopics.Count > 0:
    ct.AllSubTopics.Item(1).Delete()
print("[2/8] Cleaned existing subtopics", flush=True)

# 2. Branch: Архитектурный контекст
b1 = bridge.add_subtopic(
    ct.Text,
    "Архитектурный контекст (REUSE FIRST)",
    notes="Компоненты инфраструктуры AI Trading Workbench, уже доступные для переиспользования.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#E2E8F0",
    text_color="#1A202C",
)

bridge.add_subtopic(
    "Архитектурный контекст (REUSE FIRST)",
    "KLineChart 10.1.0 (Canvas Engine)",
    notes="Нативный оверлей horizontalStraightLine с поддержкой одной точки и режимов магнита (normal, weak_magnet, strong_magnet).",
    complete_percent=100,
    priority=2,
    shape="DATABASE",
    fill_color="#EDF2F7",
)

bridge.add_subtopic(
    "Архитектурный контекст (REUSE FIRST)",
    "Слой семантики (semantics.ts)",
    notes="TOOL_TEMPLATE.level = horizontalStraightLine, TEMPLATE_POINTS = 1, квантование цены quantizePrice.",
    complete_percent=100,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Архитектурный контекст (REUSE FIRST)",
    "Слой персистентности (DrawingService.ts)",
    notes="Управление локальным состоянием, сетевыми ошибками, версионированием и синхронизацией по WebSocket.",
    complete_percent=100,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Архитектурный контекст (REUSE FIRST)",
    "Векторные ресурсы и палитра Cold Gray",
    notes="12 эталонных SVG-иконок и 19 ступеней палитры Cold Gray извлечены и подтверждены техническим PoC.",
    complete_percent=100,
    priority=3,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_boundary(
    "Архитектурный контекст (REUSE FIRST)",
    shape="RECTANGLE",
    fill_color="#F7FAFC",
    line_color="#A0AEC0",
    line_style="DASH",
)
print("[3/8] Branch 1: Архитектурный контекст created", flush=True)

# 3. Branch: План внедрения (7 Шагов SolidJS)
b2 = bridge.add_subtopic(
    ct.Text,
    "План внедрения (7 Шагов SolidJS)",
    notes="Пошаговая сборка интерфейсного слоя UI в SolidJS и соединение с существующим графическим движком.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EBF8FF",
    text_color="#2B6CB0",
)
bridge.add_icon("План внедрения (7 Шагов SolidJS)", "ROCKET")

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 1: Векторные иконки (icons.tsx)",
    notes="Добавить типизированные функциональные компоненты SolidJS на базе извлечённых SVG-файлов из evidence/icons/ (HorizontalLine, VerticalLine, TrendLine, Rectangle).",
    complete_percent=100,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 1: Векторные иконки (icons.tsx)", due_date="2026-11-02", resources=["Claude Code", "Слава"])
bridge.add_icon("Шаг 1: Векторные иконки (icons.tsx)", "CHECK")

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 2: CSS-токены темы (styles.css)",
    notes="Задекларировать CSS Custom Properties в секции :root (Cold Gray 50..900, tv-blue-500, minty-green-500, ripe-red-500).",
    complete_percent=75,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 2: CSS-токены темы (styles.css)", due_date="2026-11-03", resources=["Claude Code"])

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 3: Стили KLineChart (ChartAdapter.ts)",
    notes="Передать зафиксированные аппаратные цвета Canvas в метод chart.setStyles (сетка #232632, свечи #089981 / #f23645).",
    complete_percent=50,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 3: Стили KLineChart (ChartAdapter.ts)", due_date="2026-11-04", resources=["Claude Code"])

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 4: Панель избранного (FavoriteToolbar.tsx)",
    notes="Плавающая панель быстрого выбора инструментов рисования и переключения магнита.",
    complete_percent=25,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 4: Панель избранного (FavoriteToolbar.tsx)", due_date="2026-11-06", resources=["Claude Code"])

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 5: Панель свойств (DrawingPropertiesBar.tsx)",
    notes="Контекстная плавающая панель настройки выделенной линии: толщина (1-4px), цвет, стиль (solid, dash).",
    complete_percent=0,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 5: Панель свойств (DrawingPropertiesBar.tsx)", due_date="2026-11-08", resources=["Claude Code"])

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 6: Модальное окно настроек (DrawingSettingsModal.tsx)",
    notes="Модальное окно редактирования точных числовых координат ценового уровня, меток и визуальных свойств.",
    complete_percent=0,
    priority=3,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 6: Модальное окно настроек (DrawingSettingsModal.tsx)", due_date="2026-11-10", resources=["Claude Code"])

bridge.add_subtopic(
    "План внедрения (7 Шагов SolidJS)",
    "Шаг 7: Связка с DrawingService & E2E тесты",
    notes="Подключение к WebSocket бэкенда, проверка персистентности и сквозные тесты на Playwright.",
    complete_percent=0,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
bridge.set_task("Шаг 7: Связка с DrawingService & E2E тесты", due_date="2026-11-12", resources=["Claude Code", "Playwright"])

bridge.add_boundary(
    "План внедрения (7 Шагов SolidJS)",
    shape="RECTANGLE",
    fill_color="#F0F9FF",
    line_color="#3182CE",
    line_style="SOLID",
)
print("[4/8] Branch 2: 7 Шагов SolidJS created", flush=True)

# 4. Branch: Исследование графиков TradingView
bridge.add_subtopic(
    ct.Text,
    "Исследование TradingView UI (tv-ui-research)",
    notes="Реверс-инжиниринг и анализ поведения интерфейса TradingView через REA и Playwright.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#FEFCBF",
    text_color="#744210",
)

bridge.add_subtopic(
    "Исследование TradingView UI (tv-ui-research)",
    "Каталогизация селекторов элементов UI",
    notes="Стабильные CSS/XPath селекторы верхнего тулбара, поиска тикеров, переключения таймфреймов и легенды OHLCV.",
    complete_percent=50,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)

bridge.add_subtopic(
    "Исследование TradingView UI (tv-ui-research)",
    "Анализ протокола WebSocket котировок",
    notes="Реверс-инжиниринг входящих пакетов котировок в реальном времени (~m~ или JSON RPC пакеты).",
    complete_percent=25,
    priority=1,
    shape="ROUNDED_RECTANGLE",
)
bridge.add_callout("Анализ протокола WebSocket котировок", "Критично: минимальные задержки котировок для торгового робота!")

bridge.add_subtopic(
    "Исследование TradingView UI (tv-ui-research)",
    "Координаты HTML5 Canvas и ценовые шкалы",
    notes="Сопоставление экранных пикселей холста с ценовыми уровнями и временной шкалой для кликов и drag-and-drop.",
    complete_percent=25,
    priority=2,
    shape="ROUNDED_RECTANGLE",
)
print("[5/8] Branch 3: tv-ui-research created", flush=True)

# 5. Branch: Целевые артефакты
bridge.add_subtopic(
    ct.Text,
    "Целевые артефакты поставки",
    notes="Документы и модули, формируемые по итогам итерации M1.",
    shape="ROUNDED_RECTANGLE",
    fill_color="#EDF2F7",
    text_color="#2D3748",
)

bridge.add_subtopic(
    "Целевые артефакты поставки",
    "DATA_FLOW.md (Схема потоков данных)",
    complete_percent=25,
    priority=2,
    shape="DOCUMENT",
)
bridge.add_subtopic(
    "Целевые артефакты поставки",
    "UI_MAP.md (Карта селекторов и ролей)",
    complete_percent=50,
    priority=2,
    shape="DOCUMENT",
)
bridge.add_subtopic(
    "Целевые артефакты поставки",
    "AUTOMATION_RECIPES.md (Рецепты для агента)",
    complete_percent=0,
    priority=3,
    shape="DOCUMENT",
)
print("[6/8] Branch 4: Целевые артефакты created", flush=True)

# 6. Relationships (Связи между ветками)
bridge.add_relationship(
    "Слой персистентности (DrawingService.ts)",
    "Шаг 7: Связка с DrawingService & E2E тесты",
    label="Синхронизация стейта",
    line_color="#2B6CB0",
    line_style="DASH",
)

bridge.add_relationship(
    "Анализ протокола WebSocket котировок",
    "DATA_FLOW.md (Схема потоков данных)",
    label="Спецификация сообщений",
    line_color="#DD6B20",
    line_style="SOLID",
)

bridge.add_relationship(
    "Шаг 1: Векторные иконки (icons.tsx)",
    "Шаг 4: Панель избранного (FavoriteToolbar.tsx)",
    label="Иконки кнопок",
    line_color="#38A169",
    line_style="SOLID",
)
print("[7/8] Relationships added", flush=True)

# 7. Review Comment
bridge.add_comment(
    "План внедрения (7 Шагов SolidJS)",
    "Клод выполняет Шаги 1-3. Шаги 4-7 запланированы на следующий спринт.",
    "Max AI (Navigator)",
)
print("[8/8] Review comment added", flush=True)

# 8. Save and open
import shutil
save_doc_path = os.path.expanduser(r"~\Documents\AI-Trading-Roadmap.mmap")
doc.SaveAs(save_doc_path)
print(f"Map saved to: {save_doc_path}", flush=True)

ai_trading_path = r"D:\Dev\AI-Trading\AI-Trading-Roadmap.mmap"
shutil.copy2(save_doc_path, ai_trading_path)
print(f"Map copied to project folder: {ai_trading_path}", flush=True)

os.startfile(ai_trading_path)
print(f"SUCCESS: AI-Trading mindmap built, saved and opened in MindManager GUI!", flush=True)

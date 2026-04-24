# gainz-tracker

> CLI tool to log and visualize workout progress from CSV exports of fitness apps

---

## Installation

```bash
pip install gainz-tracker
```

Or install from source:

```bash
git clone https://github.com/yourusername/gainz-tracker.git
cd gainz-tracker
pip install -e .
```

---

## Usage

Import a CSV export from your fitness app and start tracking:

```bash
# Import a CSV file
gainz import --file my_workouts.csv --app stronglifts

# View progress for a specific exercise
gainz progress --exercise "Bench Press" --last 30days

# Generate a visual chart
gainz chart --exercise "Squat" --output squat_progress.png
```

**Supported apps:** Strong, Stronglifts, JEFIT, Hevy

---

## Features

- 📥 Parse CSV exports from popular fitness apps
- 📊 Visualize strength progress over time
- 🏋️ Track volume, max weight, and estimated 1RM
- 📅 Filter by date range or exercise

---

## Requirements

- Python 3.9+
- `pandas`, `matplotlib`, `click`

---

## License

This project is licensed under the [MIT License](LICENSE).
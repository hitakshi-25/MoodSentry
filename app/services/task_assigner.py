import random
from app.database import get_db
import psycopg2.extras

AI_ASSIGNED_BY_ID = 1

MOOD_TASK_MAP = {
    "happy":       ("Work on high-priority task", "Proceed with a critical project task.", "High"),
    "motivated":   ("Work on high-priority task", "Proceed with a critical project task.", "High"),
    "neutral":     ("Continue with standard tasks", "Keep working on your assigned tasks.", "Medium"),
    "calm":        ("Continue with standard tasks", "Keep working on your assigned tasks.", "Medium"),
    "stressed":    ("Take a short break or review light tasks", "Low pressure work assigned for stress recovery.", "Low"),
    "sad":         ("Focus on simple tasks or take a break", "Assign easy or relaxing work.", "Low"),
    "angry":       ("De-escalate with solo or quiet task", "Assigned independent or non-pressuring tasks.", "Low"),
    "fear":        ("Light analysis or documentation work", "Assign calm-focused work like reading or documenting.", "Low"),
    "surprise":   ("Review recent tasks and reflect", "Assigned reflection task to ground your focus.", "Medium"),
    "disgust":     ("Solo task with minimal social input", "Assign work requiring minimal collaboration.", "Low"),
    "bored":       ("Try a creative mini-task or ideation", "Boost engagement with creative, optional task.", "Medium")
}

def assign_task_based_on_mood(user_id, emotion):
    db = get_db()
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    task_data = MOOD_TASK_MAP.get(emotion.lower(), (
        "Complete a standard task", "Maintain your workflow with regular task.", "Medium"
    ))

    task_title = task_data[0]
    task_description = task_data[1]
    priority = task_data[2].capitalize()  # 🛠 ENSURE 'Low', 'Medium', 'High'
    print("Debug priority:", priority) 

    try:
        cursor.execute(
            "INSERT INTO tasks (assigned_to, task_title, task_description, priority, assigned_by) VALUES (%s, %s, %s, %s, %s)",
            (user_id, task_title, task_description, priority, AI_ASSIGNED_BY_ID)
        )
        # 🧠 Log mood to mood_history table
        cursor.execute(
            "INSERT INTO mood_history (user_id, mood, detection_method) VALUES (%s, %s, %s)",
            (user_id, emotion, "facial")  # or "text"/"voice" based on route
        )
        cursor.execute(
            "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
            (user_id, f"Mood: {emotion} → Task: {task_title} [{priority}]")
        )

        db.commit()

        if emotion.lower() == "stressed":
            cursor.execute("SELECT hr_id FROM users WHERE id = %s", (user_id,))
            hr = cursor.fetchone()
            if hr and hr["hr_id"]:
                from app.services.notification import notify_hr_of_stress
                notify_hr_of_stress(
                    user_id,
                    hr["hr_id"],
                    f"⚠️ Employee ID {user_id} has reported being stressed. Assigning stress recovery task."
                )

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Task insert failed: {e}")
        raise e
    finally:
        cursor.close()
        db.close()

    return {
        "task_title": task_title,
        "description": task_description,
        "priority": priority
    }


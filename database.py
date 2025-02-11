#%%
from adapter import PostgresAdapter
import json
database = PostgresAdapter()
#%%
def store_question_output(doubts_id, grade,subject, question,hints,steps,final_answer, llama_feedback):
    pool = database.get_pool_connection()
    with pool.connection() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO doubts (doubts_id, grade,subject, question,hints,steps,final_answer, llama_feedback) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (doubts_id, grade,subject, question,json.dumps(hints),json.dumps(steps),final_answer, llama_feedback),
                )
                conn.commit()
        except Exception as e:
            print(f"Error inserting message: {e}")
            conn.rollback()

# %%
# store_question_output(123, 12, "TESTING", "TESTING", "TESTING")
# %%

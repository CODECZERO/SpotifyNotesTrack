from django.db import connection
from psycopg2.extras import execute_values
from .queries import QUERIES

def run_query(query_name: str, prams=None, commit=False, fetchone=False, 
              fetchall=False, batch=False):
    sql= QUERIES.get(query_name)
    if not sql:
        raise ValueError(f"query not found {query_name}")
    
    with connection.cursor() as curr:
        if batch:
            execute_values(curr, sql, prams)
        else:
            curr.execute(sql, prams or ())
        
        if commit:
            connection.commit()
        
        if fetchone:
            return curr.fetchone()
        
        if fetchall:
            return curr.fetchall()

def create_table():
    return run_query("create_notes_table")

def insert_notes(userId: str,trackId: str, notesText: str):
    return run_query("insert_into_playlistNotes", 
                     prams=(userId, trackId, notesText,))

def select_notes(trackId: str):
    return run_query("select_notes_by_music", prams=(trackId,), fetchall=True)


def update_notes(userId: str, trackId: str):
    return run_query("update_notes", prams=(userId, trackId, ),)

def delete_notes(userId: str, trackId: str):
    return run_query("", prams=(userId, trackId,))

def upsert_notes(userId: str, trackId: str, notesText: str):
    existing= run_query("select_notes_by_music", prams=(trackId,), fetchall=True)
    
    userNotes=next((n for n in existing if n[1]==userId),None)
    
    if userNotes:
        update_notes(userId, trackId)
    else:
        insert_notes(userId, trackId, notesText)
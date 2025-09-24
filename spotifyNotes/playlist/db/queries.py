QUERIES = {
    #===Table Creation ==
    
    "create_notes_table": """
        CREATE TABLE IF NOT EXISTS playlistNotesTrack(
            Id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            userId VARCHAR(100) NOT NULL,
            trackId VARCHAR(100) NOT NULL,
            notesText TEXT,
            createdAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updatedAT TIMESTAMP DEFAULT CURRENT_TIMESTAMP    
        );
    """,
    
    "select_notes_by_music": """
        SELECT notesText FROM playlistNotesTrack 
        where trackId=%s;
    """,
    
    "delete_by_userID": """
        DELETE FROM playlistNotesTrack WHERE userId=%s AND trackId=%s;
    """,
    
    "insert_into_playlistNotes": """
        INSERT INTO playlistNotesTrack(userId,trackId,notesText) 
        VALUES (%s,%s,%s);
    """,
    
    "update_notes": """
        UPDATE playlistNotesTrack SET notesText=%s, updateAT=NOW()
        WHERE userId=%s AND trackId=%s;
    """
}
// sticky_notes.js
document.addEventListener('DOMContentLoaded', () => {
  const trackList = document.getElementById('track-list');
  const stickiesRoot = document.getElementById('stickies-root');

  // CSRF helper (Django)
  function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }
  const csrftoken = getCookie('csrftoken');

  // loaded notes keyed by track_id
  let notesMap = {};

  async function fetchNotes() {
    const res = await fetch('/playlists/api/notes/');
    const data = await res.json();
    notesMap = {}; // reset
    data.notes.forEach(n => notesMap[n.track_id] = n);
    renderAllStickies();
  }

  function renderAllStickies() {
    // clear root
    stickiesRoot.innerHTML = '';
    // for each note, create sticky and position it; simple positioning stacks them
    let offsetY = 8;
    Object.values(notesMap).forEach(n => {
      const sticky = createStickyElement(n.track_id, n.note_text, n.id);
      sticky.style.top = offsetY + 'px';
      sticky.style.right = '8px';
      offsetY += 150; // stack vertically
      stickiesRoot.appendChild(sticky);
    });
  }

  function createStickyElement(trackId, text, noteId) {
    const el = document.createElement('div');
    el.className = 'sticky-note';
    el.dataset.trackId = trackId;
    el.dataset.noteId = noteId || '';

    const textarea = document.createElement('textarea');
    textarea.className = 'note-text';
    textarea.value = text || '';
    el.appendChild(textarea);

    const actions = document.createElement('div');
    actions.className = 'note-actions';

    const saveBtn = document.createElement('button');
    saveBtn.innerText = 'Save';
    saveBtn.onclick = async (e) => {
      e.stopPropagation();
      await saveNote(trackId, textarea.value, el);
    };

    const delBtn = document.createElement('button');
    delBtn.innerText = 'Delete';
    delBtn.onclick = async (e) => {
      e.stopPropagation();
      if (el.dataset.noteId) {
        await deleteNote(el.dataset.noteId);
      } else {
        // no id yet — just remove UI and clear map
        delete notesMap[trackId];
        renderAllStickies();
      }
    };

    actions.appendChild(saveBtn);
    actions.appendChild(delBtn);
    el.appendChild(actions);

    // make draggable (simple)
    makeDraggable(el);

    return el;
  }

  // simple drag implementation
  function makeDraggable(el) {
    let isDown = false;
    let startX, startY, startLeft, startTop;
    el.addEventListener('pointerdown', (e) => {
      isDown = true;
      startX = e.clientX;
      startY = e.clientY;
      const rect = el.getBoundingClientRect();
      startLeft = rect.left;
      startTop = rect.top;
      el.setPointerCapture(e.pointerId);
    });
    window.addEventListener('pointermove', (e) => {
      if (!isDown) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      el.style.left = (startLeft + dx - stickiesRoot.getBoundingClientRect().left) + 'px';
      el.style.top  = (startTop + dy - stickiesRoot.getBoundingClientRect().top) + 'px';
      el.style.right = 'auto';
    });
    window.addEventListener('pointerup', (e) => {
      isDown = false;
    });
  }

  // save (create or update) note
  async function saveNote(trackId, noteText, el) {
    const payload = {track_id: trackId, note_text: noteText};
    const res = await fetch('/playlists/api/notes/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken},
      body: JSON.stringify(payload)
    });
    const d = await res.json();
    // server responds with created/updated and id
    const noteId = d.id;
    notesMap[trackId] = {id: noteId, track_id: trackId, note_text: noteText};
    // store id on element for delete
    if (el) el.dataset.noteId = noteId;
    renderAllStickies();
  }

  async function deleteNote(noteId) {
    const res = await fetch(`/playlists/api/notes/${noteId}/`, {
      method: 'DELETE',
      headers: {'X-CSRFToken': csrftoken}
    });
    if (res.ok) {
      // remove from notesMap
      for (const k in notesMap) {
        if (notesMap[k].id == noteId) {
          delete notesMap[k];
          break;
        }
      }
      renderAllStickies();
    }
  }

  // wire up track buttons
  trackList.querySelectorAll('.track-item').forEach(li => {
    const trackId = li.dataset.trackId;
    const btn = li.querySelector('.toggle-sticky-btn');
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      // if sticky exists, focus it; else create a new empty sticky
      if (notesMap[trackId]) {
        renderAllStickies();
        // optionally highlight the sticky (left for you)
      } else {
        // create an empty sticky in UI; save will POST
        const fake = {track_id: trackId, note_text: ''};
        notesMap[trackId] = {id: null, track_id: trackId, note_text: ''};
        renderAllStickies();
      }
    });
  });

  // initial load
  fetchNotes();
});

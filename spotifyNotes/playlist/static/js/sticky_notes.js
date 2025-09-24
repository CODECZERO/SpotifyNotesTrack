document.addEventListener("DOMContentLoaded", () => {
    const notes = document.querySelectorAll(".sticky-note");
    notes.forEach(note => {
        note.onmousedown = function(event) {
            let shiftX = event.clientX - note.getBoundingClientRect().left;
            let shiftY = event.clientY - note.getBoundingClientRect().top;

            function moveAt(pageX, pageY) {
                note.style.left = pageX - shiftX + 'px';
                note.style.top = pageY - shiftY + 'px';
            }

            function onMouseMove(event) {
                moveAt(event.pageX, event.pageY);
            }

            document.addEventListener('mousemove', onMouseMove);

            note.onmouseup = function() {
                document.removeEventListener('mousemove', onMouseMove);
                note.onmouseup = null;
            };
        };

        note.ondragstart = function() {
            return false;
        };
    });
});

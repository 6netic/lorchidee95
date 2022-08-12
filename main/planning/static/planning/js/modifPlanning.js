function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function addComment(id, commentCell, modifButton) {
    let this_id = document.getElementById(id).value;
    let comments = document.getElementById(commentCell).textContent;
    document.getElementById(commentCell).textContent = "";
    let comments_cell = document.getElementById(commentCell);
    let txt_area = document.createElement('textArea');
    txt_area.textContent = comments;
    comments_cell.appendChild(txt_area);
    let save_btn = document.createElement("button");
    save_btn.style.position = "relative";
    save_btn.style.backgroundColor = "#4CAF50";
    save_btn.style.border = "none";
    save_btn.style.color = "white";
    save_btn.style.textAlign = "center";
    save_btn.style.width = "50%";
    save_btn.textContent = "Enregistrer";
    save_btn.style.marginTop = "3%";
    comments_cell.appendChild(save_btn);
    let modif_btn = document.getElementById(modifButton);
    modif_btn.setAttribute("disabled", "disabled");
    save_btn.onclick = function() {
        comment_content = txt_area.value;
        modif_btn.removeAttribute("disabled");
        /* -------------------- Ajax --------------------------- */
        const request = new Request("save_comment", { headers: { 'X-CSRFToken': csrftoken }});
        let formData = new FormData();
        formData.append("this_id", this_id)
        formData.append("comment_content", comment_content);
        fetch(request, { method: "POST", mode: "same-origin", body: formData })
        .then(function(response) {
        if (response.status == 200) {
            document.getElementById(commentCell).textContent = txt_area.value;
            }
        })
        .catch(function(error) {
            console.log("L'enregistrement du commentaire en base de données a échoué.")
        });

    }
}


function validateLine(id, line, modifCell, completedCell) {
    /* -------------------- Ajax --------------------------- */
    const request = new Request("validate_line", { headers: { 'X-CSRFToken': csrftoken }});
    let formData = new FormData();
    formData.append("this_id", document.getElementById(id).value);
    fetch(request, { method: "POST", mode: "same-origin", body: formData })
    .then(function(response) {
        if (response.status == 200) {
            document.getElementById(line).style.backgroundColor = "#E9E6E6";
            document.getElementById(modifCell).textContent = "";
            document.getElementById(completedCell).textContent = "Terminé";
        }
    })
    .catch(function(error) {
        console.log("Cette ligne n'a pas été traitée comme terminée en base de données.");
    });
}

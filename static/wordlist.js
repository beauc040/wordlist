async function wordPopup(id) {
    popups = document.getElementsByClassName("popup");
    popup = document.getElementById(id + "-popup");
    for (let i = 0; i < popups.length; i++) {
        if (popups[i] !== popup)
            popups[i].style.visibility = "hidden";
    }

    let opts = {
        method: "GET",
    };
    let resp = await fetch("/proxy?word=" + id, opts);
    let definitions = await resp.json();
    popup.innerHTML = id + ":<p><ul>";
    for (let i = 0; i < definitions.length; i++)
        popup.innerHTML += "<li>" + definitions[i] + "</li>";
    popup.innerHTML += "</ul>";
    popup.style.visibility = popup.style.visibility == "visible" ? "hidden" : "visible";
}

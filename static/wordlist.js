async function wordPopup(id) {
    console.log("Clicked " + id);
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
    popup.innerHTML = id + "<br/>" + definitions;
    popup.style.visibility = popup.style.visibility == "visible" ? "hidden" : "visible";
}

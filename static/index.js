function copy() {
    let p = document.getElementById("cp");
    p.select();
    p.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(p.value);
    alert(p.value);
}
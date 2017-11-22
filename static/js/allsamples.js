document.getElementById("sortid").selectedIndex = sessionStorage.getItem("sort");
document.getElementById("dirid").selectedIndex = sessionStorage.getItem("dir");

alert("test");
alert(sessionStorage.getItem("sort"));
alert(sessionStorage.getItem("dir"));

function submitThis() {
    sessionStorage.setItem("sort", document.getElementById("sortid").selectedIndex);
    sessionStorage.setItem("dir", document.getElementById("dirid").selectedIndex);

    document.getElementById("selection").submit();
}
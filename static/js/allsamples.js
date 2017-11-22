if (sessionStorage.getItem("sort") != null || sessionStorage.getItem("dir") != null){
    alert("hi");
    alert(sessionStorage.getItem("sort"));
    alert(sessionStorage.getItem("dir"));
    document.getElementById("sortid").selectedIndex = sessionStorage.getItem("sort");
    document.getElementById("dirid").selectedIndex = sessionStorage.getItem("dir");
    alert(document.getElementById("sortid").selectedIndex);
    alert(document.getElementById("dirid").selectedIndex);
}

function submitThis() {
    sessionStorage.setItem("sort", document.getElementById("sortid").selectedIndex);
    sessionStorage.setItem("dir", document.getElementById("dirid").selectedIndex);

    document.getElementById("selection").submit();
}
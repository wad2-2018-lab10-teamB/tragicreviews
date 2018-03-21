document.getElementById("id_staff_level").disabled = true;
document.getElementById("id_student_level").disabled = true;
document.getElementById("id_group").onchange = function(){
    if (document.getElementById("id_group").value === "1"){
        document.getElementById("id_staff_level").disabled = true;
        document.getElementById("id_student_level").disabled = false;
    } else if (document.getElementById("id_group").value === "2"){
        document.getElementById("id_staff_level").disabled = false;
        document.getElementById("id_student_level").disabled = true;
    } else {
        alert("No input >.<");
        document.getElementById("id_staff_level").disabled = true;
        document.getElementById("id_student_level").disabled = true;
    }
};

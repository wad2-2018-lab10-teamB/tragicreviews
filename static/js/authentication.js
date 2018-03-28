// checking whether a new password is same as old one or not
function isDifferentNewPwd() {
    var old_pwd = document.getElementById("id_old_password").value;
    var new_pwd = document.getElementById("id_new_password1").value;
    var new_pwd2 = document.getElementById("id_new_password2").value;
    if (old_pwd === new_pwd) {
        alert("Your new password should not be the same as your old password >.<");
        return false;
    } else if(new_pwd !== new_pwd2){
        alert("The two password fields didn't match >.<");
        return false;
    }else {
        return true;
    }
}

// a naive implementation of user authorisation
// too lazy to use regExp :<
function isValidEmail() {
    var email = document.getElementById("id_email").value;
    var domain = email.split("@")[1].toLowerCase();
    var group = document.getElementById("id_group").value;
    if ((domain.search("gla.ac.uk") !== -1) || (domain.search("glasgow.ac.uk") !== -1)) {
        if (domain.search("student") !== -1) {
            if (group !== "1") {
                alert("Not a staff email, please register as a student >.<");
                return false;
            }
        } else {
            if (group !== "2") {
                alert("Please register as a staff >.<");
                return false;
            }
        }
    } else {
        if (group !== "1") {
            alert("Not a staff email, please register as a student >.<");
            return false;
        }
    }
    return true;
}

function showTos() {
    var popup = document.getElementById("tospopup");
    popup.classList.toggle("show");
}

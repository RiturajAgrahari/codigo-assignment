function myFunction() {
  document.getElementById("error-msg").style.visibility = "hidden";
}

function addComment(id) {
    var elements = document.getElementsByClassName('comment-form');
    for (var i in elements) {
      if (elements.hasOwnProperty(i)) {
        elements[i].style.display = 'none';
      }
    }
    document.getElementById(`${id}`).style.display = "flex";
}

const composeEmail = (body) => {
    window.open(`http://mail.google.com/mail/?view=cm&fs=1&tf=1&su=Checkout my new blog&body=${body}`);
};

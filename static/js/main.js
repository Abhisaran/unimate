var current_cohort = ""

function openTab(evt, cohortName) {
    // Declare all variables
    var i, tabcontent, tablinks;
    current_cohort = cohortName
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cohortName).style.display = "block";
    evt.currentTarget.className += " active";
    get_cohort_data(cohortName)
}


// function get_cohort_data() {
//     let data = {cohort_id: "rmit-university-2020-1-computer-science"};
//
//     url = "https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/get-cohort"
//     fetch(url, {
//         method: "POST",
//         body: JSON.stringify(data)
//     }).then(res => {
//         console.log(res);
//     });
// }


function get_cohort_data(cohortName) {
    console.log("COHORT DATA")
    console.log(cohortName)
    fetch(`/get_cohort_data/${cohortName}`)
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.log('Looks like there was a problem. Status Code: ' +
                        response.status);
                    return;
                }
                // Examine the text in the response
                response.json().then(function (data) {
                    console.log(data);
                    response_data = data
                    divTop = document.getElementById(cohortName)
                    divTop.innerText = ''
                    var keys = Object.keys(response_data); // ['key1', 'key2']
                    keys.forEach(function (key) {
                        var values = response_data[key]
                        console.log(values)
                        let div = document.createElement('div')
                        div.className = "post-div"
                        let messageDiv = document.createElement('div')
                        messageDiv.className = "message-div"
                        let messageDivSubject = document.createElement('h2')
                        messageDivSubject.className = "message-div-subject"
                        messageDivSubject.innerText = values['subject']
                        let messageDivDesc = document.createElement('p')
                        messageDivDesc.className = "message-div-desc"
                        messageDivDesc.innerText = values['message']
                        let messageDivDate = document.createElement('p')
                        messageDivDate.className = "message-div-Date"
                        messageDivDate.innerText = "Date posted: "+ (values['date'].toString()).split('.')[0]
                        let messageDivContact = document.createElement('p')
                        messageDivContact.className = "message-div-Contact"
                        messageDivContact.innerText = "Contact: " + values['contact']
                        let messageDivDiv  = document.createElement('div')
                        messageDivDiv.className = "message-div-div"
                        let messageDivDivImage  = document.createElement('img')
                        messageDivDivImage.className = "message-div-div-img"
                        messageDivDivImage.src = values['author_image']
                        let messageDivDivName  = document.createElement('p')
                        messageDivDivName.className = "message-div-div-name"
                        messageDivDivName.innerText = values['author_name']
                        messageDivDiv.appendChild(messageDivDivImage)
                        messageDivDiv.appendChild(messageDivDivName)
                        messageDiv.appendChild(messageDivSubject)
                        messageDiv.appendChild(messageDivDesc)
                        messageDiv.appendChild(messageDivDate)
                        messageDiv.appendChild(messageDivContact)
                        div.appendChild(messageDiv)
                        div.appendChild(messageDivDiv)
                        divTop.appendChild(div)
                    })
                    // for (var da in response_data) {
                    //     if (response_data.hasOwnProperty(da)) {
                    //
                    //         console.log(response_data[da])
                    //         p = document.createElement('p')
                    //         p.innerText = response_data[da]
                    //         div.appendChild(p)
                    //     }
                    // }
                });
            }
        )
        .catch(function (err) {
            console.log('Fetch Error :-S', err);
        });
}

function put_cohort_data() {
    var cohort_id, subject, message
    subject = document.getElementById('right-container-form-subject').value
    message = document.getElementById('right-container-form-desc').value
    if (current_cohort) {
        cohort_id = current_cohort
    } else {
        alert("Choose a group first")
        return
    }
    if (!subject) {
        alert("Subject cannot be empty")
        return
    }
    if (!message) {
        alert("Message cannot be empty")
        return
    }
    const data = {cohort_id: cohort_id, subject: subject, message: message};
    var auth_id = document.getElementById("main_auth_id").innerText

    fetch(`/put_cohort_data/${auth_id}`, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            get_cohort_data(cohort_id)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

$(document).ready(function(){
    $("#modal").trigger('click');
});

// get_cohort_data()
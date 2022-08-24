document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // send mail
  document.querySelector('#compose-form').onsubmit = sendmail;

  // By default, load the inbox
  load_mailbox('inbox');
});

// send email function
function sendmail(event){
  event.preventDefault()
  const recipients = document.querySelector("#compose-recipients").value;  
  const subject = document.querySelector("#compose-subject").value;  
  const body = document.querySelector("#compose-body").value;
  // Post email to API route
  fetch('/emails' , {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => { 
    if (!response.ok) {throw response }
    else{return response.json()}
  })
  .then(result => {
    console.log(result);    // console log the result
  })
  .catch((error) => { // error handling
    error.text().then( errorMessage => {
      console.error(errorMessage);     // log the error  
      document.querySelector("#errorMessage").classList.remove('d-none');          
      document.querySelector("#errorMessage").classList.add('d-block');  
      document.querySelector("#errorMessage").innerHTML = errorMessage;
    })              
  });
  load_mailbox('sent');
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';  
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  // document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}


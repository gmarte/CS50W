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

  // Post send email 
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
function view_email(id){
  fetch('/emails/'+ id)
    .then(response => response.json())
    .then(email => {
      const email_views = document.querySelector('#emails-view');
      // Print email
      console.log(email);
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      email_views.style.display = 'block';
      // Show the mailbox name
      email_views.innerHTML = `
      <h3>${email['subject'].toUpperCase()}</h3>
      <div class="btn-group">
                <button type="button" class="btn btn-outline-primary">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply" viewBox="0 0 16 16">
                <path d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.74 8.74 0 0 0-1.921-.306 7.404 7.404 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254a.503.503 0 0 0-.042-.028.147.147 0 0 1 0-.252.499.499 0 0 0 .042-.028l3.984-2.933zM7.8 10.386c.068 0 .143.003.223.006.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96v-.667z"/>
                </svg>
                  <span class="visually-hidden">Reply</span>
                </button> 
                <button type="button" class="btn btn-outline-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive" viewBox="0 0 16 16">
                    <path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"></path>
                  </svg>
                  <span class="visually-hidden">Archive</span>
                </button>                               
              </div>
      `;
      let div = document.createElement('div');

      // mark as read
      email_read(id, true);     
      // email_archived(id, false);
  });
}

function email_read(id, status){
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({ read : status })
  })
}
function email_archived(id, status){
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({ archived : status })
  })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  const email_views = document.querySelector('#emails-view');

  // Show the mailbox name
  email_views.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  

  // getting the emails
  
  fetch('/emails/' + mailbox)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {        
        let div = document.createElement('div');
        let ahref = document.createElement('a');
        div.classList.add("list-group");
        ahref.className = "list-group-item text-decoration-none";
        // console.log("read or not" + email['read']);
        if (email['read']){
          ahref.classList.add("read");
        }else {
          ahref.classList.remove("read");
        }                
        ahref.innerHTML = `
            <label><input data-section="${email['id']}" type="checkbox"></label> 
            <span class="badge badge-info m-2">${email['sender']}</span>
            <span class="pr-2">${email['subject']}</span>
            <span class="text-muted text-truncate" style="font-size: 11px; max-width: 25%">${email['body']}</span>
            <span class="badge badge-primary float-right m-2">${email['timestamp']} </span>
        `;

        // add listener and append to DOM
        ahref.addEventListener('click', () => view_email(email['id']));
        div.appendChild(ahref);        
        email_views.appendChild(div);
    });
    });
  // <div class="list-group">
  //           <a href="#" class="list-group-item text-decoration-none read">                
  //               <label><input type="checkbox"></label>                
  //               <span class="badge badge-info m-2">Andres posada</span>
  //               <span class="pr-2">Nice work on the lastest version</span>
  //               <span class="text-muted text-truncate" style="font-size: 11px; max-width: 25%">- More content here aasdasdasdsadasdsadsadsadsadasdasdsdasdasdasdasasdasdasdasdasdsadasdasd</span>
  //               <span class="badge badge-primary float-right m-2">12:10 AM</span>                
  //           </a> 
  // </div>

}


const unReadIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-open-fill" viewBox="0 0 16 16">
<path d="M8.941.435a2 2 0 0 0-1.882 0l-6 3.2A2 2 0 0 0 0 5.4v.314l6.709 3.932L8 8.928l1.291.718L16 5.714V5.4a2 2 0 0 0-1.059-1.765l-6-3.2ZM16 6.873l-5.693 3.337L16 13.372v-6.5Zm-.059 7.611L8 10.072.059 14.484A2 2 0 0 0 2 16h12a2 2 0 0 0 1.941-1.516ZM0 13.373l5.693-3.163L0 6.873v6.5Z"/>
</svg>
<!--<span class="visually-hidden">Unread</span>-->`;
const readIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope" viewBox="0 0 16 16">
<path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V4Zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1H2Zm13 2.383-4.708 2.825L15 11.105V5.383Zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741ZM1 11.105l4.708-2.897L1 5.383v5.722Z"/>
</svg>
<!--<span class="visually-hidden">Read</span>-->`;
const replyIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply" viewBox="0 0 16 16">
<path d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.74 8.74 0 0 0-1.921-.306 7.404 7.404 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254a.503.503 0 0 0-.042-.028.147.147 0 0 1 0-.252.499.499 0 0 0 .042-.028l3.984-2.933zM7.8 10.386c.068 0 .143.003.223.006.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96v-.667z"/>
</svg>
  <!--<span class="visually-hidden">Reply</span>-->`;
const archiveIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive" viewBox="0 0 16 16">
<path d="M0 2a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1v7.5a2.5 2.5 0 0 1-2.5 2.5h-9A2.5 2.5 0 0 1 1 12.5V5a1 1 0 0 1-1-1V2zm2 3v7.5A1.5 1.5 0 0 0 3.5 14h9a1.5 1.5 0 0 0 1.5-1.5V5H2zm13-3H1v2h14V2zM5 7.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z"></path>
</svg>
<!--<span class="visually-hidden">Archive</span>-->`;  

const unArchiveIcon =`<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-archive-fill" viewBox="0 0 16 16">
<path d="M12.643 15C13.979 15 15 13.845 15 12.5V5H1v7.5C1 13.845 2.021 15 3.357 15h9.286zM5.5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1 0-1zM.8 1a.8.8 0 0 0-.8.8V3a.8.8 0 0 0 .8.8h14.4A.8.8 0 0 0 16 3V1.8a.8.8 0 0 0-.8-.8H.8z"/>
</svg>
<!--<span class="visually-hidden">Back to inbox</span>-->`;

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
function sendmail(e){
  e.preventDefault() // avoids page reload to inbox after sending email
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
    if (!response.ok) {throw response  }//throw exception
    else{return response.json()}
  })
  .then(result => {
    console.log(result);    // console log the result
    localStorage.clear();
    load_mailbox('sent');
  })
  .catch((error) => { // error handling
    error.text().then( errorMessage => {
      console.error(errorMessage);     // log the error        
      document.querySelector("#errorMessage").classList.remove('d-none');          
      document.querySelector("#errorMessage").classList.add('d-block');  
      document.querySelector("#errorMessage").innerHTML = errorMessage;
    })                
  });    
}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-single').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';  
}
function buttongroup(email){
  let div = document.createElement('div');
  div.className = 'btn-group sm-2';
    // create reply button & append to DOMContentLoaded
    const reply = document.createElement('button');
    reply.className = "btn btn-outline-primary";       
    reply.innerHTML = replyIcon;
    reply.addEventListener('click', function() {    
    compose_email();  // show form         
    document.querySelector('#compose-recipients').value = email.sender;
    let subject = email.subject;    
    if (subject.split(" ", 1)[0] != "Re:") { //Reply tittle logic
      subject = "Re: " + subject;
    }
    document.querySelector('#compose-subject').value = subject;

    let body = `
      >>> On ${email.timestamp}, ${email.sender} wrote: ${email.body}
    `;
    document.querySelector('#compose-body').value = body;
    });
    div.appendChild(reply);    

    const grparchive = document.createElement('button');
    grparchive.className = "btn btn-outline-primary";
    grparchive.innerHTML = !email.archived ? archiveIcon:unArchiveIcon;  
    div.appendChild(grparchive);
    grparchive.addEventListener('click', () => email_archived(email.id, !email.archived));                    
    

    const grpread = document.createElement('button');
    grpread.className = "btn btn-outline-primary";
    grpread.innerHTML = !email.read ? readIcon:unReadIcon;
    div.appendChild(grpread);
    grpread.addEventListener('click', () => email_read(email.id, !email.read) );

   return div;
}
function buttonGroupInbox(email){
  let div = document.createElement('div');
  div.className = 'btn-group sm-2';    
  const grparchive = document.createElement('button');
  grparchive.className = "btn btn-outline-primary";
  grparchive.innerHTML = !email.archived ? archiveIcon:unArchiveIcon;  
  div.appendChild(grparchive);
  grparchive.addEventListener('click', () => email_archived(email.id, !email.archived));                    
    

  const grpread = document.createElement('button');
  grpread.className = "btn btn-outline-primary";
  grpread.innerHTML = !email.read ? readIcon:unReadIcon;
  div.appendChild(grpread);
  grpread.addEventListener('click', () => email_read(email.id, !email.read) );

  return div;
}
function view_email(id){
  fetch('/emails/'+ id)
    .then(response => response.json())
    .then(email => {
      const email_views = document.querySelector('#emails-single'); // single email view div
      // log email
      console.log(email);
      // mark as read
      email_read(id, true);         
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      email_views.style.display = 'block';
      email_views.innerHTML = ``;                                 
      let btnGroup = buttongroup(email);      
      let the_email = document.createElement('div');
      the_email.innerHTML = `
      <h3 class="mt-3">${email.subject.toUpperCase()}</h3><span class="badge badge-primary float-right">date: ${email.timestamp}</span>
      <div><span class="font-weight-bold">from: ${email['sender']}</span></div>
      <div><span>to: ${email['recipients']} </span></div>
      <textarea disabled class="form-control">${email.body}</textarea>
      <hr>
      `; 
      email_views.appendChild(btnGroup);
      email_views.appendChild(the_email);                
  });
}
function email_read(id, status){
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({ read : status })
  });
  if (!status){ // doesnt reload unless is from read -> unread
    load_mailbox('inbox');
    window.location.reload();
  }
}
function email_archived(id, status){
  fetch('/emails/' + id, {
    method: 'PUT',
    body: JSON.stringify({ archived : status })    
  });
  load_mailbox('inbox');
  window.location.reload();
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-single').style.display = 'none';

  const email_views = document.querySelector('#emails-view');

  // Show the mailbox name
  email_views.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // getting the emails
  fetch('/emails/' + mailbox, {
    headers: {
      'Cache-Control': 'no-cache'
    }})
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {        
        let div = document.createElement('div');
        let ahref = document.createElement('a');
        div.classList.add("list-group");
        ahref.className = "list-group-item text-decoration-none";        
        if (email.read){ // background color read:unread
          ahref.classList.add("read");
        }else {
          ahref.classList.remove("read");
        }
        let span = document.createElement('span');
        let spanGrp = document.createElement('span');
        span.className= 'badge badge-primary float-right m-2';
        spanGrp.className= 'float-right';
        span.innerHTML = email.timestamp; 
        ahref.innerHTML = `            
            <span class="badge badge-info m-2">${mailbox === 'inbox'?email.sender: email.recipients}</span>
            <span class="pr-2">${email.subject}</span>
            <span class="text-muted text-truncate" style="font-size: 11px; max-width: 25%">${email.body.substring(0,email.body.length > 20? 20:email.body.length)}</span>            
        `;        
        let btnGroup = buttonGroupInbox(email);
        ahref.addEventListener('click', () => view_email(email.id));
        if (mailbox != 'sent'){
          spanGrp.appendChild(btnGroup);
        }
        ahref.appendChild(span);
        ahref.appendChild(spanGrp);
        // ahref.appendChild(btnGroup);
        
        div.appendChild(ahref);              
        email_views.appendChild(div);      
    });
    });  
}


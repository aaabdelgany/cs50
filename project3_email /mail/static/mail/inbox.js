document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit',(e)=>{
    e.preventDefault();
    console.log('testing');
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log('idk bruh');
        
    });
    e.preventDefault();
    load_mailbox('sent');
  })
  // By default, load the inbox
  load_mailbox('inbox');
  console.log('fail');
});

function compose_email() {
  console.log('idk what');
  // Show compose view and hide other views
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  let my_email=document.querySelector('#email-view');
  my_email.style.display = 'none';
  if(my_email.hasChildNodes()){
    let email =document.querySelector('#email-view div');
    my_email.removeChild(email);
  }
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if (mailbox==='inbox'){
    fetch('/emails/inbox').then(response => response.json()).then(emails => {
    console.log(emails);
    emails.forEach((email)=>{
      const element = document.createElement('div');
      element.style.border="2px solid black";
      if (email.read===true){
        element.style.backgroundColor="grey"
      }else{
        element.style.backgroundColor="white"
      }
      element.innerHTML = `<p>Sender:${email.sender}</p><p>Timestamp:${email.timestamp}</p><p>Subject:${email.subject}</p><p>Body:${email.body}`;
      let x=email.id;
      element.addEventListener('click',()=>load_email(x))
      document.querySelector('#emails-view').append(element);
    })

  });
  }else if(mailbox==='sent'){
    fetch('/emails/sent').then(response => response.json()).then(emails => {
      console.log(emails);
      emails.forEach((email)=>{
        const element = document.createElement('div');
        element.style.border="2px solid black";
        if (email.read===true){
          element.style.backgroundColor="grey"
        }else{
          element.style.backgroundColor="white"
        }
        element.innerHTML = `<p>Recipient:${email.recipients}</p><p>Subject:${email.subject}</p><p>Body:${email.body}`;
        let x=email.id;
        //element.addEventListener('click',()=>load_email(x))
        document.querySelector('#emails-view').append(element);
      })
    })
  }else if(mailbox==='archive'){
    fetch('/emails/archive').then(response => response.json()).then(emails => {
      console.log(emails);
      emails.forEach((email)=>{
        const element = document.createElement('div');
        element.style.border="2px solid black";
        if (email.read===true){
          element.style.backgroundColor="grey"
        }else{
          element.style.backgroundColor="white"
        }
        element.innerHTML = `<p>Sender:${email.sender}</p>p>Timestamp:${email.timestamp}</p><p>Subject:${email.subject}</p><<p>Body:${email.body}`;
        let x=email.id;
        element.addEventListener('click',()=>load_email(x))
        document.querySelector('#emails-view').append(element); 
      })

    })
  }
}

function load_email(email_id){
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  fetch(`/emails/${email_id}`).then(response => response.json()).then(email => {
    console.log(email);
    const element=document.createElement('div');
    element.innerHTML=`<p>Sender: ${email.sender}</p><p>Recipient: ${email.recipients}</p><p>Subject: ${email.subject}</p><p>Timestamp: ${email.timestamp}</p><p>Body: ${email.body}`;
    document.querySelector('#email-view').append(element);
    my_button(email_id,email.archived)
    reply(email);
  });
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}
function my_button(email_id,archived){
  const button=document.createElement('button');
  if(archived===false){
    button.innerHTML='Click Here to Archive this Email!';
  }else{
    button.innerHTML='Click Here to Unarchive this Email!';
  }
  button.addEventListener('click',()=>{
    if (button.innerHTML==='Click Here to Archive this Email!'){
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      console.log('archived');
    }else{
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      console.log('unarchived');
    }
    setTimeout(()=>{load_mailbox('inbox')},100);
  })
  let email=document.querySelector('#email-view div');
  email.append(button);
}

function reply(email){
  const my_reply=document.createElement('button');
  my_reply.innerHTML='Click Here to Reply to this email!';
  my_reply.addEventListener('click',()=>{
  compose_email();
  document.querySelector('#compose-recipients').value=email.sender;
  document.querySelector('#compose-subject').value=`RE: ${email.subject}`;

  document.querySelector('#compose-body').value=`On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
  });
  let original=document.querySelector('#email-view div');
  original.append(my_reply);
  
}
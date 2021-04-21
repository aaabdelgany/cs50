document.addEventListener('DOMContentLoaded',()=>{
    const new_emp=document.querySelector('#new_employee');
    if (new_emp!=undefined){
        new_emp.addEventListener('click',()=>{
            flip_new()
        })
    }
    const employee=document.querySelector('#employee_mark');
    if (employee!=undefined){

    }

    const new_emp_submit=document.querySelector('#new_emp_submit')
    const danger_new=document.querySelector('#danger_new')
    if(new_emp_submit!=undefined){
        new_emp_submit.addEventListener('click',()=>{
            const first_name=document.querySelector('#first_name');
            const last_name=document.querySelector('#last_name');
            const email=document.querySelector('#email');
            const phone=document.querySelector('#phone');
            fetch('/abduHR/new',{
                method: 'POST',
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                body: JSON.stringify({
                    first_name:first_name.value,
                    last_name:last_name.value,
                    email:email.value,
                    phone:phone.value
                })
            }).then(response => response.json()).then(result => {
                    document.querySelector('#danger_new').innerHTML=result.message;
                    document.querySelector('#danger_new').style.display="";
                    if(result.new==1){
                        document.querySelector("#danger_new").classList.remove('alert-danger');
                        document.querySelector("#danger_new").classList.add('alert-success');
                        let num_childs=document.querySelector('#employee_list').childElementCount;
                        if (num_childs===10 || num_childs===25 || num_childs===50){
                            console.log('max');
                        }else{
                            const list_group=document.createElement('ul');
                            list_group.classList.add('list-group');
                            list_group.classList.add('list-group-horizontal-sm');
                            list_group.innerHTML=`<li class="list-group-item" style="flex:1;">${result.id}</li><li class="list-group-item" style="flex:1;">${last_name.value}, ${first_name.value}</li><li class="list-group-item" style="flex:1;"><a href="/abduHR/edit/${result.id}">Edit Employee</a></li>`
                            document.querySelector('#employee_list').append(list_group);
                        }
                        
                    }
            })
        })
    }

    const edit_emp=document.querySelector('#update_employee')
    if (edit_emp!=undefined){
        edit_emp.addEventListener('click',()=>{
            const first_name=document.querySelector('#first_name');
            const last_name=document.querySelector('#last_name');
            const email=document.querySelector('#email');
            const phone=document.querySelector('#phone');
            const status=document.querySelector('#status')
            const emp_id=document.querySelector('#employee_mark').dataset.id;
            const name=document.querySelector('#name');
            const status_label=document.querySelector('#status_label');
            fetch('/abduHR/edit/' + emp_id,{
                method: 'POST',
                headers: {"X-CSRFToken": getCookie("csrftoken")},
                body: JSON.stringify({
                    first_name:first_name.value,
                    last_name:last_name.value,
                    email:email.value,
                    phone:phone.value,
                    status_flag:status.checked
                })
            }).then(response => response.json()).then(result => {
                    document.querySelector('#danger_new').innerHTML=result.message;
                    document.querySelector('#danger_new').style.display="";
                    document.querySelector("#danger_new").classList.remove('alert-success');
                    document.querySelector("#danger_new").classList.add('alert-danger');
                    if(result.edit==1){
                        document.querySelector("#danger_new").classList.remove('alert-danger');
                        document.querySelector("#danger_new").classList.add('alert-success');
                        name.innerHTML=last_name.value + ', ' + first_name.value;
                        if(result.status_update===1){
                            if(name.style.textDecoration==="line-through"){
                                name.style.textDecoration="";
                            }else{
                                name.style.textDecoration="line-through";
                            }
                            if(status_label.innerHTML==="Click Here to Deactivate this Employee"){
                                status_label.innerHTML="Click Here to Reactivate this Employee"
                            }else{
                                status_label.innerHTML="Click Here to Deactivate this Employee"
                            }
                        }
                        
                    }
        })
    })}
    function flip_new(){
        const new_form=document.querySelector('#new_form')
        if(new_form.style.display===""){
            new_form.style.display="none";
        }else{
            new_form.style.display="";
        }
    }
        // JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})

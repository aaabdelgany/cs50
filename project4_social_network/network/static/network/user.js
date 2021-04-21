document.querySelector('#follow').onclick=()=>{
    let button=document.querySelector('#follow');
    console.log(button.dataset.follower);
    fetch('/follow',{
        method:'POST',
        body:JSON.stringify({
            follower:button.dataset.follower,
            followed:button.dataset.followed
        }),
        headers:{"X-CSRFToken": getCookie("csrftoken")}
    }).then(response=>response.json()).then(result=>{console.log(result)})
}
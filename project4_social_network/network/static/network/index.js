document.addEventListener('DOMContentLoaded',()=>{
    const username=document.querySelector('#user');


    let new_b=document.querySelector('#new_button');
    if(new_b!=undefined){
        new_b.addEventListener('click',()=>{
            document.querySelector('#new_button').style.display="none";
            document.querySelector('#new_post').style.display="block";
        })
    }   
    let follow_b=document.querySelector('#follow');
    if(follow_b!=undefined){
        follow_b.addEventListener('click',()=>{
            fetch('/follow',{
                method:'POST',
                body:JSON.stringify({
                    follower:follow_b.dataset.follower,
                    followed:follow_b.dataset.followed
                })
                    }).then(response=>response.json()).then(result=>{
                        console.log(result);
                        load_unfollow(result);
                    })
        })
    }

    let unfollow=document.querySelector('#unfollow');
    if(unfollow!=undefined){
        unfollow.addEventListener('click',()=>{
            console.log('why')
            fetch('/follow',{
                method:'POST',
                body:JSON.stringify({
                    follower:follow_b.dataset.follower,
                    followed:follow_b.dataset.followed
                })
                    }).then(response=>response.json()).then(result=>{
                        console.log(result);
                        load_follow(result);
                    })
        })
    }
    let posts=document.querySelectorAll('.post');
    if(posts!=undefined){
        posts.forEach(post=>{
            if (post.dataset.owner===username.dataset.user){
                let edit_button=document.createElement('button');
                edit_button.innerHTML="Edit post";
                let text_area=document.createElement('textarea');
                text_area.style.display="none";
                //<input type="submit" value="Submit">
                let submit=document.createElement('input');
                submit.value="Submit";
                submit.setAttribute('type','submit');
                submit.style.display="none";
                submit.addEventListener('click',()=>{
                    text_area.style.display="none";
                    submit.style.display="none";
                    edit_button.style.display="";
                    post.childNodes[4].style.display="";
                    post.childNodes[4].innerHTML=text_area.value;
                    fetch('/',{
                        method:'POST',
                        body:JSON.stringify({
                            id:post.dataset.id,
                            content:text_area.value
                        })
                            }).then(response=>response.json()).then(result=>{
                                console.log(result);
                            })
                })



                post.insertBefore(text_area,post.childNodes[2]);
                post.insertBefore(submit,post.childNodes[3]);
                edit_button.addEventListener('click',()=>{
                    text_area.style.display="block";
                    edit_button.style.display="none";
                    submit.style.display="block";
                    post.childNodes[4].style.display="none";
                })
                post.append(edit_button);
            }

        })
    }

    let likes=document.querySelectorAll('.like');
    likes.forEach(post=>{
        fetch('/user_like',{
            method:'POST',
            body:JSON.stringify({
                id:post.dataset.id,
            })
                }).then(response=>response.json()).then(result=>{
                    if(result.likes===true){
                        post.innerHTML="Unlike this post"
                    }else{
                        post.innerHTML="Like this post"
                    }
                    })
                

        post.addEventListener('click',()=>{
            fetch('/like',{
                method:'POST',
                body:JSON.stringify({
                    id:post.dataset.id,
                })
                    }).then(response=>response.json()).then(result=>{
                        post.previousSibling.innerHTML=result.num + ' People like this post'
                        console.log(result);
                        like_flip(post);
                    })
        })
    })
    function like_flip(post){
        if (post.innerHTML==="Like this post"){
            post.innerHTML="Unlike this post";
        }else{
            post.innerHTML="Like this post";
        }
    }

    function load_unfollow(result){
        document.querySelector('#follow').style.display="none";
        document.querySelector('#unfollow').style.display="block";
        document.querySelector('#follows-count').innerHTML='Follows: ' + result.follows;
        document.querySelector('#followed-count').innerHTML='Followed by: ' + result.followed;
    }
    function load_follow(result){
        document.querySelector('#unfollow').style.display="none";
        document.querySelector('#follow').style.display="block";
        document.querySelector('#follows-count').innerHTML='Follows: ' + result.follows;
        document.querySelector('#followed-count').innerHTML='Followed by: ' + result.followed;
    }

})


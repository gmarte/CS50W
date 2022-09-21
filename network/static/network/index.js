const like = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"></path>
                        </svg>`;
const unlike = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
<path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
</svg>`;      

document.addEventListener('DOMContentLoaded', function() {
  console.log("ini DOM");
  var spans = document.querySelectorAll("span, [id^='post_like_']");
  var edits = document.querySelectorAll("a, [id^='post_edit_']"); 
  
  for (var i = 0; i < spans.length; i++) {
      var self = spans[i];
      if (self.dataset.id){
        self.addEventListener('click', function (event) {  
          // prevent browser's default action
          event.preventDefault();
          console.log("calling like" + this.dataset.id);
          // calling the like action
          likeAction(this.dataset.id)
        }, false);
      }      
  }

  for (var i = 0; i < edits.length; i++) {
    var self = edits[i];  
    if(self.dataset.id) {
      self.addEventListener('click', function (event) {  
        // prevent browser's default action
        event.preventDefault();
        console.log("calling edits" + this.dataset.id);        
        // calling the edit innerHTML
        let description = document.querySelector('#description_'+this.dataset.id); 
        let descriptText = description.innerHTML;
        console.log(this.innerHTML);
        if (this.innerHTML == 'EDIT'){
        description.innerHTML = `<textarea class="form-control mt-2" rows="4" cols="50" id="textarea_description_`+this.dataset.id+`" name="description" type="text" placeholder="Post your deepest thoughts">`+ descriptText +`</textarea>`;
        // <button class="btn btn-sm btn-success col-12 p-2 mt-1" type="submit">Edit</button>`;        
        let buttonEdit = document.createElement('button');
        buttonEdit.className = 'btn btn-sm btn-success col-12 p-2 mt-1';
        buttonEdit.addEventListener('click', () => updatePost(this.dataset.id));
        buttonEdit.innerHTML = 'Edit';
        description.appendChild(buttonEdit);
        }        
        else{            
            description.innerHTML = document.querySelector('#textarea_description_'+this.dataset.id).innerHTML;
        }
        this.innerHTML = this.innerHTML == 'EDIT'?'CANCEL':'EDIT';
      }, false);
    }      
}
});

function updatePost(id){
    console.log("update post "+id);
    let description = document.querySelector('#textarea_description_'+id).innerHTML;
    console.log('updating text' + description);

    // fetch('/posts/' + id, {
    //     method: 'PUT',
    //     body: JSON.stringify({ like : 'true' })
    //   }).then(response => { 
    //     if (!response.ok) {throw response } //throw exception
    //     else{return response.json()}
    //   }).then(result => {
    //     console.log(result); // console log the result
    //     if (result.like_post){
    //       document.querySelector("#post_like_"+id).innerHTML = like;        
    //     }
    //     else{
    //       document.querySelector("#post_like_"+id).innerHTML = unlike;
    //     }
    //     document.querySelector("#like_count_"+id).innerHTML = result.likes_count;
    //   });    
}

function likeAction(id){
  console.log("sending ajax");
  fetch('/posts/' + id, {
      method: 'PUT',
      body: JSON.stringify({ like : 'true' })
    }).then(response => { 
      if (!response.ok) {throw response } //throw exception
      else{return response.json()}
    }).then(result => {
      console.log(result); // console log the result
      if (result.like_post){
        document.querySelector("#post_like_"+id).innerHTML = like;        
      }
      else{
        document.querySelector("#post_like_"+id).innerHTML = unlike;
      }
      document.querySelector("#like_count_"+id).innerHTML = result.likes_count;
    });    
  // window.location.reload();    
}
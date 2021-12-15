document.querySelector('#addCategoryForm').onsubmit = () => {
   event.preventDefault();
    const newCategory = document.querySelector('#newCategory').value;
    const form = document.querySelector('#addCategoryForm');
   const csrfToken = form.getElementsByTagName("input")[0].value;
  console.log(newCategory);
  console.log(csrfToken);
  console.log('Hello');
  fetch('/newlisting/addCategory', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({'newCategory': newCategory})
  })

  .then(response => response.json())
  .then(data => {
    if(data.str === ""){
        //window.location.reload();
            document.querySelector('#message').style.color= '#ff6666';
        document.querySelector('#message').innerHTML= 'Category already exists!';
        
    }
    else{
      alert(`Category: ${newCategory} added!`);
      window.location.reload();
    }
  });
};
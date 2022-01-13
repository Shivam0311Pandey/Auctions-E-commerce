// if(window.innerWidth <= 1000){
//   document.querySelector('.smallScreen').style.display = 'block';
//   } else{
//     document.querySelector('.smallScreen').style.display = 'none';
// }
// window.onresize = () => {
//   console.log(window.innerWidth);
//   if(window.innerWidth <= 1000){
//     document.querySelector('.smallScreen').style.display = 'block';
//     } else{
//       document.querySelector('.smallScreen').style.display = 'none';
//     }
// }


window.onscroll = () =>{
  if(window.scrollY > window.innerHeight){
    document.querySelector('.sign').style.transform= 'translateX(0)';
  } else{
    document.querySelector('.sign').style.transform= 'translateX(160%)';
  }
};

function addremovewatchlist(item){
  const auctionId = item.getAttribute("data-auctionId");
  console.log(auctionId);
  fetch(`addremoveWatchlist/${auctionId}`)
  .then(response => response.json())
  .then(data =>{
    window.location.reload();
    document.querySelector('.watchlist-count').innerHTML = `${data.status}`;
  });
};

function placebid(formdata){
  const auctionId = formdata.getAttribute("data-auctionId");
  const startingBid = parseFloat(formdata.getAttribute("data-startingBid"));
  console.log(parseInt(auctionId));
  console.log(startingBid);
  let latestBid = formdata.getAttribute("data-latestBid");
  if(latestBid == 'None'){
    latestBid = 0;
  } else{
    latestBid = parseFloat(latestBid);
  }
  console.log(latestBid);
  const bid = parseFloat(document.querySelector('#newBid').value);
  console.log(bid);
  if(bid>=startingBid && bid>latestBid && bid>0){
    console.log('Yes!');
    const csrfToken = formdata.getElementsByTagName("input")[0].value;
    fetch('/auction/placeBid',{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({'auctionId': auctionId, 'bid':bid})
    })
    window.location.reload();
    document.querySelector('#bid-status').style.color='#00e600';
    document.querySelector('#bid-status').innerHTML='Bid placed!';
  }
  else{
    event.preventDefault();
    formdata.querySelector('#bid-status').style.color= '#ff6666';
    formdata.querySelector('#bid-status').innerHTML='Not a valid bid!';
    console.log('Not a valid bid!');
    formdata.querySelector('#newBid').value= "";
  }
};

function closelisting(listing){
  const auctionId = listing.getAttribute("data-auctionId");
  console.log(auctionId);
  fetch(`/closeLisitng/${auctionId}`)
  window.location.reload();
};

function deletecomment(i){
  const commentId = i.dataset.comment;
  console.log(commentId);
  fetch(`deleteComment/${commentId}`)
  window.location.reload();
};



function addCategoryFunction(event){
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
        document.querySelector('#message').style.color= '#ff6666';
        document.querySelector('#message').innerHTML= 'Category already exists or not valid!';
        
    }
    else{
      alert(`Category: ${newCategory} added!`);
      window.location.reload();
    }
  });
};
 
/* Function to display the sub items in a dropdown list for button category 1*/
function myFunctionCat1() {
    document.getElementById("myDropdown1").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn1')) {
      var dropdowns = document.getElementsByClassName("dropdown-content1");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

/* Function to display the sub items in a dropdown list for button category 2*/
function myFunctionCat2() {
    document.getElementById("myDropdown2").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn2')) {
      var dropdowns = document.getElementsByClassName("dropdown-content2");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

// FUnction on searching an item
//   function search(ele){
//     if (event.key === 'Enter'){
//         alert(ele.value);
//     }

//   }




// Fetch data from the API
// fetch("https://thejsway-server.herokuapp.com/api/articles")
//   .then(response => response.json()) // Translate JSON into JavaScript
//   .then(articles => {
//     articles.forEach(article => {
//       // Create title element
//       const titleElement = document.createElement("h3");
//       titleElement.textContent = article.title;
//       // Create content element
//       const contentElement = document.createElement("p");
//       contentElement.textContent = article.content;
//       // Add title and content to the page
//       const articlesElement = document.getElementById("articles");
//       articlesElement.appendChild(titleElement);
//       articlesElement.appendChild(contentElement);
//     });
//   })
//   .catch(err => {
//     console.error(err.message);
//   });




fetch("http://localhost:5000/products/getcategory",{
  headers:{
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Acess-Control-Allow-Methods": "GET",

  }
}
)
  .then((response) => response.json())
  .then((data) => {
    const category1 = document.getElementById("myDropdown1");
    var subcategory = document.createElement("a");
    subcategory.setAttribute("href", "#");
    subcategory.innerHTML = "Subcategory1";
    category1.appendChild(subcategory);
    
    var subcategory2 = document.createElement("a");
    subcategory2.setAttribute("href", "#");
    subcategory2.innerHTML = "Subcategory2";
    category1.appendChild(subcategory2);
    console.log(data,category1);
  })
  .catch((error) => {
    console.log(error);
  });













//   var xhr = null;
//   getXmlHttpRequestObject = function () {
//       if (!xhr) {
//           // Create a new XMLHttpRequest object 
//           xhr = new XMLHttpRequest();
//       }
//       console.log(xhr)
//       return xhr;
//   };
//   function getCategory(){
//     xhr = getXmlHttpRequestObject();
//     xhr.onreadystatechange = dataCallback;
//     //asynchronous requests
//     xhr.open("GET", "http://127.0.0.1:5000/category", true);
//     // Send the request over the network
//     xhr.send(null);
//   }
//   function dataCallback() {
//       // Check response is ready or not
//       if (xhr.readyState == 4 && xhr.status == 200) {
//           console.log("User data received!");
//           var data = JSON.parse(xhr.responseText);
//         //   console.log(data);
//            dataDiv = document.getElementsByClassName('dropbtn1');
//           // Set current data text
//           dataDiv.innerHTML = xhr.responseText;
//       }
//   }

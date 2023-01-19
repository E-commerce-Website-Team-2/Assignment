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
  function search(ele){
    if (event.key === 'Enter'){
      const inputelement = document.getElementById("search");
      const query = inputelement.value;
      inputelement.value = "";
      fetch(`http://localhost:5000/products/search?query=${query}`,{
        headers:{
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Acess-Control-Allow-Methods": "GET",
      
        }
      }
      )
        .then((response) => response.json())
        .then((data) => {

          product_element = document.getElementById("subsection");
          product_element.innerHTML = "";
          for ( ind in data) {

            div_element = document.createElement("div");
            div_element.setAttribute("class", "items");

            div_sub = document.createElement("div");
            div_sub.setAttribute("class", "img img1");

            img_element = document.createElement("img");
            img_element.setAttribute("src",data[ind]["productImage"]);

            div_sub.appendChild(img_element);

            div_name = document.createElement("div");
            div_name.setAttribute("class","name");
            div_name.innerHTML = "Product1";

            div_price = document.createElement("div");
            div_price.setAttribute("class","price");
            div_price.innerHTML = data[ind]["price"];

            div_element.appendChild(div_sub);
            div_element.appendChild(div_name);
            div_element.appendChild(div_price);

            
            product_element.appendChild(div_element);
            console.log(product_element);
            console.log(data[ind]);
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }

  }

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
      category_call = `http://localhost:5000/products/category?cat1="men"&cat2=${data.men[subcategory]}`
      for (var subcategory in data.men){
        var subcategory1 = document.createElement("a");
        subcategory1.setAttribute("href", '');
        subcategory1.innerHTML = data.men[subcategory];
        document.getElementById("myDropdown1").appendChild(subcategory1);
      }
      for (var subcategory in data.women){
        var subcategory2 = document.createElement("a");
        subcategory2.setAttribute("href", '');
        subcategory2.innerHTML = data.women[subcategory];
        document.getElementById("myDropdown2").appendChild(subcategory2);
      }
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

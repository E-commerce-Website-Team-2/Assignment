// This is used fetch subcategories from the backend via database and update thhe dropdown menu in the forntend.
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
  for (var subcategory in data.men){
    var list_element = document.createElement("li");
    var subcategory1 = document.createElement("a");
    var cat1 = 'men';
    var cat2 = data.men[subcategory];
    subcategory1.setAttribute("class","dropdown-item");
    subcategory1.setAttribute("onclick",`Category('${cat1}','${cat2}')`);
    console.log(subcategory1);
    subcategory1.innerHTML = data.men[subcategory];
    list_element.appendChild(subcategory1)
    document.getElementsByClassName("cat1")[0].appendChild(list_element);
  }


  for (var subcategory in data.women){
    var list_element = document.createElement("li");
    var subcategory1 = document.createElement("a");
    var cat1 = 'women';
    var cat2 = data.women[subcategory];
    subcategory1.setAttribute("class","dropdown-item");
    subcategory1.setAttribute("onclick",`Category('${cat1}','${cat2}')`);
    console.log(subcategory1);
    subcategory1.innerHTML = data.women[subcategory];
    list_element.appendChild(subcategory1)
    document.getElementsByClassName("cat2")[0].appendChild(list_element);
  }
})
.catch((error) => {
console.log(error);
});



// Function on searching an item - Get response from backend and add the response products to the forntend page
function search(ele){
  
  if (event.key === 'Enter'){
    // window.location.href = 'http://localhost:8000/index.html';
    console.log("hello");
    const inputelement = document.getElementById("search");
    const query = inputelement.value;
    inputelement.value = "";
    
    fetch(`http://localhost:5000/products/search/1?query=${query}`,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",
    
      }
    }
  )
    .then((response) => response.json())
    .then((data) => {
        
      product_element = document.getElementsByClassName("pro-container")[0];
      product_element.innerHTML = "";
      for ( ind in data) {
        console.log( data[ind])
        div_element = document.createElement("div");
        div_element.setAttribute("class", "pro");
        div_element.setAttribute("onclick",`DetailedProduct(${data[ind]["uniqueID"]},'${data[ind]["name"]}',${data[ind]["price"]},'${data[ind]["productImage"]}')`);


        img_element = document.createElement("img");
        img_element.setAttribute("src",data[ind]["productImage"]);

        div_element.appendChild(img_element);

        div_name = document.createElement("div");
        div_name.setAttribute("class","des");

        h5_element = document.createElement("h5");
        h5_element.innerHTML = data[ind]["name"];

        h4_element = document.createElement("h4");
        h4_element.innerHTML = data[ind]["price"];

        div_name.appendChild(h5_element);
        div_name.appendChild(h4_element);
        div_element.appendChild(div_name);

        
        product_element.appendChild(div_element);
        // console.log(product_element);
        // console.log(data[ind]["name"]);
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

}

// This function is used to return the products when a subcategory is selected. It asks backend for the products with subcategories.

function Category(cat1,cat2){
  console.log(cat1,cat2);
  let params = {
  "cat1": cat1,
  "cat2": cat2
  };
  
  let query = Object.keys(params)
             .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
             .join('&');
  
  let url = 'http://localhost:5000/products/category/1?' + query;
  fetch(url,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",
    
      }
    }
    )
      .then((response) => response.json())
      .then((data) => {
        
        product_element = document.getElementsByClassName("pro-container")[0];
        product_element.innerHTML = "";
        for ( let ind = 1; ind<data.length; ind++ ) {
          console.log( data[ind])
          div_element = document.createElement("div");
          div_element.setAttribute("class", "pro");
          div_element.setAttribute("onclick",`DetailedProduct(${data[ind]["uniqueID"]},'${data[ind]["name"]}',${data[ind]["price"]},'${data[ind]["productimage"]}')`);
  
  
          img_element = document.createElement("img");
          img_element.setAttribute("src",data[ind]["productimage"]);
  
          div_element.appendChild(img_element);
  
          div_name = document.createElement("div");
          div_name.setAttribute("class","des");
  
          h5_element = document.createElement("h5");
          h5_element.innerHTML = data[ind]["name"];
  
          h4_element = document.createElement("h4");
          h4_element.innerHTML = data[ind]["price"];
  
          div_name.appendChild(h5_element);
          div_name.appendChild(h4_element);
          div_element.appendChild(div_name);
  
          
          product_element.appendChild(div_element);
          // console.log(product_element);
          // console.log(data[ind]["name"]);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }
  
    
// This function is called when a user clicks on a product whhichh moves to another product_detail html element with some properties sent to it.

function DetailedProduct(id,name,price,image){
  let params = {
      "uniqueId": id,
      "name": name,
      "price": price,
      "image": image,
    };
    
  let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
    
  let url = 'http://localhost:8000/product_detail.html?' + query;
  document.location.href = url;

}



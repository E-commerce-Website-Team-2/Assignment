// This is used fetch subcategories from the backend via database and update thhe dropdown menu in the forntend.
window.onload = fetch("http://localhost:5000/products/categorytree",{
    headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",

      }
    }
  )
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    for (ind in data[1]){
      category_element = document.getElementById("category");
      div_element = document.createElement("div");
      
      button_element = document.createElement("button");
      button_element.setAttribute("class", "btn btn-secondary dropdown-toggle");
      button_element.setAttribute("type", "button");
      button_element.setAttribute("id","dropdownMenuButton1");
      button_element.setAttribute("data-bs-toggle", "dropdown");
      button_element.setAttribute("aria-expanded", "false");
      button_element.setAttribute("value",data[1][ind][0]);
      // console.log(data[1][0]);
      button_element.innerHTML = data[1][ind][1];
      console.log(data[1][ind])
      button_element.addEventListener('click', function(){
        GetProduct(this)
      });

      // button_element.setAttribute('onclick',`GetProduct(${this},${data[1][ind][0]}`);
      ulist_element = document.createElement("ul");
      ulist_element.setAttribute("class","dropdown-menu");
      ulist_element.setAttribute("aria-labelledby","dropdownMenuButton1");

      div_element.appendChild(button_element);
      div_element.appendChild(ulist_element);
      category_element.appendChild(div_element);
    }
  })
  .catch((error) => {
  console.log(error);
  });

function GetProduct(ele){
  parentElement = ele.parentNode;
  console.log(parentElement.childNodes[1].childNodes.length)
  if(parentElement.childNodes[1].childNodes.length == 0){
    fetch(`http://localhost:5000/products/categorytree?cat=${ele.value}`,{
      headers:{
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Acess-Control-Allow-Methods": "GET",
  
        }
      }
    )
    .then((response) => response.json())
    .then((data) => {
      // console.log(data);
      
      for (ind in data[1]){
        var list_element = document.createElement("li");
        var subcategory1 = document.createElement("a");
  
  
        let url = `http://localhost:8000/index.html?cat=${data[1][ind][0]}&pageno=1`;
  
        subcategory1.setAttribute("class","dropdown-item");
        subcategory1.setAttribute("href",url);
        // console.log(subcategory1);
        subcategory1.innerHTML = data[1][ind][1];
        list_element.appendChild(subcategory1)
        parentElement.childNodes[1].appendChild(list_element);
      }
  
  
  
    })
    .catch((error) => {
    console.log(error);
    });
  }

}

// Below code is used to redirect to home page on searching or selecting a category
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if (urlParams.has('search')&urlParams.has('pageno')){
  var query = urlParams.get('search');
  var pageno = urlParams.get('pageno');
  var sort = "";
  if(urlParams.has('sort')){
    sort = urlParams.get('sort');
  }
  fill_products(query,pageno,sort);
}
if (urlParams.has('cat') && urlParams.has('pageno')){
  var cat = urlParams.get('cat');
  var pageno = urlParams.get('pageno');
  var sort = "";
  if(urlParams.has('sort')){
    sort = urlParams.get('sort');
  }
  Category(cat,pageno,sort);
}


// Function to create url when a category is selected of a pageno with a sort filter applied
function createURLforCategory(cat,pageno,sort){
  var params = {
    "cat": cat,
    "pageno":pageno,
    "sort":sort
    };
  var query = Object.keys(params)
         .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
         .join('&');
  var url = `http://localhost:8000/index.html?` + query;
  return url;
}

// Function to fill the home page with products sent from the backend for thhe particular search query and page number
function fill_products(query,pageno,sort){
  // 1. Fetch the products with given query and page number from backend
  fetch(`http://localhost:5000/products/search/${pageno}?query=${query}&sort=${sort}`,{
      headers:{
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Acess-Control-Allow-Methods": "GET",
    
      }
    }
  )
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data[0] == 200){
        console.log(data);
        // 2.  Get the number of products sent in the response from the backend and calculate the no of pages
        no_of_products = data[1];
        no_of_pages = Math.ceil(no_of_products/9);

        //3. Get the pagination section where the pagination with given pages is created
        ul_element = document.getElementsByClassName("pagination")[0];
        ul_element.innerHTML = "";

        //4. Get the product section where the products is going to be added
        product_element = document.getElementsByClassName("pro-container")[0];
        product_element.innerHTML = "";

        // Get the filter dropdown menu to visible and set the href attribut of the dropdown list
        document.getElementsByClassName("dropdown-3")[0].style.display = "block";
        document.getElementsByClassName("asc")[0].setAttribute("href",`http://localhost:8000/index.html?search=${query}&pageno=${pageno}&sort=1`);
        document.getElementsByClassName("desc")[0].setAttribute("href",`http://localhost:8000/index.html?search=${query}&pageno=${pageno}&sort=2`);

        //5. Iterate through the response data containing a list of products and append it to the html page under the product section
        for (let ind = 2; ind<data.length; ind++ ) {

          div_element = document.createElement("div");
          div_element.setAttribute("class", "pro");
          div_element.setAttribute("onclick",`DetailedProduct("${data[ind]["uniqueId"]}","${data[ind]["name"]}",${data[ind]["price"]},"${data[ind]["productImage"]}")`);


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

          //6. Add the pagination section with the particular pageno and query text
          if (!document.getElementsByClassName("pagination")[0].hasChildNodes()){
            createPagination(query,no_of_pages,pageno,sort);
          }
        }

      }
      else{
          window.location.href = 'http://localhost:8000/404.html';

      }
    })   .catch((error) => {
      console.log(error);
    });
}

// Function on searching an item - Get response from backend and add the response products to the forntend page
function search(ele){
  // If user hits enter in the search input tag
  if (event.key === 'Enter'){
    // Recieve the value from the input tag and encode the value 
    const inputelement = document.getElementById("search");
    let query = inputelement.value;
    inputelement.value = "";
    query = encodeURIComponent(query);
    // Change the location with search and page parameter added to the current window.
    window.location.href = `http://localhost:8000/index.html?search=${query}&pageno=1`;
    
      }
  }

// This function is used to return the products when a subcategory is selected. It asks backend for the products with subcategories.
function Category(cat,pageno,sort){
  

  // Genrate the url with thhe parameters cat1 and cat2 and call to backend with parameters to recieve the category tree.
  let params = {
    "cat": cat,
    "sort":sort
    };
  
  let query = Object.keys(params)
             .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
             .join('&');
  let url = `http://localhost:5000/products/category/${pageno}?` + query;


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
        console.log(data);
        if(data[0] == 200){
          // Get the number of products sent in the response from the backend and calculate the no of pages
          no_of_products = data[1];
          no_of_pages = Math.ceil(no_of_products/9);

          // Get the pagination section where the pagination with given pages is created
          ul_element = document.getElementsByClassName("pagination")[0];
          ul_element.innerHTML = "";

          // Get the product section where the products is going to be added
          product_element = document.getElementsByClassName("pro-container")[0];
          product_element.innerHTML = "";

        // Get the filter dropdown menu to visible and set the href attribut of the dropdown list
        document.getElementsByClassName("dropdown-3")[0].style.display = "block";

        document.getElementsByClassName("asc")[0].setAttribute("href",createURLforCategory(cat,pageno,1));
        document.getElementsByClassName("desc")[0].setAttribute("href",createURLforCategory(cat,pageno,2));

          //Iterate through the response data containing a list of products and append it to the html page under the product section
          for ( let ind = 2; ind<data.length; ind++ ) {

            div_element = document.createElement("div");
            div_element.setAttribute("class", "pro");
            console.log(typeof data[ind]["name"]);
            div_element.setAttribute("onclick",`DetailedProduct('${data[ind]["uniqueID"]}',"${data[ind]["name"]}",${data[ind]["price"]},'${data[ind]["productimage"]}')`);
    
    
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
          }

          // Add the pagination section with the particular pageno and query text
          if (!document.getElementsByClassName("pagination")[0].hasChildNodes()){
              createPaginationCategory(cat,no_of_pages,pageno,sort);
            }
          }
        else{
          window.location.href = 'http://localhost:8000/404.html';

        }

      })
      .catch((error) => {
        console.log(error);
      });


  }

// This function is called when a user clicks on a product whhichh moves to another product_detail html element with some properties sent to it.
function DetailedProduct(id,name,price,image){

  // Generate a url with the respective paramaeters thhat needs to fetched in product_detail page.
  let params = {
      "uniqueId": id,
      "name": name,
      "price": price,
      "image": image,
    };
    
  let query = Object.keys(params)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
               .join('&');
  console.log(id);
  let url = 'http://localhost:8000/product_detail.html?' + query;

  // Change the window location to the new url created above.
  document.location.href = url;

}


// Function to change the css of pageno on clicking a page 
function SelectPage(el)
{
    // This is used for making the current page selected to active which changes the css of the highleted page.
    $('.page-item').removeClass('active');
    $(el).parent().addClass('active');
} 

// Function to create Pagination for searching.
function createPagination(searchText,pages,pageno,sort){
  // Acess the pagination section for thhe pages to be added
  ul_element = document.getElementsByClassName("pagination")[0];
  list_element = document.createElement("li");

  // If current pageno is 1 then set thhe prev button to disabled else set the location to the previous page
  if (pageno == 1){
    list_element.setAttribute("class","page-item disabled");
  }
  else{
    list_element.setAttribute("class","page-item");
    list_element.setAttribute("onclick",`window.location.href='http://localhost:8000/index.html?search=${searchText}&pageno=${pageno-1}&sort=${sort}'`);
  }
  

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Prev";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);

  // Generate the max and min index of the current pageno (+5 and -5 from current page)
  pageno = Number(pageno);
  if(pageno - 5 <= 0){
    min_index = 1;
  }else{
    min_index = pageno - 5;
  }

  if(pageno + 5 >= pages){
    max_index = pages;
  }else{
    max_index = pageno + 5;
  }

  // console.log(min_index,max_index,pages);

  // Create the pages and add an extra active class to the current page
  for (var i = min_index; i<=max_index;i++){
    list_element = document.createElement("li");
    if (i === pageno){
      list_element.setAttribute("class","page-item active");
    }else{
      list_element.setAttribute("class","page-item");
    }


    anchor_element = document.createElement("a");
    anchor_element.setAttribute("class","page-link");
    anchor_element.setAttribute("href",`http://localhost:8000/index.html?search=${searchText}&pageno=${i}&sort=${sort}`);
    anchor_element.setAttribute("onclick",'SelectPage(this)');

    anchor_element.innerHTML = i;
    list_element.appendChild(anchor_element);
    ul_element.appendChild(list_element);
  }


  list_element = document.createElement("li");

  // If current pageno is the max page then set thhe next button to disabled else set the location to the next page
  if (pageno === pages){
  list_element.setAttribute("class","page-item disabled");
  }
  else{
  list_element.setAttribute("class","page-item");
  list_element.setAttribute("onclick",`window.location.href='http://localhost:8000/index.html?search=${searchText}&pageno=${pageno+1}&sort=${sort}'`);
  }

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Next";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);
  
}

// Function to create Pagination when a category button is selected.
function createPaginationCategory(cat,pages,pageno,sort){
    // Acess the pagination section for thhe pages to be added
  ul_element = document.getElementsByClassName("pagination")[0];

  
  list_element = document.createElement("li");

  // If current pageno is 1 then set thhe prev button to disabled else set the location to the previous page
  if (pageno == 1){
    list_element.setAttribute("class","page-item disabled");
  }
  else{
    list_element.setAttribute("class","page-item");
    url = createURLforCategory(cat,pageno-1,sort);
    list_element.setAttribute("onclick",`window.location.href='${url}'`);
  }
  

  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Prev";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);

  // Generate the max and min index of the current pageno (+5 and -5 from current page)
  pageno = Number(pageno);
  if(pageno - 5 <= 0){
    min_index = 1;
  }else{
    min_index = pageno - 5;
  }

  if(pageno + 5 >= pages){
    max_index = pages;
  }else{
    max_index = pageno + 5;
  }

  // console.log(min_index,max_index,pages);

  // Create the pages and add an extra active class to the current page
  for (var i = min_index; i<=max_index;i++){
    list_element = document.createElement("li");
    if (i === pageno){
      list_element.setAttribute("class","page-item active");
    }else{
      list_element.setAttribute("class","page-item");
    }

    url = createURLforCategory(cat,i,sort);

    anchor_element = document.createElement("a");
    anchor_element.setAttribute("class","page-link");
    anchor_element.setAttribute("href",url);
    anchor_element.setAttribute("onclick",'SelectPage(this)');

    anchor_element.innerHTML = i;
    list_element.appendChild(anchor_element);
    ul_element.appendChild(list_element);
  }



  list_element = document.createElement("li");

  // If current pageno is the max page then set thhe next button to disabled else set to the next page
  if (pageno === pages){
  list_element.setAttribute("class","page-item disabled");
  }
  else{
  list_element.setAttribute("class","page-item");
  url = createURLforCategory(cat,pageno+1,sort);
  list_element.setAttribute("onclick",`window.location.href='${url}'`);
  }
  anchor_element = document.createElement("a");
  anchor_element.setAttribute("class","page-link");

  anchor_element.innerHTML = "Next";
  list_element.appendChild(anchor_element);
  ul_element.appendChild(list_element);
  
}




